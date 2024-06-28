from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.db.models import Q
from products.models import Category, Product
from events.models import Event 



def shop(request):
    """ View function to render the shop page showing all categories of products and events
    plus all individual products and events """

    categories = Category.objects.all()
    products = Product.objects.all()
    events = Event.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter a search")
                return redirect(reverse('shop'))
            # product queries for name, descritpion and category
            product_queries = (
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__name__icontains=query)
            )
            # event query for name and description (as no category)
            event_queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(product_queries)
            events = events.filter(event_queries)

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
        'combined_list': combined_list_sorted,
        'search_term': query,
    }

    return render(request, 'shop/shop.html', context)
