from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post



# Create your views here.

def all_posts(request):
    """ A view to return the blog page with all blog items """
    # Gather data
    posts = Post.objects.all()

    # Search requests
    query = ''  
    if 'q' in request.GET:
        query = request.GET['q']
        # if the query is blank = an error message
        if not query:
            messages.error(request, "You didn't enter a search")
            return redirect(reverse('posts'))

        # product and event queries for name, descritpion and category
        post_queries = (
        Q(title__icontains=query) | 
        Q(body__icontains=query)              
        )
        posts = posts.filter(post_queries)

    # pagination to limit how many posts per page
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  
               

    context = {
        'posts': posts,
        'page_number': page_number,
        'page_obj': page_obj,
        'search_term': query,
        }

    return render(request, 'blog/posts.html', context)


