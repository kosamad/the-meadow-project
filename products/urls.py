from django.urls import path

# import views from the current directory
from . import views

urlpatterns = [   
    path('<product_id>', views.product_detail, name='product_detail'),
]