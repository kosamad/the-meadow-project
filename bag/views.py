from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from products.models import Product, Event


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')





def add_to_bag(request, item_id):
    """ A view to handle adding a product/event to the shopping bag """
    # Quantity from form (converted to int from string)
    quantity = int(request.POST.get('quantity'))
    # Where to go after the form is submitted
    redirect_url = request.POST.get('redirect_url')

    if request.method == 'POST':
        item_type = request.POST.get(item_type)
        item_id = request.POST.get('item_id')   
        quantity = int(request.POST.get('quantity', 1))
        
    bag = request.session.get('bag', {})  

   


    if item_id in list(bag.keys()):
        bag[item_id]+- quantity
    else:
        bag[item_id] = quantity


    request.session['bag'] = bag
    print(request.session['bag'])    
    return redirect(redirect_url)




    # # Determine if the item being added is a product or event
    # if item_id.startswith('P_'):
    #     product_id = item_id[2:]  # Extract the product ID, starting at index 2 (removing 'P_')
    #     item = get_object_or_404(Product, pk=product_id) # get that product
    #     item_type = 'product'
    # elif item_id.startswith('E_'):
    #     event_id = item_id[2:]  # Extract the event ID
    #     item = get_object_or_404(Event, pk=event_id) # get that event
    #     item_type = 'event'

    # # getting bag variable (dictionary) in the session or create one.
    # bag = request.session.get('bag',{})

    # if item_id in bag:
    #     # Increment quantity if the item already exists in bag
    #     bag[item_id]['quantity'] += quantity
    # else:
    #     # Add new item to the bag with information
    #     bag[item_id] = {
    #         'type': item_type,
    #         'quantity': quantity,
    #         'item': item, # Object (actual event/product) therefore has all additional info from model.
    #     }

    # Store the updated bag back into the session
    request.session['bag'] = bag
    print(request.session['bag'])    
    return redirect(redirect_url)




    


   

    

    # product = get_object_or_404(Product, pk=product_id)
    # redirect_url = request.POST.get('redirect_url')
    # # getting bag variable in the session or create one.
    # bag = request.session.get('bag',{})

    # if request.method == 'POST':        
    #     form = ProductOrderForm(request.POST)
    #     if form.is_valid():
    #         size = form.cleaned_data['size']            
    #         optional_card_message = form.cleaned_data.get('optional_card_message', '')
    #         note_to_seller = form.cleaned_data.get('note_to_seller', '')
    #         quantity = form.cleaned_data['quantity']
    #         selected_size_price = form.cleaned_data['selected_size_price']
    #         product_id = form.cleaned_data['product_id']       
            

    #         # Store the updated bag back into the session
    #         request.session['bag'] = bag

    #         print.session['bag']                    

    #         return redirect(redirect_url)
    # else:
    #     form = ProductOrderForm()

    # context = {
    #     'product': product,
    #     'form': form,
    # }
    # return render(request, 'products/product_detail.html', context)
