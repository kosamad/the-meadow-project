from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.db.models import Q
from products.models import Category, Product, Event 



def shop(request):

    """ View function to render the shop page showing ALL categories of products
     plus ALL individual individual products/events """

    # Gather data
    categories = Category.objects.all()
    products = Product.objects.all()
    events = Event.objects.all()
    # parameters so no errors when page is loaded if they don't exist/ arne't being used
    query = None  
    sort = None
    direction = None
    combined_list = []
    selected_category = None 

    if request.GET:            
    
        # show the specific categories of products or event (note the event category does not have an s in Category)
        if 'category' in request.GET:           
            selected_category = request.GET['category']
            if selected_category == 'events':
                products = Product.objects.none()
                events = Event.objects.all()
            elif selected_category == 'products':
                products = Product.objects.all()
                events = Event.objects.none()
            else:
                products = products.filter(category__name__icontains=selected_category)
                events = events.filter(category__name__icontains=selected_category)
        
        
        # checking for queries sent from the search box
        if 'q' in request.GET:
            query = request.GET['q']
            # if the query is blank = an error message
            if not query:
                messages.error(request, "You didn't enter a search")
                return redirect(reverse('shop'))

            # product and event queries for name, descritpion and category
            product_queries = (
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__friendly_name__icontains=query)
            )
            products = products.filter(product_queries)

            event_queries = (
                Q(name__icontains=query) | 
                Q(description__icontains=query) | 
                Q(category__friendly_name__icontains=query)
            )                   
            events = events.filter(event_queries)
        
    # group (append) products and events together for sorting.  
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

     # Format selected_category for display
    if selected_category:
        display_category = selected_category.replace('_', ' ').title()  # Format category name
    else:
        display_category = 'All'

    context = {
        'products': products,
        'events': events,
        'search_term': query,
        'current_categories': Category.objects.filter(name=selected_category) if selected_category else categories,
        'combined_list': combined_list,
        'item_count': len(combined_list),
        'selected_category': display_category,
        
    }

    return render(request, 'shop/shop.html', context)

