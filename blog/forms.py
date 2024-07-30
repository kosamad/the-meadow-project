from django import forms
from .models import Post
from products.models import Product, Event


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
            'body': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your blog post here...'}),
        }

        product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs={'placeholder': 'Select a product'}))
        event = forms.ModelChoiceField(queryset=Event.objects.all(), widget=forms.Select(attrs={'placeholder': 'Select an event'}))
 

