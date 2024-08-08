from django.contrib import admin
from .models import Category, Event, Product, ProductVariant


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',        
        'image',
        'price',
    )

class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name',              
        'price',
        'image',    
        'event_datetime',
    )

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'size',              
        'price',      
    )

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)

