from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post


# Create your views here.

def all_posts(request):
    """ A view to return the blog page with all blog items """
    # Gather data
    posts = Post.objects.all()
    # pagination to limit how many posts per page
    paginator = Paginator(posts, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'page_number': page_number,
        'page_obj': page_obj
        }

    return render(request, 'blog/posts.html', context)


