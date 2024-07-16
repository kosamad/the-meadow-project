from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Order, ProductOrderLineItem, EventOrderLineItem


@receiver(post_save, sender=ProductOrderLineItem)
@receiver(post_save, sender=EventOrderLineItem)
# handle post_save event with parameters (orderlineitem, instance of model that sent, boolean Ture is new or False if updated, and kwargs)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.order.update_total()



@receiver(post_delete, sender=ProductOrderLineItem)
@receiver(post_delete, sender=EventOrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.order.update_total()