from django import forms
from .models import Post
from products.models import Product, Event
from django_summernote.widgets import SummernoteWidget
from .widgets import CustomClearableFileInput
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError



class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'image', 'alt_text',
                  'product', 'event',
                  'body'
                  )
        widgets = {
            'alt_text': forms.TextInput(attrs={'placeholder':'Add descriptive text for your image'}),
            'title': forms.TextInput,
            'image': CustomClearableFileInput,        
            'body': SummernoteWidget(),
            'product': forms.Select(attrs={'placeholder': 'Select a product'}),
            'event': forms.Select(attrs={'placeholder': 'Select an event'}),        
            }

    # Custom validation for the body field
    def clean_body(self):
        body = self.cleaned_data.get('body', '')

        # Use BeautifulSoup to remove HTML tags
        soup = BeautifulSoup(body, "html.parser")
        plain_text = soup.get_text(strip=True)

        # Check if the remaining text is empty or contains only whitespace
        if not plain_text:
            raise ValidationError("The body cannot be empty or contain only whitespace.")
        return body

    
          
     
 

