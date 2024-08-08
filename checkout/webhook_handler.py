from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import json
import time
import stripe
from .models import Order, ProductVariant, ProductOrderLineItem, EventOrderLineItem
from products.models import Product, Event
from profiles.models import UserProfile
from django.conf import settings
from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings



class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    
    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )


    def _send_ticket_email(self, order, event_line_items):
        """Send the user an event ticket email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/ticket_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/ticket_email_body.txt',
            {'order': order, 'event_line_items': event_line_items})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )


    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)



    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """

        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info
        order_type = intent.metadata.order_type
        delivery_date_str = intent.metadata.get('delivery_date', '')
        delivery_method = intent.metadata.get('delivery_method', '')       

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
        intent.latest_charge
        )
      
        billing_details = stripe_charge.billing_details    
        shipping_details = intent.shipping or {} 
        grand_total = round(stripe_charge.amount / 100, 2)     
              
        # Clean data in the billing details       
        for field, value in billing_details.address.items():
            if value == "":                
                billing_details.address[field] = None           
                         
        # Validate and reformat delivery_date format        
        delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d').date() if delivery_date_str else None

        # Clean data in the shipping info if there is a delivery
        if delivery_method == 'delivery':
            address = shipping_details.get('address', {})
            for field, value in shipping_details.address.items():
                if value == "":
                    shipping_details.address[field] = None

        # Update Profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            # get profile
            profile = UserProfile.objects.get(user__username=username)
            if save_info:                                
                profile.default_full_name = billing_details.name
                profile.default_email = billing_details.email
                profile.phone_number = billing_details.phone                    
                profile.default_town_or_city = billing_details.address.city
                profile.default_street_address1 = billing_details.address.line1
                profile.default_street_address2 = billing_details.address.line2
                profile.default_county = billing_details.address.state
                profile.save() 
             
        # Checking if the order has alread been created in the database
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order_instance = Order.objects.get(
                    full_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,                    
                    town_or_city__iexact=billing_details.address.city,
                    street_address1__iexact=billing_details.address.line1,
                    street_address2__iexact=billing_details.address.line2,
                    county__iexact=billing_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order_instance)
            # Check and send event ticket email if event items exist
            event_line_items = order_instance.event_lineitems.all()
            if event_line_items.exists():
                self._send_ticket_email(order_instance, event_line_items)

            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order_instance  = None            
            try:
                bag_items = json.loads(bag)
                order_instance  = Order.objects.create(
                    full_name=billing_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=billing_details.phone,                    
                    postcode=billing_details.address.postal_code,
                    town_or_city=billing_details.address.city,
                    street_address1=billing_details.address.line1,
                    street_address2=billing_details.address.line2,
                    county=billing_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for unique_key, item_data in bag_items.items():
                    product_type = item_data.get('product_type')
                    # Process product items
                    if product_type == 'product':
                        item_id = unique_key.split('_')[0]
                        variant_id = item_data.get('variant_id')

                        try:
                            product = Product.objects.get(id=item_id)
                            variant = ProductVariant.objects.get(id=variant_id)
                            quantity = item_data.get('quantity', 0)
                            card_message = item_data.get('card_message', '')
                            note_to_seller = item_data.get('note_to_seller', '')

                            if delivery_method == 'pickup':
                                delivery_name = ''
                                delivery_street_address1 = ''
                                delivery_street_address2 = ''
                                delivery_town_or_city = ''
                                delivery_postcode = ''
                                delivery_county = ''
                            else:
                                # Extract delivery information from shipping_details
                                delivery_name = shipping_details.get('name', '')
                                delivery_street_address1 = shipping_details.address.line1
                                delivery_street_address2 = shipping_details.address.line2
                                delivery_town_or_city = shipping_details.address.city
                                delivery_postcode = shipping_details.address.postal_code
                                delivery_county = shipping_details.address.state                        
                                
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
                            order_line_item.save()

                        except Product.DoesNotExist or ProductVariant.DoesNotExist:
                            # Handle missing product or variant
                            pass

                    elif product_type == 'event':
                        item_id = unique_key.split('_')[0]

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
                            order_line_item.save()
                        except Event.DoesNotExist:
                            # Handle missing event
                            pass     
                    else:
                        print ('the order type is not being set correclty')     
            except Exception as e:
                if order_instance:
                    order_instance.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_confirmation_email(order_instance)
        # Send event ticket email if event items exist
        if event_line_items.exists():
            self._send_ticket_email(order_instance, event_line_items)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)



    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)