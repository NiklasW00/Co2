from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.utils import timezone
from django.forms.widgets import DateTimeInput

class Lifestyle(forms.Form):
    LIFESTYLE_CHOICES = [
        ('vegetarian','vegetarian'),
        ('vegan','vegan'),
        ('with_Meat','with meat'),
    ]
    style = forms.ChoiceField(widget=forms.Select, label='Your Lifestyle:', choices=LIFESTYLE_CHOICES)

class TrafficForm(forms.Form):
    MODE_CHOICES = [
        ('private_car_elec', 'electric car'),
        ('private_car_gasoline', 'gasoline car'),
        ('bus', 'bus'),
        ('train', 'train'),
        ('bike','bike'),
        ('metro','tram'),
        ('walk', 'walk')
    ]

    mode = forms.ChoiceField(widget=forms.Select,label='Transportation Mode', choices=MODE_CHOICES)
    distance = forms.FloatField(label='Distance (km)', min_value=0.5)

class Household(forms.Form):
    number_of_people = forms.IntegerField(label='Number of people', min_value=1, required=False)
    size_of_housing = forms.FloatField(label='Size of housing(m²)', min_value=1, required=False)
    country = forms.CharField(label='Country',initial='Germany')

class DailyActivityForm(forms.Form):
    datepicker = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}), required=True)
   
class DateSelectForm(forms.Form):
    start_date = forms.DateField(label='start date', widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    end_date = forms.DateField(label='end date', widget=forms.DateInput(attrs={'type': 'date'}), required=True)
