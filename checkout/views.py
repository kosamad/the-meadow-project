from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages

from .forms import OrderForm, ProductOrderForm, EventOrderForm
from .models import Order, ProductOrderLineItem, EventOrderLineItem
from products.models import Product, Event, ProductVariant

# Create your views here.
def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('shop'))    

    # General order form 
    order_form = OrderForm()
    product_form = ProductOrderForm()
    event_form = EventOrderForm()
    order_type = 'product' if 'product' in bag else 'event'

    # Render correct product/event order form 
    if request.method == 'POST': 
        if order_type == 'product':
            form = ProductOrderForm(request.POST)
        elif order_type == 'event':
            form = EventOrderForm(request.POST)
        
        if form.is_valid():
            # Save form data to database, etc.
            form.save()
            # Redirect to success page or another view
            return redirect('order_success')
    
    
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,        
        'form': form,
        'order_type': order_type,
    }
    return render(request, template, context)

    

