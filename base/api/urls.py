from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('auth/', views.getAuthorizes),
    path('auth/<str:pk>', views.getAuthorize),
]
