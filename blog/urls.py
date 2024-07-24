from django.urls import path
from . import views
from .views import AddPostView

urlpatterns = [
    path('', views.all_posts, name='posts'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
]