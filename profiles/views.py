from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib import messages

# Create your views here.

def profile(request):
    '''Display the Users profile'''

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance = profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
    else:
        form = UserProfileForm(instance=profile)

    form = UserProfileForm(instance=profile) # user default info
    orders = profile.orders.all() # get users orders

    # get users username and eamil for display
    username = profile.user.username 
    email = profile.user.email

    template = 'profiles/profile.html'
    context = {
        'form':form,
        'orders':orders,
        'username': username,
        'email': email,        
    }

    return render (request, template, context)