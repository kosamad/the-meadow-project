from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404



def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')
