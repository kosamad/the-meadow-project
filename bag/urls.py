from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add_product_to_bag/<int:item_id>/', views.add_product_to_bag, name='add_product_to_bag'),
    path('add_event_to_bag/<int:item_id>/', views.add_event_to_bag, name='add_event_to_bag'),
    path('update_card_message/<int:item_id>/', views.update_card_message, name='update_card_message'),
    path('update_note_to_host/<int:item_id>/', views.update_note_to_host, name='update_note_to_host'),
    path('update_note_to_seller/<int:item_id>/', views.update_note_to_seller, name='update_note_to_seller'),
    path('update_quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
]
