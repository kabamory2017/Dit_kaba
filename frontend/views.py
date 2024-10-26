from django.shortcuts import render

def home(request):
    return render(request, 'frontend/home.html')

def about(request):
    return render(request, 'frontend/about.html')

def features(request):
    return render(request, 'frontend/features.html')

def contact(request):
    return render(request, 'frontend/contact.html')

def login(request):
    return render(request, 'frontend/login.html')

def register(request):
    return render(request, 'frontend/register.html')

