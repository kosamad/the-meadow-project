from django.shortcuts import render

# Create your views here.





def contact(request):
    """ A view to return the index page """

    if request.method == 'POST':
        message_name = request.POST('message_name')
        message_email = request.POST['message_email']
        message = request.POST['message']

        context = {
            'message_name': message_name,
            'message_email': message_email
        }

        template = 'contact/contact.html'
       
        return render(request, template, context)      

    
    else:
        return render(request, 'contact/contact.html')



    return render(request, 'contact/contact.html')