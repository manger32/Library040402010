from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "Homepage"),
    path('authorize/', views.authorize, name = "Authorize"),
    path('navbar/', views.navbar, name = "Navigation")
]