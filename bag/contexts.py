''' Contexts for bag required across the application '''

from decimal import Decimal
from django.conf import settings

from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context



# def bag_contents(request):

#     bag_items = []
#     total = Decimal('0.00')
#     product_count = 0
#     # Get shopping bag (or empty dictionary if absent)
#     bag = request.session.get('bag',{})

#     for item_id, item_data in bag.items():
#         print(f"Item ID: {item_id}")
#         item_components = item_id.split('_')
#         print(f"Item Components: {item_components}")
#         product_id = item_components[0]
#         size = item_components[1]
#         optional_card_message = item_components[2]
#         note_to_seller = item_components[3]
#         selected_size_price = item_data['selected_size_price']
#         quantity = item_data['quantity']

#         product = get_object_or_404(Product, pk=product_id)
#         total += quantity * Decimal(selected_size_price)
#         product_count += quantity
#         bag_items.append({
#             'item_id': item_id,
#             'quantity': quantity,
#             'product': product,
#             'selected_size_price': selected_size_price,
#         }) 

#     if total < settings.FREE_DELIVERY_THRESHOLD:
#         delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE/ 100)
#         free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
#     else:
#         delivery = 0
#         free_delivery_delta = 0

#     grand_total = delivery + total

#     context = {
#         'bag_items': bag_items,
#         'total': total,
#         'product_count': product_count,
#         'delivery': delivery,
#         'free_delivery_delta': free_delivery_delta,
#         'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
#         'standard_delivery_percentage': settings.STANDARD_DELIVERY_PERCENTAGE,
#         'grand_total': grand_total,}

#     return context