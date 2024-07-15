from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    # path('add/<uuid:item_id>/', views.add_to_bag, name='add_to_bag'), 
    path('add_product_to_bag/<uuid:item_id>/', views.add_product_to_bag, name='add_product_to_bag'),
    path('add_event_to_bag/<uuid:item_id>/', views.add_event_to_bag, name='add_event_to_bag'),
    path('update_card_message/<uuid:item_id>/', views.update_card_message, name='update_card_message'),
    path('update_note_to_host/<uuid:item_id>/', views.update_note_to_host, name='update_note_to_host'),
    path('update_note_to_seller/<uuid:item_id>/', views.update_note_to_seller, name='update_note_to_seller'),
    path('update_quantity/<uuid:item_id>/', views.update_quantity, name='update_quantity'),
    path('remove_item/<uuid:item_id>/', views.remove_item, name='remove_item'),       
]