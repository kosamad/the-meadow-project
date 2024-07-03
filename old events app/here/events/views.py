from django.shortcuts import render, get_object_or_404, redirect
from .models import Event

def event_detail(request, event_id):
    """ A view to show the event details for an individual item """    
    event = get_object_or_404(Event, pk=event_id)
    context = {
        'event': event,
    }
    return render(request, 'events/event_detail.html', context)

