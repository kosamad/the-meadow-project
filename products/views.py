from django.shortcuts import render
from .models import Product


def flowers(request):
    flowers = Product.objects.filter(category__name='Flowers')
    context = {
        'products': flowers,
    }
    return render(request, 'products/flowers.html', context)



def plants(request):
    plants = Product.objects.filter(category__name='Plants')
    context = {
        'products': plants,
    }
    return render(request, 'products/plants.html', context)