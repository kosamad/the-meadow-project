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
    selected_category = None
    sort = None
    direction = 'asc' # Default direction
    combined_list_sorted = None

    if request.GET:
        if 'category' in request.GET:
            selected_category = request.GET['category']
            if selected_category == 'events':
                products = Product.objects.none() # no products are displayed
                events = events
            else:
                products = products.filter(category__name__icontains=selected_category)
                events = Event.objects.none() # no events are displayed

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
            products = products.filter(product_queries)
            # event query for name and description (as no category)
            event_queries = Q(name__icontains=query) | Q(description__icontains=query)            
            events = events.filter(event_queries)

    # List to hold filtered data
    combined_list = []

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
    
    # Sorting logic
    if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort=sortkey
            if sortkey == 'name':
                combined_list.sort(key=lambda x: x['item'].friendly_name.lower())
            elif sortkey == 'price':
                combined_list = sorted(combined_list, key=lambda x: x['item'].price)

            if 'direction' in request.GET and request.GET['direction'] == 'desc':
                combined_list.reverse()
                direction = 'desc'

    current_sorting = f'{sort}_{direction}'
          

    # combined_list_sorted = sorted(combined_list, key=lambda x: x['item'].friendly_name.lower())
      
    # sort_by = request.GET.get('sort', None)
    # if sort_by == 'price':
    #     combined_list_sorted = sorted(combined_list, key=lambda x: x['item'].price)
    # else:
    #     combined_list_sorted = sorted(combined_list, key=lambda x: x['item'].friendly_name.lower())
        
    context = {
        'categories': categories,
        'combined_list': combined_list,
        'search_term': query,
        'selected_category': selected_category,        
        'current_sorting': current_sorting,
    }

    return render(request, 'shop/shop.html', context)
