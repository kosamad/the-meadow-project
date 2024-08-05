from django.urls import path

# import views from the current directory
from . import views

urlpatterns = [
    path('', views.contact, name='contact')
]