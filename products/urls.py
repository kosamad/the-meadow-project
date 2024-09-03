from django.urls import path
from . import views

urlpatterns = [
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('event/<int:id>/', views.event_detail, name='event_detail'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_event/', views.add_event, name='add_event'),
    path('add_variant/<int:product_id>/', views.add_product_variant, name='add_product_variant'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('delete_product_variant/<int:variant_id>/', views.delete_product_variant, name='delete_product_variant'),
    path('edit_product_variant/<int:variant_id>/', views.edit_product_variant, name='edit_product_variant'),
    path('edit_event/<int:id>/', views.edit_event, name='edit_event'),
    path('delete_event/<int:id>/', views.delete_event, name='delete_event'),
]





