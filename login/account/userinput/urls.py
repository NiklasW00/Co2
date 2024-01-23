from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('dashboard/', views.dashboard,name='dashboard'),
    path('show_history/', views.showHistory, name='show_history'),
]