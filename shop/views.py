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
    # List to hold filtered data
    combined_list = []

    if request.GET:
        if 'category' in request.GET:
            selected_category = request.GET['category']
            if selected_category == 'events':
                products = Product.objects.none() # no products are displayed
                events = Event.objects.all()
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

    # sort_by = request.GET.get('sort', 'name')
    # direction = request.GET.get('direction', 'asc')

    # if sort_by == 'price':
    #     combined_list_filtered = sorted(combined_list_filtered, key=lambda x: x['item'].price, reverse=(direction == 'desc'))
    # elif sort_by == 'name':
    #     combined_list_filtered = sorted(combined_list_filtered, key=lambda x: x['item'].friendly_name.lower(), reverse=(direction == 'desc'))




    # # Other sorting logic  
    # if request.GET:
    #     if 'sort' in request.GET:
    #         sortkey = request.GET['sort']
    #         sort = sortkey
    #         if sortkey == 'name':
    #             sortkey = 'lower_name'
    #             combined_list = combined_list.annotate(lower_name=Lower('name'))            
    #         if 'direction' in request.GET:
    #             if direction == 'desc':
    #                 sortkey = f'-{sortkey}'
    #         combined_list = combined_list.order_by(sortkey)

    # current_sorting = f'{sort}_{direction}' 
            
      
    

        
   

    context = {
        # 'combined_list': combined_list_filtered,       
        # 'categories': categories,
        # 'selected_category': selected_category,
        # 'query': query,
        # 'current_sorting': current_sorting,

        'categories': categories,
        'combined_list': combined_list_filtered,
        'selected_category': selected_category,
        'query': query,
        # 'sort': sort_by,
        # 'direction': direction,
    }

    return render(request, 'shop/shop.html', context)
