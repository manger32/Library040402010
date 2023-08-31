from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('', views.home, name = "Homepage"),
    path('authorize/<str:pk>/', views.authorize, name = "Authorize"),
    path('profile/<str:pk>/', views.userProfile, name = "user-profile"),
    path('navbar/', views.navbar, name = "Navigation"),
    path('create-resource/', views.create_resource, name="create-resource"),
    path('update-resource/<str:pk>/', views.update_resource, name="update-resource"),
    path('delete-resource/<str:pk>/', views.delete_resource, name="delete-resource"),
    path('delete-comment/<str:pk>/', views.delete_comment, name="delete-comment"),
    path('update-profile/', views.updateProfile, name="update-profile"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activitiesPage, name="activity"),
    path('file-upload/', views.file_upload, name="file-upload"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
