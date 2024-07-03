from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',        
        'category',        
        'price',
        'rating',
        'image',
    ) 

    ordering = ('name',)            

    
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name',              
        'price',
        'image',    
        'event_datetime',
    ) 

    ordering = ('name',)     



# Registered models.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
