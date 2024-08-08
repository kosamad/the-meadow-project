from django.urls import path
from . import views

urlpatterns = [
    path('product/<uuid:product_uuid>/', views.product_detail, name='product_detail'),
    path('event/<uuid:event_uuid>/', views.event_detail, name='event_detail'),
    path('add/', views.add_product, name='add_product'),
    path('add_variant/<uuid:product_uuid>/', views.add_product_variant, name='add_product_variant'),
    path('edit_product/<uuid:product_uuid>/', views.edit_product, name='edit_product'),
    path('edit_product_variant/<int:variant_id>/', views.edit_product_variant, name='edit_product_variant'),
]





