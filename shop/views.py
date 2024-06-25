from django.shortcuts import render
from products.models import Category


def shop(request):
    """ View function to render the shop page showing all categories of products and events """

    categories = Category.objects.all()

    context = {
        'categories': categories,
    }
    return render(request, 'shop/shop.html', context)
