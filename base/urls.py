from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('', views.home, name = "Homepage"),
    path('authorize/<str:pk>/', views.authorize, name = "Authorize"),
    path('navbar/', views.navbar, name = "Navigation"),
    path('create-resource/', views.create_resource, name="create-resource"),
    path('update-resource/<str:pk>/', views.update_resource, name="update-resource"),
    path('delete-resource/<str:pk>/', views.delete_resource, name="delete-resource"),
]