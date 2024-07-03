from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Event


def product_detail(request, product_id):
    """ A view to show the product details for an individual item """
    product = get_object_or_404(Product, pk=product_id)    

    context = {
        'product': product,        
    }
    return render(request, 'products/product_detail.html', context)



def event_detail(request, event_id):
    """ A view to show the event details for an individual item """    
    event = get_object_or_404(Event, pk=event_id)
    context = {
        'event': event,
    }
    return render(request, 'products/event_detail.html', context)



