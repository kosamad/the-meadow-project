from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Event
from django.urls import reverse
from datetime import datetime, date

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=False, blank=False, upload_to='blog_images/', default="")
    alt_text = models.TextField(default="", null=False, blank=False)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField(null=False, blank=False)   

    def __str__(self):
        """
        Return title
        """
        return self.title

    # URL so Admin can add posts from the form
    def get_absolute_url(self):
        # redirect to the id of the post just created.
        return reverse('post_detail', args=[self.id])

    # def get_product_name(self):
    #     if self.product:
    #         return self.product.friendly_name
    #     return None

    # def get_event_name(self):
    #     if self.event:
    #         return self.event.friendly_name
    #     return None


