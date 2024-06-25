from django.shortcuts import render
from .models import Event

def all_events(request):
    """ A view to return all events """

    events = Event.objects.all()

    context = {
        'events': events,
    }

    return render(request, 'events/events.html', context)
