from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from profiles.models import UserProfile
from django.contrib.auth.decorators import login_required
from checkout.models import Order
from .models import Review

# Create your views here.


@login_required
def reviews(request):
    '''Displays all reviews for the admin'''

    # Check if the user is an admin
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can access this page')
        return redirect(reverse('profile'))

    # Retrieve all reviews ordered by the created_on field in descending order
    reviews = Review.objects.all().order_by('-created_on')

    template = 'reviews/reviews.html'
    context = {
        'reviews': reviews,
    }

    return render(request, template, context)


@login_required
def delete_review(request, review_id):
    '''Deletes a review and redirects to the review list.'''
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only admin can delete reviews.')
        return redirect('profile')

    review = get_object_or_404(Review, id=review_id)

    # Delete the review
    review.delete()

    messages.info(request, 'Review has been successfully deleted.')
    return redirect('reviews')


@login_required
def review_order(request, order_id):
    '''Display the leave a reveiw page'''

    order = get_object_or_404(Order, id=order_id)
    profile = get_object_or_404(UserProfile, user=request.user)

    # get users username and eamil for display
    username = profile.user.username

    # Check if the order belongs to the current user
    if order.user_profile.user != request.user:
        messages.error(request, "You do not have permission to review this order.")
        return redirect('home')

    if request.method == 'POST':
        user = request.POST.get('user')
        review_text = request.POST.get('review_text')

    # Validate form
        if not review_text:
            messages.error(request, 'Please leave a review in the box')
            context = {
                'order': order,
                'username': username,
            }
            return render(request, 'reviews/review_order.html', context)

        # Create and save the review
        review = Review(
            user=request.user,
            order=order,
            review_text=review_text
        )
        review.save()

        messages.success(request, 'Your review has been successfully submitted!')
        return redirect('profile')

    template = 'reviews/review_order.html'
    context = {
        'order': order,
        'username': username,
    }
    return render(request, template, context)
