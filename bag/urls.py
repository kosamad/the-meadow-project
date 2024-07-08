from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<uuid:item_id>/', views.add_to_bag, name='add_to_bag'),    
    path('clear-basket/', views.clear_basket, name='clear_basket'),    
]