from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Product, Event, ProductVariant
from .forms import ProductForm, ProductVariantForm, EventForm
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
    """ A view to add an individual product item """

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save()
            messages.success(request, 'Product added successfully! Now add variants.')
            return redirect('product_detail', product_uuid=product.id)
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
    """ A view to add a variant to an individual product item """

    # get product info
    product = get_object_or_404(Product, id=product_uuid)

    if request.method == 'POST':
        variant_form = ProductVariantForm(request.POST, request.FILES, product=product)
        if variant_form.is_valid():
            variant = variant_form.save(commit=False)
            variant.product = product
            variant.save()
            messages.success(request, 'Product variant added successfully!')
            return redirect('product_detail', product_uuid=product.id)
        else:
            messages.error(request, 'Failed to add product variant. Please ensure the form is valid.')
    else:
        variant_form = ProductVariantForm(product=product)
    
    template = 'products/add_product_variant.html'
    context = {
        'variant_form': variant_form,
        'product': product,
    }

    return render(request, template, context)



def edit_product(request, product_uuid):
    """ A view to edit an individual product item """

    product = get_object_or_404(Product, id=product_uuid)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_detail', product_uuid=product.id)
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        product_form = ProductForm(instance=product)

    template = 'products/edit_product.html'
    context = {
        'product_form': product_form,
        'product': product
    }
    return render(request, template, context)



def edit_product_variant(request, variant_id):
    """ A view to edit an individual product item """

    variant = get_object_or_404(ProductVariant, id=variant_id)
    product = variant.product 

    if request.method == 'POST':
        # is edit means the size select box doesn't work on edit mode
        variant_form = ProductVariantForm(request.POST, request.FILES, instance=variant, is_edit=True)
        if variant_form.is_valid():
            variant_form.save()
            # Update product price based on the updated variant
            product.save()

            messages.success(request, 'Product variant updated successfully!')
            return redirect('product_detail', product_uuid=product.id)
        else:
            messages.error(request, 'Failed to update product variant. Please ensure the form is valid.')
    else:
        variant_form = ProductVariantForm(instance=variant, is_edit=True)

    template = 'products/edit_product_variant.html'
    context = {
        'variant_form': variant_form,
        'product': product,
        'variant': variant,
    }
    return render(request, template, context)



def add_event(request):
    """ A view to add an individual event """

    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():            
            #create a new event instance
            event = event_form.save()           
            return redirect('event_detail', event_uuid=event.id)
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        event_form = EventForm()
    
    template = 'products/add_event.html'
    context = {
        'event_form': event_form,
    }
    return render(request, template, context)


def edit_event(request, event_uuid):
    """ A view to edit an individual event """
    event = get_object_or_404(Event, id=event_uuid)

    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES, instance=event)
        if event_form.is_valid():         
            event_form.save()
            messages.success(request, 'Event updated successfully!')        
            return redirect('event_detail', event_uuid=event.id)
        else:
            messages.error(request, 'Failed to edit event. Please ensure the form is valid.')
    else:
        event_form = EventForm(instance=event)
    
    template = 'products/edit_event.html'
    context = {
        'event_form': event_form,
        'event': event,
    }
    return render(request, template, context)



