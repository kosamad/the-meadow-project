from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm, ProductOrderForm, EventOrderForm
from .models import Order, ProductOrderLineItem, EventOrderLineItem
from products.models import Product, Event, ProductVariant
from bag.contexts import bag_contents

import stripe
import json

# Create your views here.
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('shop'))    

    # Getting the bag information (Amount for stripe)
    current_bag = bag_contents(request)
    total = current_bag['grand_total']    
    stripe_total = round(total * 100) #req amount as an int
    stripe.api_key = stripe_secret_key # set secret key on stripe
    intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
  

    # General order form
    order_form = OrderForm()
    product_form = ProductOrderForm()
    event_form = EventOrderForm()
    order_type = 'product' if any(item['product_type'] == 'product' for item in bag.values()) else 'event'
    # print ( bag )
    # print( order_type)
    form = product_form if order_type == 'product' else event_form

    # Render correct product/event order form 
    if request.method == 'POST': 
        if order_type == 'product':
            form = ProductOrderForm(request.POST)
        elif order_type == 'event':
            form = EventOrderForm(request.POST)
        
        if form.is_valid():
            # Save form data to database, etc.            
            instance = form.save(commit=False)
            instance.save()
            # Redirect to success page or another view
            return redirect('order_success')
    
    # warning in case public key not set.
    if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,        
        'form': form,
        'order_type': order_type,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, template, context)

    

