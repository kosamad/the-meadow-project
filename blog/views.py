from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# Create your views here.

def blog(request):
    """ A view to return the blog page """
    # Gather data
    posts = Post.objects.all()







    return render(request, 'blog/blog.html')


