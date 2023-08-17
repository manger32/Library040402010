from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "Homepage"),
    path('authorize/<str:pk>/', views.authorize, name = "Authorize"),
    path('navbar/', views.navbar, name = "Navigation"),
    path('create-resource/', views.create_resource, name="create-resource"),
]