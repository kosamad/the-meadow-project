from django.shortcuts import render
from products.models import Category, Product
from events.models import Event 



def shop(request):
    """ View function to render the shop page showing all categories of products and events
    plus all individual products and events """

    categories = Category.objects.all()
    products = Product.objects.all()
    events = Event.objects.all()


    combined_list = []
    for product in products:
        combined_list.append({
            'item': product,
            'item_type': 'Product',
        })
    for event in events:
        combined_list.append({
            'item': event,
            'item_type': 'Event',
        })

    # alphabetical sorting
    combined_list_sorted = sorted(combined_list, key=lambda x: x['item'].friendly_name.lower())

    context = {
        'categories': categories,
        'combined_list': combined_list_sorted
    }

    return render(request, 'shop/shop.html', context)
