from django.shortcuts import render, redirect

# Create your views here.
def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')



def add_to_bag(request, item_id):
    """ A view that adds a quantiy of a spcific product/event to the bag"""

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    bag = request.session.get('bag',{})

     # Convert item_id (UUID) to string before using it as a key
    item_id_str = str(item_id)

    if item_id_str in list(bag.keys()):
        bag[item_id_str] += quantity
    else:
        bag[item_id_str] = quantity

    request.session['bag'] = bag
    print(request.session['bag'])

    return redirect(redirect_url)

# note: Ensure that wherever you retrieve items from the bag session dictionary, you consistently use string keys (e.g., str(item_id)) to access or modify items.
