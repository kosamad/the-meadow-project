from django import forms
from .models import Product, Event, Category, ProductVariant
from django.forms import inlineformset_factory




class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['category', 'name', 'friendly_name','price', 'description', 'image', 'alt_text', 'is_gift_card', 'is_active'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names

        # Add helper text to the 'price' field
        self.fields['price'].help_text = 'Set the price of the product. Set this to the price of a medium size.'     



class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['size', 'price', 'is_active']

