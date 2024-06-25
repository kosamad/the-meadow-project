from django.urls import path

# import views from the current directory
from . import views

urlpatterns = [
    path('flowers/', views.flowers, name='flowers'),
    path('plants/', views.plants, name='plants'),
]