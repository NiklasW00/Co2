from django.urls import path
from . import views

urlpatterns = [
    # following 'login/' is the keyword of website, actually is 127.0.0.1/8000/app_account/login
    # and call the function user_login in views.py when loading this site
    path('login/',views.user_login, name='login')
]