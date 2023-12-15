from django.shortcuts import render, redirect
# this decorators is applyed for decorate dashboard site
from django.contrib.auth.decorators import login_required
# this library is used for creating user
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import myUserCreationForm, RemoveUser
from django.http import HttpResponse

#without login the dashboard shouldnot be shown--> need "login required" -->decorate
@login_required
# this function create a dashboard website after user login
# request object store all posted imformation from browser (request.POST, request.GET)
def dashboard(request):
    return render(
        request, 'userlogin/dashboard.html',
    )
    

def register(request):
    """This function is defined for user registration"""
    if request.method == 'POST':
        #user myUserCreationForm to render register.html
        user_form = myUserCreationForm(request.POST)
        if user_form.is_valid():
            # create a new user object
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password1']
            )
            new_user.save()
            context = {"new_user":new_user}
            return render(
                request,
                'userlogin/register_done.html',
                context
            )
        else:
            print(user_form.errors)
    else:
        user_form = myUserCreationForm()
    return render(
        request,
        'userlogin/register.html',
        {"user_form":user_form},
        )
            
@login_required
def delete_user(request):
    """This function is defined for user deletion"""
    if request.method == 'POST':
        form = RemoveUser(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                user.delete()
                return render(
                    request,
                    'userlogin/delete_user_done.html',
                    {},
                )  
            else:
                return HttpResponse("User delete error! Pleae check your username and password!")
    else:
        form = RemoveUser()
        context = {"form":form}
        return render(request,'userlogin/delete_user.html',context)
    