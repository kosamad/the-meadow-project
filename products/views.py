from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductOrderForm


def product_detail(request, product_id):
    """ A view to show the product details for an individual item """
    product = get_object_or_404(Product, pk=product_id)
    form = ProductOrderForm()

    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'products/product_detail.html', context)


def add_to_bag(request, product_id):
    """ A view to handle adding a product to the shopping bag """
    product = get_object_or_404(Product, pk=product_id)
    redirect_url = request.POST.get('redirect_url')

    if request.method == 'POST':        
        form = ProductOrderForm(request.POST)
        if form.is_valid():
            size = form.cleaned_data['size']            
            optional_card_message = form.cleaned_data.get('optional_card_message', '')
            note_to_seller = form.cleaned_data.get('note_to_seller', '')
            quantity = form.cleaned_data['quantity']
            selected_size_price = str(form.cleaned_data['selected_size_price']) # stored as a string
            product_id = form.cleaned_data['product_id']           

            # Unique identifyer for each product.
            item_id = f"{product_id}_{size}_{optional_card_message}_{note_to_seller}"

            # getting bag variable in the session or create one.
            bag = request.session.get('bag',{})

            if item_id in bag:
                bag[item_id]['quantity'] += quantity
            else:
                bag[item_id] = {
                    'quantity': quantity,
                    'size': size,                    
                    'optional_card_message': optional_card_message,
                    'note_to_seller': note_to_seller,
                    'selected_size_price': selected_size_price
                }

            # Store the updated bag back into the session
            request.session['bag'] = bag                

            return redirect(redirect_url)
    else:
        form = ProductOrderForm()

    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'products/product_detail.html', context)