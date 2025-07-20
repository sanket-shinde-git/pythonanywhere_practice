"""
URL configuration for first_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from product.views import greet,plain_text, html_view, greet_user,hello_user,usr_list,get_products, create_products ,hard_delete_prod,update_prod,soft_delete,get_stock,make_available,upload_csv,download_csv,password_change

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',greet),
    path('ptv/',plain_text ),
    path('htv/',html_view),
    path('greet-user/',greet_user),
    path('hello-user/',hello_user),
    path('usr-list/',usr_list, name= 'usr_list'),
    path('get-products/',get_products, name= "get_all_products"),
    path('create-products/', create_products, name ="create_products"),
    path('delete-products/<int:product_id>', hard_delete_prod, name ="hard_delete_prod"),
    path('update-products/<int:product_id>', update_prod, name ="update_prod"),
    path('soft-delete/<int:product_id>', soft_delete, name ="soft_delete"),
    path('get-stock/', get_stock, name ="get_stock"),
    path('make-available/<int:product_id>', make_available, name ="make_available"),
    path('upload-csv/', upload_csv, name = 'upload_csv'),
    path('download-csv/<str:data_type>/', download_csv, name = 'download_csv'),
    path('accounts/password_change/', password_change,  name='password_change'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),



]
