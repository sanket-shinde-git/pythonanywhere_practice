from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import request, JsonResponse, HttpResponse,HttpResponseNotAllowed
from flask import jsonify , Response
from .models import Product
import pandas as pd
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import io

# Create your views here.,


def greet(request):

    data = {
        "msg": "Welcome to Page"

    }
    return JsonResponse(data)


def plain_text(request):
    return HttpResponse("HTTPResponse Plain text ")


def html_view(request):
    html_data = "<h1>  H1 heading </h1><p> Paragraph </p>"
    return HttpResponse(html_data)


def greet_user(request):
    name = request.GET.get("name", "Guest")
    return HttpResponse(f"Hello, {name}!")


def hello_user(request):    
    nm = request.GET.get("name", "GUEST")
    context = {
        'name': nm}
    return render(request, 'home.html', context)

@login_required
def usr_list(request):
    users = ['sanket', 'shiv', 'om ','pruthvi']

    return render(request, 'users.html', {"users": users})



@login_required
@csrf_exempt
def create_products(request):
    print("Request method:", request.method)

    if request.method == "POST":
        # print('inside create before assignment')
        name = request.POST["nm"]
        descr = request.POST["desc"]
        price = request.POST["prc"]
        qty = request.POST["qty"]
        
        product_id = request.POST.get("prod_id")

        if not product_id:
            Product.objects.create(
                name=name, 
                description=descr, 
                price=price, 
                qty=qty, 
                created_by = request.user)

        else:
            prod_obj = Product.objects.get(id=product_id)
            prod_obj.name = name
            prod_obj.description = descr
            prod_obj.price = price
            prod_obj.qty = qty
            prod_obj.updated_by = request.user  
            prod_obj.save()

        return redirect("get_all_products")

    else:

        return render(request, "create_products.html")
    


@login_required
@csrf_exempt
def hard_delete_prod(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect("get_all_products")

@login_required
@csrf_exempt
def soft_delete(request, product_id):
    product = Product.objects.get(id=product_id)
    product.is_deleted = True
    product.deleted_by = request.user  

    product.save()
    return redirect("get_all_products")


@login_required
@csrf_exempt
def update_prod(request, product_id):
    prod = Product.objects.get(id=product_id)
    return render(request, "create_products.html", {'product': prod})

@login_required
def get_stock(request):
    # all_prod = Product.objects.all()  # select * from product
    all_prod = Product.objects.filter(is_deleted = True)      #select * from product where is_deleted = False

    return render(request, 'available.html', {'Product': all_prod})

@login_required
@csrf_exempt
def make_available(request, product_id):
    product = Product.objects.get(id=product_id)
    product.is_deleted = False
    product.save()
    return redirect("get_all_products")

@login_required
@csrf_exempt
def upload_csv(request):
    if request.method == "POST":

        if "csv_file" not in request.FILES:
            return JsonResponse({"msg": "Incorrect file"})

        csv_file = request.FILES["csv_file"]                #what is the use of this and above 2 lines

        if not csv_file.name.endswith('.csv'):
            print("not CSV file  ##########################################################")
            return HttpResponse("Please upload a valid CSV file.")

        df = pd.read_csv(csv_file, encoding='utf-8-sig')

        required_col = {'name', 'description', 'price', 'qty'}
        df.columns = [col.strip().lower() for col in df.columns]

        if not required_col.issubset(df.columns):
            return HttpResponse("Please upload a CSV with valid columns.")

        for i, row in df.iterrows():
            Product.objects.create(
                name=row['name'],
                description=row['description'],
                price=row['price'],
                qty=row['qty'],
                created_by=User.objects.get(username='admin')
            )

        return HttpResponse("CSV uploaded and products created successfully.")

    # If not POST, show the upload form
    return render(request, "products.html")

@login_required
@csrf_exempt
def get_products(request):
    # Get active (non-deleted) products
    active_prod = Product.objects.filter(is_deleted=False)

    # Get soft deleted products
    deleted_prod = Product.objects.filter(is_deleted=True)

    # Store the filtered data in the session for later use in CSV download
    active_data = [{
        'id': prod.id,
        'name': prod.name,
        'description': prod.description,
        'price': prod.price,
        'qty': prod.qty,
        'is_deleted': prod.is_deleted
    } for prod in active_prod]

    deleted_data = [{
        'id': prod.id,
        'name': prod.name,
        'description': prod.description,
        'price': prod.price,
        'qty': prod.qty,
        'is_deleted': prod.is_deleted
    } for prod in deleted_prod]

    # Store the product data in the session
    request.session['active_product_data'] = active_data
    request.session['deleted_product_data'] = deleted_data

    return render(request, 'products.html', {'Product': active_prod, 'Deleted_Product': deleted_prod})


@login_required
@csrf_exempt
def download_csv(request, data_type):
    if request.method == "GET":
        # Check which data type to download
        if data_type == "active":
            # Retrieve active product data (non-deleted)
            data = request.session.get('active_product_data', [])
            filename = "active_products.csv"
        elif data_type == "deleted":
            # Retrieve deleted product data (soft-deleted)
            data = request.session.get('deleted_product_data', [])
            filename = "soft_deleted_products.csv"
        else:
            return HttpResponse("Invalid data type.", status=400)

        if not data:
            return HttpResponse("No product data found.", status=404)

        # Create DataFrame from the session data
        df = pd.DataFrame(data)

        # Generate CSV from DataFrame
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        # Prepare the HTTP response for file download
        response = HttpResponse(output.getvalue(), content_type="text/csv")
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response

    # If the request method is not GET, return an error
    return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            logout(request)

            return redirect(reverse('login'))
        
    else :
        form = PasswordChangeForm(user=request.user)

    return render(request, 'registration/change_pass.html', {'form': form})

































# @csrf_exempt
# def get_products(request):
#     # all_prod = Product.objects.all()      #select * from product
#     # select * from product where is_deleted = False
#     all_prod = Product.objects.filter(is_deleted=False)

#     # request.session['product_data'] = list(all_prod.values())       #--------- download/upload 

#     return render(request, 'products.html', {'Product': all_prod})




# @csrf_exempt
# def download_csv(request):
#     if request.method == "GET":
        
#         obj_prod = Product.objects.all()


#         # data = request.session.get('product_data', [])


#         data = [{
#         'id': prod.id,
#         'name': prod.name,
#         'description': prod.description,
#         'price': prod.price,
#         'qty': prod.qty,
#         'is_deleted': prod.is_deleted

#         } for prod in obj_prod]


#         print(data)



#         df = pd.DataFrame(data)
#         print(df)

#         output = io.StringIO()
#         df.to_csv(output, index=False)
#         output.seek(0)


#         response = HttpResponse(output.getvalue(),content_type = "text/csv")
#         response['Content-Disposition']='attachment; filename=django_products.csv'
#         return response
#     return HttpResponseNotAllowed(['GET']) #     return HttpResponse("Only GET method is allowed.")


#     # return Response(output, mimetype= 'text/csv', headers={"Content-Disposition":"Attachments; filename = django_products.csv"})



# forms.py
# from .forms import ProductForm
# from django import forms
# from .models import Product

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name', 'description', 'price', 'qty']
