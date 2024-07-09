from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, Event, ProductVariant

# Create your views here.
def view_bag(request):
    """ A view that renders the bag contents page """
    
    return render(request, 'bag/bag.html')



def add_product_to_bag(request, item_id):
    """ A view that adds a quantiy of a spcific product/event to the bag"""
    # Get inputed fields from the form on the product.details page
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    product_type = request.POST.get('product_type') # i.e is it an event or a product
    variant_id = request.POST.get('variant_id')
    card_message = request.POST.get('card_message')
    note_to_seller = request.POST.get('note_to_seller')
    
    # Retrieve or create the bag in the session
    bag = request.session.get('bag',{})
    
    # Get product and varient id's
    product = get_object_or_404(Product, id=item_id)
    item_id_str = str(product.id)  # Convert item_id (UUID) to string before using it as a key
    variant = get_object_or_404(ProductVariant, id=variant_id)
        
    if item_id_str in bag and variant in bag :
        bag[item_id_str]['quantity'] += quantity
    else:
        bag[item_id_str] = {
            'quantity': quantity,
            'product_type': product_type,
            'variant_id': variant_id,
            'price': str(variant.price), # decimal fields must be converted to a string before JSON use
            'size': variant.size,
            'card_message': card_message,
            'note_to_seller': note_to_seller
        }

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)



def add_event_to_bag(request, item_id):
    """ A view that adds a quantiy of a spcific product/event to the bag"""

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    product_type = request.POST.get('product_type') # i.e is it an event or a product

    bag = request.session.get('bag',{})

    event = get_object_or_404(Event, id=item_id)
    item_id_str = str(event.id)
    
    if item_id_str in bag:
        bag[item_id_str]['quantity'] += quantity
    else:
        bag[item_id_str] = {
            'quantity': quantity, 
            'product_type': product_type
            }

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)


# def add_to_bag(request, item_id):
#     """ A view that adds a quantiy of a spcific product/event to the bag"""

#     quantity = int(request.POST.get('quantity'))
#     redirect_url = request.POST.get('redirect_url')
#     product_type = request.POST.get('product_type') # i.e is it an event or a product

#     bag = request.session.get('bag',{})

#     # Convert item_id (UUID) to string before using it as a key and check if its' a product or event
#     if product_type == 'product':
#         product = get_object_or_404(Product, id=item_id)
#         item_id_str = str(product.id)
#     # elif product_type == 'event':
#     #     event = get_object_or_404(Event, id=item_id)
#     #     item_id_str = str(event.id)
    
#     if item_id_str in bag:
#         bag[item_id_str] += quantity
#     else:
#         bag[item_id_str] = quantity

#     request.session['bag'] = bag
#     print(request.session['bag'])
#     return redirect(redirect_url)


# note: Ensure that wherever you retrieve items from the bag session dictionary, you consistently use string keys (e.g., str(item_id)) to access or modify items.



def clear_basket(request):
    if 'bag' in request.session:
        del request.session['bag']
    return redirect('shop')