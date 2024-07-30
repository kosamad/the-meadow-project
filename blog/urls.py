from django.urls import path
from . import views
from .views import AddPostView, UpdatePostView, DeletePostView

urlpatterns = [
    path('', views.all_posts, name='posts'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
    path('post/<int:pk>/edit/', UpdatePostView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='post_delete'),
]