from django.shortcuts import render, redirect, get_object_or_404
import hashlib
from decimal import Decimal
from products.models import Product, Event, ProductVariant



def view_bag(request):
    """ A view that renders the bag contents page """
    
    return render(request, 'bag/bag.html')



def hash_text(text):
    """Function to create a hash of the text (card message/note_to_seller) for uniqueness."""

    return hashlib.sha256(text.encode()).hexdigest()



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
    # item_id_str = str(product.id)  # Convert item_id (UUID) to string before using it as a key
    variant = get_object_or_404(ProductVariant, id=variant_id)

    # Create a unique key for the bag item
    unique_key = f"{product.id}_{variant.id}_{hash_text(card_message)}_{hash_text(note_to_seller)}"
        
    if unique_key in bag :
        bag[unique_key]['quantity'] += quantity
    else:
        bag[unique_key] = {
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

     # Get inputed fields from the form on the event.details page
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    product_type = request.POST.get('product_type') # i.e is it an event or a product
    event_price = request.POST.get('event_price')
    attendee_name = request.POST.get('attendee_name', '') 
    note_to_host = request.POST.get('note_to_host', '') 

    bag = request.session.get('bag',{})

    event = get_object_or_404(Event, id=item_id)    

    unique_key = f"{event.id}_{hash_text(attendee_name)}_{hash_text(note_to_host)}"
    
    if unique_key in bag:
        bag[unique_key]['quantity'] += quantity
    else:
        bag[unique_key] = {
            'quantity': quantity, 
            'product_type': product_type,
            'price': event_price,
            'attendee_name': attendee_name,
            'note_to_host': note_to_host,
            }

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)



def clear_basket(request):
    if 'bag' in request.session:
        del request.session['bag']
    return redirect('shop')




def update_card_message(request, item_id):
    """View which allows the user to ammend their card message"""

    if request.method == 'POST':
        new_card_message = request.POST.get('card_message')
        bag = request.session.get('bag', {})

        for unique_key, details in bag.items():
            if details.get('item_id') == item_id:
                details['card_message'] = new_card_message
                # Update the unique_key with the new card_message hash
                details['unique_key'] = f"{details['product_id']}_{details['variant_id']}_{hash_text(new_card_message)}_{hash_text(details['note_to_seller'])}"
                break

        request.session['bag'] = bag
        return redirect('view_bag')

    return HttpResponseBadRequest("Bad request") 
    
 