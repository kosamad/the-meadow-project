from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Event, ProductVariant


def product_detail(request, product_uuid):
    """ A view to show the product details for an individual item """

    product = get_object_or_404(Product, id=product_uuid) # id=product_id I am using UUID
    variants = ProductVariant.objects.filter(product=product)
    default_variant = variants.filter(size='M').first() or variants.first()
    default_price = default_variant.price if default_variant else None

    context = {
        'product': product,
        'variants': variants,
        'default_price': default_price,
        'default_variant_id': default_variant.id if default_variant else None,
    }
    return render(request, 'products/product_detail.html', context)



def event_detail(request, event_uuid):
    """ A view to show the event details for an individual item """ 

    event = get_object_or_404(Event, id=event_uuid)
    context = {
        'event': event,
    }
    return render(request, 'events/event_detail.html', context)


