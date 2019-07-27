from django.urls import path
from blog import views

urlpatterns = [
    path(r'', views.index),
    path(r'index/', views.index, name='index'),
    path(r'login/', views.login, name='login'),
    path(r'search_name/', views.search_name),
    path(r'accounts/login/', views.index, name='index'),
    path(r'search_phone/', views.search_phone),
    path(r'register/', views.register, name='register'),
    path(r'event_manage/', views.event_manage, name='event_manage'),
    path(r'guest_manage/', views.guest_manage, name='guest_manage'),
    path(r'logout/', views.logout, name='logout')
]
