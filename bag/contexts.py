from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product, Event

def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0 
    event_count = 0
    bag = request.session.get('bag', {})

    for item_id_str, quantity in bag.items():        
        try:
            product = get_object_or_404(Product, id=item_id_str)
            subtotal = quantity * product.price
            total += subtotal
            product_count += quantity
            bag_items.append({
                'item_id': item_id_str,
                'quantity': quantity,
                'product': product,
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            try:
                event = get_object_or_404(Event, id=item_id_str)
                subtotal = quantity * event.price
                total += subtotal
                event_count += quantity
                bag_items.append({
                    'item_id': item_id_str,
                    'quantity': quantity,
                    'event': event,
                    'subtotal': subtotal,
                })
            except Event.DoesNotExist:
                pass
        

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total
    
    # context is a dictionary, availiable to all templates across the application
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'event_count': event_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context