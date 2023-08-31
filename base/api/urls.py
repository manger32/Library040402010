from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_Routes),
    path('auth/', views.get_Authorizes),
    path('auth/<str:pk>', views.get_Authorize),
]
