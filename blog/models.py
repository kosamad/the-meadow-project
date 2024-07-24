from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Event

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='blog_images/')
    alt_text = models.TextField(default="")
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()   

    def __str__(self):
        """
        Return title
        """
        return self.title

    # def get_product_name(self):
    #     if self.product:
    #         return self.product.friendly_name
    #     return None

    # def get_event_name(self):
    #     if self.event:
    #         return self.event.friendly_name
    #     return None


