from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(blank= 100)
    price = models.PositiveIntegerField()
    qty = models.PositiveIntegerField()
    is_deleted = models.BooleanField(default= False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete= models.SET_NULL, null=True,  related_name='products')
    updated_by = models.ForeignKey(User, on_delete= models.SET_NULL, null=True,  related_name='products_updated')
    deleted_by = models.ForeignKey(User, on_delete= models.SET_NULL, null=True,  related_name='products_deleted')







    def __str__(self):
        return f'{self.name} - ${self.price}'
    
