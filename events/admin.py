from django.contrib import admin
from .models import Event

# Registered models

class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name',              
        'price',
        'image',
    ) 

    ordering = ('name',)     

admin.site.register(Event, EventAdmin)