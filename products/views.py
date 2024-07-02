from django.shortcuts import render, get_object_or_404
from .models import Product
from .forms import ProductOrderForm


def product_detail(request, product_id):
    """ A view to show the product details for an individual item """

    product = get_object_or_404(Product, pk=product_id)

    # Prduct order form
    if request.method == 'POST':
        form = ProductOrderForm(request.POST)
        if form.is_valid():
            size = form.cleaned_data['size']
            date = form.cleaned_data['date']
            delivery_option = form.cleaned_data['delivery_option']
            optional_card_message = form.cleaned_data.get('optional_card_message', '')
            note_to_seller = form.cleaned_data.get('not_to_seller', '')
            quantity = form.cleaned_data['quantity']
            selected_size_price = form.cleaned_data['selected_size_price']
            product_id = form.cleaned_data['product_id']
            return redirect('success')
        else:
            form = ProductOrderForm()


    context = {
        'product': product,
        'form': ProductOrderForm(),
    }
    return render(request, 'products/product_detail.html', context)