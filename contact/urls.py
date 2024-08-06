from django.urls import path
from . import views

# import views from the current directory


urlpatterns = [
    path('contact/', views.contact, name='contact')
]