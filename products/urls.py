from django.urls import path

# import views from the current directory
from . import views

urlpatterns = [   
    path('products/<product_id>/', views.product_detail, name='product_detail'),
    path('events/<event_id>/', views.event_detail, name='event_detail'),      
]




