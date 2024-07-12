"""
Products application model
"""
import uuid
from django.db import models


class Category(models.Model):
    """
    A model for product categories.
    """

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254, null=False, blank=False)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)    

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name



class Product(models.Model):
    """
    A model for products.
    """    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)       
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()    
    image = models.ImageField(null=True, blank=True, upload_to='product_images/')
    alt_text = models.TextField(default="")
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_gift_card = models.BooleanField(default=False)    
    is_active = models.BooleanField(default=True)
    is_infinite_stock = models.BooleanField(default=False, help_text='Check if stock is a bouquet')  

    SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )

    # Default order on the site is by firendly_name
    class Meta:
        ordering = ['friendly_name'] 

    def __str__(self):
        return self.name



class ProductVariant(models.Model):    
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    size = models.CharField(max_length=1, choices=Product.SIZE_CHOICES)
    stock = models.PositiveIntegerField(default=0, help_text='Number of items available in stock for this size')
    is_infinite_stock = models.BooleanField(default=False, help_text='Check if stock is a bouquet')
    price = models.DecimalField(max_digits=6, decimal_places=2)     
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('product', 'size')  # Ensures each size variant is unique for a product

    def __str__(self):
        return f"{self.product.name} - {self.get_size_display()}"
        




class Event(models.Model): 
    """
    A model for events.
    """       
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)    
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    event_datetime = models.DateTimeField(null=True, blank=True, verbose_name='Event Date and Time')
    duration_hours = models.IntegerField(default=1, verbose_name='Duration (hours)')  
    description = models.TextField()
    capacity = models.IntegerField()   
    tickets_sold = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True, upload_to='event_images/')
    alt_text = models.TextField(default="")
    is_active = models.BooleanField(default=True)
    is_event = models.BooleanField(default=True, editable=False)   

    class Meta:
        ordering = ['event_datetime']  

    def __str__(self):
        return self.name 

    
