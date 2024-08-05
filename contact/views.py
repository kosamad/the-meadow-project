from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from products.models import Product, Event


def contact(request):
    """ A view to return the index page """

    return render(request, 'contact/contact.html')