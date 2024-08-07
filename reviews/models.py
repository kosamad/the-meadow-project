from django.db import models
from django.contrib.auth.models import User
from checkout.models import Order, ProductOrderLineItem, EventOrderLineItem

# Create your models here.

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)    
    review_text = models.TextField(null=False, blank=False,)

    def __str__(self):
        return f'Review by {self.user.username} for Order {self.order.order_number}'