from django.contrib import admin
from products.models import Product, Category, Event

class BagAdmin(admin.ModelAdmin):
    list_dislay = (
        'name', 
        'type',
        'item_id',       
        'category',                
        'price',
        'quantity',        
    )

# Register your models here.
