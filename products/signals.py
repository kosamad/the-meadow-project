from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models 
from .models import ProductVariant, Product


@receiver(post_save, sender=ProductVariant)
def update_product_price(sender, instance, **kwargs):
    """ Update the product price when a variant is added or updated """
    product = instance.product

    # Get all variants for the product
    variants = ProductVariant.objects.filter(product=product)

    # Find the price of the Medium size variant, or the lowest price if Medium is not available
    medium_variant = variants.filter(size='M').first()
    if medium_variant:
        new_price = medium_variant.price
    else:
        new_price = product.price # this should be set to the medium price in the first instance.   
    
    product.price = new_price
    product.save()