from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.




# Contact form code adapted from Codemy.com YouTube video series https://www.youtube.com/watch?v=xNqnHmXIuzU
def contact(request):
    """ A view to return the index page """

    if request.method == 'POST':
        message_name = request.POST.get('message-name')
        message_email = request.POST.get('message-email')
        message = request.POST.get('message')

        #  Validating form and ensures all parts are presnt
        if not message_name or not message_email or not message:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'contact/contact.html')

        # send email
        send_mail(
            f'Contact form message from {message_name}',  # subject
            message,  # message
            message_email,  # from email
            ['themeadowproj@gmail.com'],  # to email
        )

        messages.success(request, 'Your email has been sent successfully!')
        return redirect('contact')        

    return render(request, 'contact/contact.html')