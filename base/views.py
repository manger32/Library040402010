from django.shortcuts import render
from . import views
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def authorize(request):
    return render(request, 'authorize.html')

def navbar(request):
    return render(request, 'navbar.html')