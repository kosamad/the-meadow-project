"""
Events application model
"""


from django.db import models

class Event(models.Model): 
    """
    A model for events.
    """       
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    event_date = models.DateTimeField(null=True, blank=True, verbose_name='Event Date and Time')
    event_time = models.DateTimeField(null=True, blank=True, verbose_name='Event Time')
    description = models.TextField()
    capacity = models.IntegerField()   
    tickets_sold = models.IntegerField(default=0)

    def __str__(self):
        return self.name 

    
