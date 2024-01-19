from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # following 'login/' is the keyword of website, actually is 127.0.0.1/8000/userlogin/login
    # and call the function user_login in views.py when loading this site
    #path('login/',views.user_login, name='login') html will be put in templates folder
    
    # html template will be put in /templates/registration folder
    #path('login/',auth_views.LoginView.as_view(), name='login')
    
    #you can also use as_view() function to map html files in template folder 
    path('login/',auth_views.LoginView.as_view(template_name='userlogin/login.html'),name='login'),
    
    #this link directs to logout site
    path('logout/',auth_views.LogoutView.as_view(template_name='userlogin/logout.html'), name ='logout'),
    
    path('register/', views.register, name='register'),
    
    #password change site use django default function PasswrodChangeView
    #"name" is important for calling path and function
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(template_name='userlogin/password_change.html'),
         name='change_password'),
    
    
    # in django default auth_views, all function members should be same with django docus. e.g. name="password_change_done"
    path('password-change-done',
         auth_views.PasswordChangeDoneView.as_view(template_name='userlogin/password_change_done.html'),
         name='password_change_done'),
    
    # This url is set to mapping for user deletion
    path('delete_user/', views.delete_user , name='delete_user') ,
    
    # This url is set to mapping customer email submmit form for email reset
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name ='userlogin/password_reset.html'),
         name='reset_password'),
    
    # This url is mapping for sending reset email
     path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name ='userlogin/password_reset_sent.html'),
         name='password_reset_done'),
     
     # Show link to password reset form in email
     path('password/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name ='userlogin/password_reset_confirm.html'),
         name='password_reset_confirm'),
     
     # Show password reset successfully changed msg 
     path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name ='userlogin/password_reset_complete.html'),
         name='password_reset_complete'),
     
     # Show current user name, first and last name, email
     path('show_userInfo/', views.show_userInfo, name='show_userInfo'),
]


#template_name ='userlogin/password_reset_sent.html'
