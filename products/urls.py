from django.urls import path
from . import views

urlpatterns = [
    path('product/<uuid:product_uuid>/', views.product_detail, name='product_detail'),
    path('event/<uuid:event_uuid>/', views.product_detail, name='event_detail'),
]





