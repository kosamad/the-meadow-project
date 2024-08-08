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
        self.fields['name'].help_text = 'This should be set like this example ada_bouquet for Ada Bouquet friendly name'
        self.fields['price'].help_text = 'Set the price of the product. Set this to the price of a medium size.'
        self.fields['alt_text'].help_text = 'Describe the image'
        self.fields['is_active'].help_text = 'Checked if the product is avaliable'    



class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['size', 'price', 'is_active']

    def __init__(self, *args, **kwargs):
        # Extract the is_edit flag from kwargs if available
        is_edit = kwargs.pop('is_edit', False)
        
        super().__init__(*args, **kwargs)
        
        # Make the size field read-only if in edit mode
        if is_edit:
            self.fields['size'].disabled = True
   
