from django.urls import path
from . import views

urlpatterns = [
    path('product/<uuid:product_uuid>/', views.product_detail, name='product_detail'),
    path('event/<uuid:event_uuid>/', views.event_detail, name='event_detail'),
    path('add/', views.add_product, name='add_product'),
]





