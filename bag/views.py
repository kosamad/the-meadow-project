from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal
from products.models import Product, Event, ProductVariant
import uuid



def view_bag(request):
    """ A view that renders the bag contents page """
    
    return render(request, 'bag/bag.html')



def add_product_to_bag(request, item_id):
    """ A view that adds a quantiy of a spcific product/event to the bag"""
    if request.method == 'POST':
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
        unique_key = f"{product.id}_{variant.id}_{card_message}_{note_to_seller}"
            
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
                'note_to_seller': note_to_seller,            
            }
            

        request.session['bag'] = bag
        messages.success(request, f'Added {product.friendly_name} in {variant.size} to your bag.')       
        return redirect(redirect_url)



def add_event_to_bag(request, item_id):
    """ A view that adds a quantiy of a spcific product/event to the bag"""

     # Get inputed fields from the form on the event.details page
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    product_type = request.POST.get('product_type') # i.e is it an event or a product
    event_price = request.POST.get('event_price')
    attendee_name = request.POST.get('attendee_name') 
    note_to_host = request.POST.get('note_to_host') 

    bag = request.session.get('bag',{})

    event = get_object_or_404(Event, id=item_id)    

    unique_key = f"{event.id}_{attendee_name}_{note_to_host}"
    
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




def update_card_message(request, item_id):
    """View which allows the user to ammend their card message"""

    if request.method == 'POST':
        card_message = request.POST.get('new_card_message')
        unique_key = request.POST.get('unique_key')
        variant_id = request.POST.get('variant_id')
        note_to_seller = request.POST.get('note_to_seller')    
                           
        bag = request.session.get('bag', {})

        product = get_object_or_404(Product, id=item_id)
        variant = get_object_or_404(ProductVariant, id=variant_id) 
       
        if unique_key in bag:
            # Update the card message
            bag[unique_key]['card_message'] = card_message
            # make a new unique key with the new card message and remove the old one
            new_unique_key = f"{product.id}_{variant.id}_{card_message}_{note_to_seller}"
            if new_unique_key != unique_key:
                # get rid of the old unique key and save the assign new_unique_key to it.
                bag[new_unique_key] = bag.pop(unique_key)
                unique_key = new_unique_key
                # check if it's a new unique key of if a product is being incremented
                if unique_key in bag:
                    bag[unique_key]['quantity'] += 1
            messages.success(request, "Your message was updated.")
        else:
            # in case the item isn't found in the basket.
            messages.error(request, "The item you are trying to update was not found in your bag.")

        request.session['bag'] = bag
        return redirect('view_bag')  




def update_note_to_seller(request, item_id):
    """View which allows the user to ammend the event note to seller (product)"""

    if request.method == 'POST':
        note_to_seller = request.POST.get('new_note_to_seller')
        card_message = request.POST.get('card_message')
        unique_key = request.POST.get('unique_key')
        variant_id = request.POST.get('variant_id')

        bag = request.session.get('bag', {})

        product = get_object_or_404(Product, id=item_id)
        variant = get_object_or_404(ProductVariant, id=variant_id)                        
       
        if unique_key in bag:           
            bag[unique_key]['note_to_seller'] = note_to_seller            
            new_unique_key = f"{product.id}_{variant.id}_{card_message}_{note_to_seller}"
            if new_unique_key != unique_key:
                bag[new_unique_key] = bag.pop(unique_key)
                unique_key = new_unique_key
                if unique_key in bag:
                    bag[unique_key]['quantity'] += 1
            messages.success(request, "Your message was updated.")
        else:           
            messages.error(request, "The item you are trying to update was not found in your bag.")

        request.session['bag'] = bag
        return redirect('view_bag')  




def update_quantity(request, item_id):
    """View which allows the user to ammend the event note to seller (product)"""
   
    if request.method == 'POST':
        quantity = int(request.POST.get('new_quantity'))           
        unique_key = request.POST.get('unique_key')
        variant_id = request.POST.get('variant_id')        

        bag = request.session.get('bag', {})

        product = get_object_or_404(Product, id=item_id)
        variant = get_object_or_404(ProductVariant, id=variant_id)                        
       
        if unique_key in bag:           
            bag[unique_key]['quantity'] = quantity            
            messages.success(request, "Your bag quantity was updated.")
        else:           
            messages.error(request, "The item you are trying to update was not found in your bag.")

        request.session['bag'] = bag
        return redirect('view_bag')  


   

       
def update_note_to_host(request, item_id):
    """View which allows the user to ammend the event note to host (event)"""

    if request.method == 'POST':
        note_to_host = request.POST.get('new_note_host')
        unique_key = request.POST.get('unique_key')
        attendee_name = request.POST.get('attendee_name') 
                           
        bag = request.session.get('bag', {})

        event = get_object_or_404(Event, id=item_id)        
       
        if unique_key in bag:            
            bag[unique_key]['note_to_host'] = note_to_host            
            new_unique_key = f"{event.id}_{attendee_name}_{note_to_host}"            
            if new_unique_key != unique_key:
                bag[new_unique_key] = bag.pop(unique_key)
                unique_key = new_unique_key
                if unique_key in bag:
                    bag[unique_key]['quantity'] += 1                        
            messages.success(request, "Your note was updated.")            
        else:           
            messages.error(request, "The item you are trying to update was not found in your bag.")

        request.session['bag'] = bag        
        return redirect('view_bag')
 


def remove_item(request, item_id):

    if request.method == 'POST':      
             
        unique_key = request.POST.get('unique_key')

        bag = request.session.get('bag', {})
        # remove item and defensive programming in place in case something goes wrong.
        if unique_key in bag:
            try:
                del bag[unique_key]
                request.session['bag'] = bag
                messages.success(request, "Your item was successfully removed from your bag.")
            except KeyError:
                messages.error(request, "Item with unique key not found in your bag.")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            messages.error(request, "Item with unique key not found in your bag.")         

    return redirect('view_bag')