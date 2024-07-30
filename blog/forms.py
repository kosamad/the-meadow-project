from django import forms
from .models import Post
from products.models import Product, Event
from django_summernote.widgets import SummernoteWidget


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
            'image': forms.ClearableFileInput,        
            'body': SummernoteWidget(),
        }       
        product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs={'placeholder': 'Select a product'}))
        event = forms.ModelChoiceField(queryset=Event.objects.all(), widget=forms.Select(attrs={'placeholder': 'Select an event'}))
 

