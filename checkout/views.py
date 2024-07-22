from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist

from .forms import OrderForm, ProductOrderForm
from .models import Order, ProductOrderLineItem, EventOrderLineItem
from products.models import Product, Event, ProductVariant
from bag.contexts import bag_contents

import stripe
import json

# check if user has requested to save their data
@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0] # payment intent id
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})
        print("Bag contents:", bag)

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

        # Product form data only if it's a product order (prevents Event errors)
        product_form_data = {}
        if 'product' in request.POST.get('order_type', ''):
            product_form_data = {
                'delivery_method': request.POST.get('delivery_method'),
                'delivery_date': request.POST.get('delivery_date'),
                'delivery_name': request.POST.get('delivery_name'),
                'delivery_street_address1': request.POST.get('delivery_street_address1'),
                'delivery_street_address2': request.POST.get('delivery_street_address2'),
                'delivery_town_or_city': request.POST.get('delivery_town_or_city'),
                'delivery_postcode': request.POST.get('delivery_postcode'),
                'delivery_county': request.POST.get('delivery_county'),
            }
            print("Product form data:", product_form_data)

        order_type = request.POST.get('order_type')
        order_form = OrderForm(general_form_data)
        product_form = ProductOrderForm(product_form_data) if 'product' in order_type else None

        print("Order Type:", order_type)

        if order_form.is_valid():
            order_instance = order_form.save(commit=False)
            print("General Order form is valid.")
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid             
            order.original_bag = json.dumps(bag)                          
            try:
                order_instance.save()
                print("Processing bag contents")

                if product_form and not product_form.is_valid():
                    messages.error(request, "There was an error with the product form. Please double-check your information.")
                    order_instance.delete() # Clean up partially saved order.
                    return redirect(reverse('view_bag'))          

                for unique_key, item_data in bag.items():
                    print(f"Processing item: {unique_key} with data: {item_data}")                                       
                    product_type = item_data.get('product_type')

                    # Product only processing    
                    if product_type == 'product':
                        item_id = unique_key.split('_')[0]
                        variant_id = item_data.get('variant_id')
                        print("Product ID:", item_id)
                        print("Variant ID:", variant_id)

                        # Exception handling for Product and ProductVariant to prevent double save error
                        try:
                            product = Product.objects.get(id=item_id)
                            variant = ProductVariant.objects.get(id=variant_id)
                            quantity = item_data.get('quantity', 0)
                            card_message = item_data.get('card_message', '')
                            note_to_seller = item_data.get('note_to_seller', '')
                            delivery_method = request.POST.get('delivery_method')
                            delivery_date = request.POST.get('delivery_date')
                            delivery_name = request.POST.get('delivery_name')
                            delivery_street_address1 = request.POST.get('delivery_street_address1')
                            delivery_street_address2 = request.POST.get('delivery_street_address2')
                            delivery_town_or_city = request.POST.get('delivery_town_or_city')
                            delivery_postcode = request.POST.get('delivery_postcode')
                            delivery_county = request.POST.get('delivery_county')
                            print("Product:", product)
                            print("Variant:", variant)
                            print(f"Creating ProductOrderLineItem with product: {product}, variant: {variant}, quantity: {quantity}")

                            order_line_item = ProductOrderLineItem(
                                order=order_instance,
                                product=product,
                                product_variant=variant,
                                quantity=quantity,
                                delivery_method=delivery_method,
                                delivery_date=delivery_date,
                                delivery_name=delivery_name,
                                delivery_street_address1=delivery_street_address1,
                                delivery_street_address2=delivery_street_address2,
                                delivery_town_or_city=delivery_town_or_city,
                                delivery_postcode=delivery_postcode,
                                delivery_county=delivery_county,
                                card_message=card_message,
                                note_to_seller=note_to_seller
                            )
                            print(f"Delivery Method: {order_line_item.delivery_method}")
                            print(f"Delivery Date: {order_line_item.delivery_date}")
                            print(f"Saving ProductOrderLineItem: {order_line_item}")
                            order_line_item.save()
                            print('Product order line item saved')

                        except ObjectDoesNotExist as e:
                            print(f"Product or ProductVariant not found and skipped: {e}")                                                             
                            

                    elif product_type == 'event':
                        item_id = unique_key.split('_')[0]                           
                        # Exception handling for Event
                        try:
                            event = Event.objects.get(id=item_id)
                            quantity = item_data.get('quantity', 0)
                            note_to_host = item_data.get('note_to_host', '')
                            attendee_name = item_data.get('attendee_name', '')

                            order_line_item = EventOrderLineItem(
                                order=order_instance,
                                event=event,
                                quantity=quantity,
                                note_to_host=note_to_host,
                                attendee_name=attendee_name,
                            )
                            print(f"Saving EventOrderLineItem: {order_line_item}")
                            order_line_item.save()
                            print('Event order line item saved')

                        except ObjectDoesNotExist as e:
                            print(f"Event not found: {e}")                                      

                # save user profile info if they checked the box
                request.session['save_info'] = 'save-info' in request.POST
                return redirect(reverse('checkout_success', args=[order_instance.order_number]))

            except Exception as e:
                print(f"Error saving order: {e}")
                messages.error(request, f"There was an error processing your order. Please try again. Error: {e}")
                order_instance.delete()
                return redirect(reverse('view_bag'))

        else:
            print("Order form is not valid.")
            print(order_form.errors)
            messages.error(request, 'There was an error with your form. Please double check your information.')
            messages.error(request, f'Order form errors: {order_form.errors}')

    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('shop'))

        # Getting the bag information (Amount for stripe)
        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)  # Amount for Stripe in cents
        stripe.api_key = stripe_secret_key
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
        order_form = OrderForm()
        product_form = ProductOrderForm() if has_product else None        

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'product_form': product_form,           
            'order_type': order_type,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }
        return render(request, template, context)


def checkout_success(request, order_number):
    """
    View to handle successful checkouts
    """

    save_info = request.session.get('save_info') # for user profile
    order = get_object_or_404(Order, order_number=order_number) # get order number and send to view
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    # Delete bag   
    if 'bag' in request.session:
        del request.session['bag']  

   
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'product_lineitems': order.product_lineitems.all(),
        'event_lineitems': order.event_lineitems.all(),
    }

    return render(request, template, context)