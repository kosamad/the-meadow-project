from django.shortcuts import render


def shop(request):
    """ View function to render the shop page """
    return render(request, 'shop/shop.html')
