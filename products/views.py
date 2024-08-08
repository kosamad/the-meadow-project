from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Product, Event, ProductVariant
from .forms import ProductForm, ProductVariantForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def product_detail(request, product_uuid):
    """ A view to show the product details for an individual item """

    product = get_object_or_404(Product, id=product_uuid) # id=product_id I am using UUID
    variants = ProductVariant.objects.filter(product=product)
    default_variant = variants.filter(size='M').first() or variants.first()
    default_price = default_variant.price if default_variant else None

    context = {
        'product': product,
        'variants': variants,
        'default_price': default_price,
        'default_variant_id': default_variant.id if default_variant else None,
    }
    return render(request, 'products/product_detail.html', context)



def event_detail(request, event_uuid):
    """ A view to show the event details for an individual item """ 

    event = get_object_or_404(Event, id=event_uuid)
    context = {
        'event': event,
    }
    return render(request, 'products/event_detail.html', context)



def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save()
            messages.success(request, 'Product added successfully! Now add variants.')
            # return redirect(reverse('add_product_variant', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        product_form = ProductForm()
    
    template = 'products/add_product.html'
    context = {
        'product_form': product_form,
    }
    return render(request, template, context)




def add_product_variant(request, product_uuid):

    # get product info
    product = get_object_or_404(Product, id=product_uuid)

    if request.method == 'POST':
        variant_form = ProductVariantForm(request.POST, request.FILES)
        if variant_form.is_valid():
            variant = variant_form.save(commit=False)
            variant.product = product
            variant.save()

            messages.success(request, 'Product variant added successfully!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product variant. Please ensure the form is valid.')
    else:
        variant_form = ProductVariantForm()
    
    template = 'products/add_product_variant.html'
    context = {
        'variant_form': variant_form,
        'product': product,
    }

    return render(request, template, context)





