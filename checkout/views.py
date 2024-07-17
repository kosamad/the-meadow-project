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

    if request.method == 'POST':
        bag = request.session.get('bag', {})
        general_form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],            
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        product_form_data = {                       
            'delivery_method': request.POST['delivery_method'],
            'delivery_date': request.POST['delivery_date'],
            'delivery_name': request.POST['delivery_name'],
            'delivery_street_address1': request.POST['delivery_street_address1'],
            'delivery_street_address2': request.POST['delivery_street_address2'],
            'delivery_town_or_city': request.POST['delivery_town_or_city'],
            'delivery_postcode': request.POST['delivery_postcode'],
            'delivery_county': request.POST['delivery_county'],
        }

        
        event_form_data = {            
            }

        # Determine order type based on form data or hidden field
        order_type = request.POST.get('order_type')

        # Initialise forms
        order_form = OrderForm(general_form_data)        
        product_form = ProductOrderForm(product_form_data)
        event_form = EventOrderForm(event_form_data)

        if order_form.is_valid():
            order_instance = order_form.save(commit=False)
            order_instance.save()
        # Validate and save form based on order_type
            if 'product' in request.POST.get('order_type'):
                if product_form.is_valid():
                    product_instance = product_form.save(commit=False)
                    product_instance.order = order_instance
                    product_instance.save()
            if 'event' in request.POST.get('order_type'):
                if event_form.is_valid():
                    event_instance = event_form.save(commit=False)
                    event_instance.order = order_instance
                    event_instance.save()

            for unique_key, details in bag.items():
                try:                                             
                    if details['product_type'] == 'product':
                        item_id, variant_id, _, _ = unique_key.split('_', 3) # split my unique key to get id's 
                        product = get_object_or_404(Product, id=item_id)
                        variant = get_object_or_404(ProductVariant, id=variant_id)
                        quantity = details.get('quantity', 0)
                        card_message = details.get('card_message', '')
                        note_to_seller=details.get('note_to_seller', ''),
                        order_line_item = ProductOrderLineItem(
                            order=order_instance,
                            product=product,
                            product_variant=variant,
                            quantity=quantity,
                            delivery_method=details.get('delivery_method'),
                            delivery_date=details.get('delivery_date'),
                            delivery_name=details.get('delivery_name'),
                            delivery_street_address1=details.get('delivery_street_address1'),
                            delivery_street_address2=details.get('delivery_street_address2'),
                            delivery_town_or_city=details.get('delivery_town_or_city'),
                            delivery_postcode=details.get('delivery_postcode'),
                            delivery_county=details.get('delivery_county'),
                            card_message=card_message,
                            note_to_seller=note_to_seller
                        )                        
                        order_line_item.save()

                    elif details['product_type'] == 'event':
                        item_id, _, _= unique_key.split('_', 3)
                        event = get_object_or_404(Event, id=item_id)
                        quantity = details.get('quantity', 0)
                        note_to_host = details.get('note_to_host', '')
                        attendee_name = details.get('attendee_name', '')
                        order_line_item = EventOrderLineItem(
                            order=order_instance,
                            event=event,
                            quantity=quantity,
                            note_to_host=note_to_host,
                            attendee_name=attendee_name,                       
                        )
                        order_line_item.save()
                # exception if product or even not found
                except Exception as e:                    
                    messages.error(request, "One of the items in your basket wasn't found in our database. \
                        Please call us for assistance!")
                    order.delete()
                    return redirect(reverse('view_bag'))
                                     
            # Save the info to the user's profile if they checked the box
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order_instance.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

            

    else:
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

        # Determine order type based on bag contents      
        has_product = any(item['product_type'] == 'product' for item in bag.values())
        has_event = any(item['product_type'] == 'event' for item in bag.values())

        if has_product and has_event:
            order_type = 'product and event'
        elif has_product:
            order_type = 'product'
        elif has_event:
            order_type = 'event'
        else:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('shop'))

        # Initialise product and event forms for rendering
        if order_type == 'product':
            order_form = OrderForm()
            product_form = ProductOrderForm()
            event_form = None
        elif order_type == 'event':
            order_form = OrderForm()
            product_form = None
            event_form = EventOrderForm()
        elif order_type == 'product and event':
            order_form = OrderForm()
            product_form = ProductOrderForm()
            event_form = EventOrderForm()


    
    print ( bag )
    print( order_type)
    # form = product_form if order_type == 'product' else event_form          
       
    
    # warning in case public key not set.
    if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,        
        'product_form': product_form,
        'event_form': event_form,
        'order_type': order_type,       
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, template, context)

    

