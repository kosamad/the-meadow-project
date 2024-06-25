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
    description = models.CharField(max_length=254, null=False, blank=False)

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
    image = models.ImageField(null=True, blank=True)
    image_alt = models.CharField(max_length=254)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)        

    SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )

    size = models.CharField(max_length=1, choices=SIZE_CHOICES, null=True, blank=True)



    def __str__(self):
        return self.name

