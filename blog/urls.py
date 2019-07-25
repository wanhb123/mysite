from django.urls import path
from blog import views

urlpatterns = [
    path(r'', views.index),
    path(r'index/', views.index, name='index'),
    path(r'accounts/login/', views.index, name='index'),
    path(r'register/', views.register, name='register'),
    path(r'login/', views.login, name='login'),
    path(r'login_success/', views.login_success, name='logout'),
    path(r'logout/', views.logout, name='logout')
]
