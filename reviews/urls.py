from django.urls import path
from . import views

urlpatterns = [
    path('review/', views.reviews, name='reviews'),
    path('review_order/<int:order_id>/', views.review_order, name='review_order'),  
]