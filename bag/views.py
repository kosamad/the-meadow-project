from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404



def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')





def add_to_bag(request, item_id):
    """ A view to handle adding a product/event to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    # getting bag variable in the session or create one.
    bag = request.session.get('bag',{})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

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
