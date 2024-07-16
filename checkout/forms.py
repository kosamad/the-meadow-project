from django import forms
from .models import Order, ProductOrderLineItem, EventOrderLineItem

DELIVERY_CHOICES = [
    ('delivery', 'Delivery'),
    ('pickup', 'Shop Pickup'),
]

class OrderForm(forms.ModelForm):   

    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'county',
                  )


    def __init__(self, *args, **kwargs):
        """
        Add placeholders for form boxes and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)       
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',           
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:            
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False

    

# Product and or Event Specific order form
class ProductOrderForm(forms.ModelForm):
    delivery_method = forms.ChoiceField(choices=DELIVERY_CHOICES, widget=forms.RadioSelect)
    delivery_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = ProductOrderLineItem
        fields = ('product', 'product_variant', 'quantity', 'delivery_method', 'delivery_name', 'delivery_date',
                  'delivery_street_address1', 'delivery_street_address2', 'delivery_town_or_city',
                  'delivery_postcode', 'delivery_county')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery_method'].required = True
        self.fields['delivery_date'].required = True

        placeholders = {
            'product': 'Product',
            'product_variant': 'Variant',
            'quantity': 'Quantity',            
            'delivery_method': 'Delivery Method',
            'delivery_date': 'Delivery/Pick Up Date',
            'delivery_name': 'Delivery Recipient',
            'delivery_street_address1': 'Delivery Street Address 1',
            'delivery_street_address2': 'Delivery Street Address 2',
            'delivery_town_or_city': 'Delivery Town or City',
            'delivery_postcode': 'Delivery Postal Code',
            'delivery_county': 'Delivery County'
        }

        self.fields['delivery_date'].widget.attrs['autofocus'] = True

        for field in self.fields:            
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False

# Event Specific order form
class EventOrderForm(forms.ModelForm):
    class Meta:
        model = EventOrderLineItem
        fields = ('event', 'quantity')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        

        placeholders = {
            'event': 'Event',
            'quantity': 'Quantity',
        }

        for field in self.fields:            
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False