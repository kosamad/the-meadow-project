from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# Create your views here.

def all_posts(request):
    """ A view to return the blog page with all blog items """
    # Gather data
    posts = Post.objects.all()

    context = {
        'posts': posts,
    }







    return render(request, 'blog/posts.html', context)


