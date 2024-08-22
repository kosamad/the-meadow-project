from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from checkout.models import Order



# Create your views here.
@login_required
def profile(request):
    '''Display the Users profile'''

    profile = get_object_or_404(UserProfile, user=request.user)    

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
    
    orders = profile.orders.all().order_by('-date')  # get users orders

    # get users username and eamil for display
    username = profile.user.username 
    email = profile.user.email

    template = 'profiles/profile.html'
    context = {
        'form':form,
        'orders':orders,
        'on_profile_page': True,
        'username': username,
        'email': email,        
    }

    return render (request, template, context)

@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    # get products and events
    product_lineitems = order.product_lineitems.all()
    event_lineitems = order.event_lineitems.all()

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'product_lineitems': product_lineitems,
        'event_lineitems': event_lineitems,
        'from_profile': True,
    }

    return render(request, template, context)