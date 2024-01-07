from django import forms

class Lifestyle(forms.Form):
    LIFESTYLE_CHOICES = [
        ('vegetarian','Vegetarian'),
        ('vegan','Vegan'),
        ('with_Meat','with meat'),
    ]
    style = forms.ChoiceField(label='Your Lifestyle:', choices=LIFESTYLE_CHOICES)


class TrafficForm(forms.Form):
    MODE_CHOICES = [
        ('private_car_elec', 'Private_car_elec'),
        ('private_car_gasoline', 'Private_car_gasoline'),
        ('bus', 'Bus'),
        ('train', 'Train'),
        ('bike','bike'),
        ('metro','Metro'),
        ('walk', 'Walk')
    ]

    mode = forms.ChoiceField(label='Transportation Mode', choices=MODE_CHOICES)
    distance = forms.FloatField(label='Distance (km)', min_value=0.5)

class Household(forms.Form):
    number_of_people = forms.IntegerField(label='Number of people', min_value=1, required=False)
    size_of_housing = forms.FloatField(label='Size of housing(m²)', min_value=1, required=False)
    country = forms.CharField(label='Country',initial='Germany')

class DailyActivityForm(forms.Form):
    datepicker = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}), required=True)
   