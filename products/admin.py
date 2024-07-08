from django.contrib import admin
from .models import Category, Event, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',              
        'price',
        'image',        
    )

class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name',              
        'price',
        'image',    
        'event_datetime',
    )

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Event, EventAdmin)

