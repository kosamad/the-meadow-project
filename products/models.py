"""
Products application model
"""

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
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)    
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='product_images/')
    alt_text = models.TextField(default="")
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_gift_card = models.BooleanField(default=False)    
    is_active = models.BooleanField(default=True)       

    SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )

    size = models.CharField(max_length=1, choices=SIZE_CHOICES, null=True, blank=True)

    # Default order on the site is by firendly_name
    class Meta:
        ordering = ['friendly_name'] 

    def __str__(self):
        return self.name



class Event(models.Model): 
    """
    A model for events.
    """       
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    event_datetime = models.DateTimeField(null=True, blank=True, verbose_name='Event Date and Time')    
    description = models.TextField()
    capacity = models.IntegerField()   
    tickets_sold = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True, upload_to='event_images/')
    alt_text = models.TextField(default="")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['event_datetime']  

    def __str__(self):
        return self.name 

    
