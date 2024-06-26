from django.shortcuts import render
from products.models import Category, Product



def shop(request):
    """ View function to render the shop page showing all categories of products and events
    plus all products """

    categories = Category.objects.all()
    products = Product.objects.all()

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'shop/shop.html', context)
