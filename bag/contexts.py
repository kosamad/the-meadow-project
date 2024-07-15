from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product, Event, ProductVariant


def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    event_count = 0
    total_items = 0
    bag = request.session.get('bag', {})  
   
    for unique_key, details in bag.items():
        try:            
            if details['product_type'] == 'product':
                item_id, variant_id, _, _ = unique_key.split('_', 3) # split my unique key to get id's 
                product = get_object_or_404(Product, id=item_id)
                variant = get_object_or_404(ProductVariant, id=variant_id)
                subtotal = details['quantity'] * Decimal(details['price'])
                total += subtotal
                product_count += details['quantity']
                
                bag_items.append({
                    'item_id': item_id,
                    'quantity': details['quantity'],
                    'product': product,
                    'variant': variant,
                    'subtotal': subtotal,
                    'card_message': details.get('card_message', ''), # if no input, it's set to an empty string so no errors
                    'note_to_seller': details.get('note_to_seller', ''),
                    'unique_key': unique_key, 
                    'variant_id': variant.id, 
                })

            elif details['product_type'] == 'event':
                item_id, _, _= unique_key.split('_', 3)
                event = get_object_or_404(Event, id=item_id)
                subtotal = details['quantity'] * Decimal(details['price'])
                total += subtotal
                event_count += details['quantity']
                bag_items.append({
                    'item_id': item_id,
                    'quantity': details['quantity'],
                    'event': event,                
                    'subtotal': subtotal,                   
                    'attendee_name': details.get('attendee_name',''),
                    'note_to_host': details.get('note_to_host',''),
                    'unique_key': unique_key,                                          
                })          
        except (Product.DoesNotExist, Event.DoesNotExist, ProductVariant.DoesNotExist):
            pass

    # Sort the bag to ensure it keeps a consitent format when bag items are edited.
    bag_items.sort(key=lambda x: str(x['item_id']))

    # Delivery costs    
    # No delivery charge for event items as are emailed
    if event_count > 0:
        delivery = 0  
        free_delivery_delta = 0

    # product delivery
    else:
        if total < settings.FREE_DELIVERY_THRESHOLD:
            delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
            free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
        else:
            delivery = 0
            free_delivery_delta = 0  

    grand_total = delivery + total
    total_items = product_count + event_count

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'event_count': event_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
        'total_items': total_items,
    }

    return context





# def bag_contents(request):
#     bag_items = []
#     total = 0
#     product_count = 0 
#     # event_count = 0
#     bag = request.session.get('bag', {})

#     # for item_id_str, quantity in bag.items():        
#     #     try:
#     #         product = get_object_or_404(Product, id=item_id_str)
#     #         subtotal = quantity * product.price
#     #         total += subtotal
#     #         product_count += quantity
#     #         bag_items.append({
#     #             'item_id': item_id_str,
#     #             'quantity': quantity,
#     #             'product': product,
#     #             'subtotal': subtotal,
#     #         })
#     #     except Product.DoesNotExist:
#     #         try:
#     #             event = get_object_or_404(Event, id=item_id_str)
#     #             subtotal = quantity * event.price
#     #             total += subtotal
#     #             event_count += quantity
#     #             bag_items.append({
#     #                 'item_id': item_id_str,
#     #                 'quantity': quantity,
#     #                 'event': event,
#     #                 'subtotal': subtotal,
#     #             })
#     #         except Event.DoesNotExist:
#     #             pass
        

#     if total < settings.FREE_DELIVERY_THRESHOLD:
#         delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
#         free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
#     else:
#         delivery = 0
#         free_delivery_delta = 0
    
#     grand_total = delivery + total
    
#     # context is a dictionary, availiable to all templates across the application
#     context = {
#         'bag_items': bag_items,
#         'total': total,
#         'product_count': product_count,
#         # 'event_count': event_count,
#         'delivery': delivery,
#         'free_delivery_delta': free_delivery_delta,
#         'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
#         'grand_total': grand_total,
#     }

#     return context