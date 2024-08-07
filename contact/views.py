from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from checkout.models import Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from profiles.models import UserProfile

# Create your views here.


# Contact form code inspired by (but adapted from) Codemy.com YouTube video series https://www.youtube.com/watch?v=xNqnHmXIuzU
def contact(request):
    """ A view to return the index page """

    orders = []    

    if request.user.is_authenticated:       
        profile = get_object_or_404(UserProfile, user=request.user)
        orders = profile.orders.all()  # Retrieve user's orders for optional selection       
       
    if request.method == 'POST':
        message_name = request.POST.get('message-name')
        message_email = request.POST.get('message-email')
        message = request.POST.get('message')
        order_number = request.POST.get('order-number', '')  # Default to empty if not provided as this is optional

        #  Validating form and ensures all parts are presnt
        if not message_name or not message_email or not message:
            messages.error(request, 'Please fill in all fields.')
            context = {
                'orders': orders,               
            }
            return render(request, 'contact/contact.html', context)

        # send email
        send_mail(
            subject=f'Contact form message from {message_name}',  # subject
            message=message,  # message
            from_email=message_email,  # from email
            recipient_list=['themeadowproj@gmail.com'],             
        )        

        messages.success(request, 'Your email has been sent successfully!')
        return redirect('contact')   

    context = {
        'orders': orders,        
        }     

    return render(request, 'contact/contact.html', context)


