from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

class myUserCreationForm(UserCreationForm):
    # this class inherites UserCreationForm class and extend the sign up fields with firstname, lastname and email
    class Meta:
        model = User
        fields = ("username","first_name","last_name","email")
        
    def get_username():
        username = User.get_username
        return username
    
    
class RemoveUser(forms.Form):
    # this form is applied to show password and user authentication site
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)