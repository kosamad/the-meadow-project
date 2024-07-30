from django.shortcuts import render

# Create your views here.

def about_view(request):
    return render(request, 'about/about.html')
