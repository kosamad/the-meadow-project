from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.db.models import Q
from products.models import Category, Product, Event 


def shop(request):
    """ View function to render the shop page showing all categories of products and events
    plus all individual products and events """

    categories = Category.objects.all()
    products = Product.objects.all()
    events = Event.objects.all()    
    query = None
    selected_category = None        
    # List to hold filtered data
    combined_list = []

    if request.GET:
        if 'category' in request.GET:
            selected_category = request.GET['category']            
            if selected_category == 'events':
                products = Product.objects.none()
                events = Event.objects.all()
            else:
                products = products.filter(category__name__icontains=selected_category)
                events = Event.objects.none()           

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter a search")
                return redirect(reverse('shop'))

            # product and event queries for name, descritpion and category
            product_queries = (
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__name__icontains=query)
            )
            products = products.filter(product_queries)

            event_queries = (
                Q(name__icontains=query) | 
                Q(description__icontains=query) | 
                Q(category__name__icontains=query)
            )                   
            events = events.filter(event_queries)              
    
    # Append products/events to combined_list
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

    # Default sorting of filtered shop
    combined_list_filtered= sorted(combined_list, key=lambda x: x['item'].friendly_name.lower())

    # Remove _ in selected_category name for display
    if selected_category:
        display_category = selected_category.replace('_', ' ')
    else:
        display_category = 'All'

    context = {
        'categories': categories,
        'combined_list': combined_list_filtered,
        'selected_category': display_category,
        'query': query,
    }

    return render(request, 'shop/shop.html', context)
