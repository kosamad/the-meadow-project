import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.utils import timezone
from .validators import validate_date

from products.models import Product, ProductVariant, Event
from profiles.models import UserProfile

DELIVERY_CHOICES = [
    ('delivery', 'Delivery'),
    ('pickup', 'Shop Pickup'),
]


# Create your models here.
class Order(models.Model):

    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                        null=True, blank = True, related_name = 'orders' )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)    
    postcode = models.CharField(max_length=20, null=False, blank=False)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    
    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()



    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs and differences between events and products.
        """
        product_total = self.product_lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0   
        event_total = self.event_lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.order_total = product_total + event_total
        
        # Calculate delivery cost based on order items
        event_items = self.event_lineitems.all()
        product_items = self.product_lineitems.all()
        
        if self.event_lineitems.exists():
            self.delivery_cost = 0  # Free delivery for events
        elif self.product_lineitems.exists() and self.order_total < Decimal(settings.FREE_DELIVERY_THRESHOLD):
            self.delivery_cost = self.order_total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        else:
            self.delivery_cost = 0
        
        self.grand_total = self.order_total + self.delivery_cost
        self.save()



    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)


    def __str__(self):
        """
        Resturn order number
        """
        return self.order_number



class ProductOrderLineItem(models.Model):
    """
    For Products and/or Events if together in the basket
    """
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='product_lineitems')
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)    
    product_variant = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.SET_NULL)
    card_message = models.TextField(blank=True, default='')
    note_to_seller = models.TextField(blank=True, default='')    
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)
    # delivery details   
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True, validators=[validate_date])
    delivery_name = models.CharField(max_length=20, null=True, blank=True)
    delivery_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    delivery_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    delivery_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    delivery_postcode = models.CharField(max_length=20, null=True, blank=True)
    delivery_county = models.CharField(max_length=80, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        print(f"111Saving ProductOrderLineItem for product {self.product} and variant {self.product_variant}")
        if self.product:
            if self.product_variant:
                self.lineitem_total = self.product_variant.price * self.quantity
            else:
                self.lineitem_total = self.product.price * self.quantity
        else:
            print("Error: Product is missing, setting lineitem_total to 0") #prevents error from 111Saving ProductOrderLineItem for product None and variant None 
            self.lineitem_total = 0

        super().save(*args, **kwargs)
        self.order.update_total()
        print("111ProductOrderLineItem saved and order total updated")

    def __str__(self):
        return f'Name: {self.product.friendly_name} on Order number: {self.order.order_number}'
       


class EventOrderLineItem(models.Model):
    """
    For Event only orders
    """
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='event_lineitems')
    event = models.ForeignKey(Event, null=False, blank=False, on_delete=models.CASCADE)
    note_to_host = models.TextField(blank=True, default='')
    attendee_name = models.CharField(max_length=80, blank=True, default='')
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False,)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        if self.event:     
            self.lineitem_total = self.event.price * self.quantity
        else:
            raise ValueError("Event is required to calculate line item total")

        super().save(*args, **kwargs)
        self.order.update_total()

    def __str__(self):
        return f'Name: {self.event.friendly_name} on Order number: {self.order.order_number}'