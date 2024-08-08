from django import forms
from .models import Product, Event, Category, ProductVariant
from django.forms.widgets import DateTimeInput
from django.core.exceptions import ValidationError



class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['category', 'name', 'friendly_name','price', 'description', 'image', 'alt_text', 'is_gift_card', 'is_active'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # All categoried apart from event
        categories = Category.objects.exclude(name__iexact='event')
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names

        # Add helper text
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
        self.product = kwargs.pop('product', None)
        
        super().__init__(*args, **kwargs)
        
        # Make the size field read-only if in edit mode
        if is_edit:
            self.fields['size'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        size = cleaned_data.get('size')
        
        if self.product and size:
            # Check if the variant with the same size already exists for the product
            if ProductVariant.objects.filter(product=self.product, size=size).exists():
                raise ValidationError(f"A variant with size '{size}' already exists for this product.")

        return cleaned_data



class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = [
            'category', 'name', 'friendly_name','event_datetime',
            'duration_hours', 'price', 'description', 'image','alt_text',
            'is_active',
        ]
        widgets = {
            'event_datetime': DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Limit category choices to only the "Event" category and preselect
        try:
            event_category = Category.objects.get(name__iexact='event')
            self.fields['category'].queryset = Category.objects.filter(id=event_category.id)
            self.fields['category'].initial = event_category.id 
        except Category.DoesNotExist:
            # Handle the case where the event category is not found
            self.fields['category'].queryset = Category.objects.none()  # No options available if event category is missing
            messages.error(None, "Event category not found. Please add an event category to proceed.")         

        # Add helper text 
        self.fields['name'].help_text = 'This should be set like this example ada_bouquet for Ada Bouquet friendly name'        
        self.fields['alt_text'].help_text = 'Describe the image'
        self.fields['image'].help_text = 'For our events, horizontal images work best' 
        self.fields['is_active'].help_text = 'Checked if the event is avaliable/there are tickets' 
