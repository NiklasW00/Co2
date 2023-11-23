from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def user_login(request):
    # if the request is POST, means user input name and password and then click the Button "submit"
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # is_valid() checks if user input is completely
        if form.is_valid():
            cd = form.cleaned_data
            # use authenticate() func to check if username and password is correct
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'],
            )
            
            #if user exists and name, password are correct
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse(
                        'Authenticated successfully'
                    )
                else:
                    return HttpResponse('Disabled account')
            # if invalid password
            else:
                return HttpResponse('Invalid login')
    # if the request is GET, means just load the login site show login site
    else:
        form=LoginForm()
        return render(request, 'userlogin/login.html', {'form': form})