from django.urls import path

# import views from the current directory
from . import views

urlpatterns = [   
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),    
]




