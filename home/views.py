from django.shortcuts import render
from products.models import Product, Event
from reviews.models import Review


def index(request):
    """ A view to return the index page """

    # Get reveiws
    reviews = Review.objects.all()

    context = {
        'reviews': reviews,
    }

    return render(request, 'home/index.html', context)
