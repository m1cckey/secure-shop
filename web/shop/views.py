from django.shortcuts import render



def render_page(request, template, context=None):
    return render(request, template, context or {})

def index(request):
    return render_page(request, 'index.html')

def login(request):
    return render_page(request, 'login.html')

def register(request):
    return render_page(request, 'register.html')

def search(request):
    return render_page(request, 'search.html')

def profile(request):
    return render_page(request, 'profile.html')