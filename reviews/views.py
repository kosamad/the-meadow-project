from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from profiles.models import UserProfile
from django.contrib.auth.decorators import login_required
from checkout.models import Order, ProductOrderLineItem, EventOrderLineItem
from .models import Review 

# Create your views here.

@login_required
def reviews(request):
    '''All reveiws display page for admin'''     

    template = 'reviews/review.html'
    context = {        
                   
    }

    return render (request, template, context)

@login_required
def review_order(request, order_id=None):
    '''Display the leave a reveiw page'''

    profile = get_object_or_404(UserProfile, user=request.user)    
    orders = profile.orders.all() # get users orders

    # get users username and eamil for display
    username = profile.user.username

   # Check if the order belongs to the current user
    if order.user_profile.user != request.user:
        messages.error(request, "You do not have permission to review this order.")
        return redirect('home') 

    if request.method == 'POST':
        user = request.POST.get('user')        
        review_text = request.POST.get('review_text')

    # Validate form
        if not review_text:
            messages.error(request, 'Please leave a review in the box')
            context = {
                'orders':orders,        
                'username': username,                    
                'username': username,           
            }
            return render(request, 'reviews/review.html', context)
    
        review = Review(user=request.user, review_text=review_text)        
       
        review.save()
        messages.success(request, 'Your review has been successfully submitted!')
        return redirect('review_item')   
  
    template = 'reviews/review_item.html'
    context = {        
        'order':order,        
        'username': username,
        'review_text':review_text                 
    }

   
    return render (request, template, context)

