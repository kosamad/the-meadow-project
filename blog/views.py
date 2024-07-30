from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import PostForm
from django.urls import reverse_lazy



# Create your views here.

def all_posts(request):
    """ A view to return the blog page with all blog items """
    # Gather data
    posts = Post.objects.all()

    # Search requests
    query = ''
    no_results = False 
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
        # Check if there are no results
        posts = posts.filter(post_queries)
        if not posts.exists():
            no_results = True

    # pagination to limit how many posts per page
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  
               

    context = {
        'posts': posts,
        'page_number': page_number,
        'page_obj': page_obj,
        'search_term': query,
        'no_results': no_results, 
        }

    return render(request, 'blog/posts.html', context)


def post_detail(request, post_id):
    
    post = get_object_or_404(Post, id=post_id)

    context = {
        'post': post
    }

    return render(request, 'blog/post_detail.html', context)


    

# Code to add/eidt/delete a blog post using CreateView/UpdateView/DeleteView ammended from Youtube tutorial by Codemy
class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'



class UpdatePostView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'    
    context_object_name = 'post'

    # Resolve Url when needed
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'post_id': self.object.id})


class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'

    # Function ensures users 'go back' to the page they came from
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER', reverse_lazy('posts'))
        return context 

    # redirect after successful deletion.     
    def get_success_url(self):
        return reverse_lazy('posts')
   
    


