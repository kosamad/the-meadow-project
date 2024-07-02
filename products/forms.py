from django import forms
from .models import Product
from datetime import datetime


class ProductOrderForm(forms.Form):

    DELIVERY_CHOICES = [
        ('delivery', 'Delivery'),
        ('store_pickup', 'Store Pickup'),
    ]

    size = forms.ChoiceField(
        choices=Product.SIZE_CHOICES,
        initial='M',
        widget=forms.Select(attrs={'class': 'form-control'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.now().date()}))
    delivery_option = forms.ChoiceField(
        choices=DELIVERY_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'delivery-option'}))
    optional_card_message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False
    )
    note_to_seller=forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False
    )
    quantity=forms.IntegerField(initial=1, min_value=1)
    selected_size_price = forms.DecimalField(widget=forms.HiddenInput())    