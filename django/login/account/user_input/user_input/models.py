from django.db import models

class LifestyleModel(models.Model):
    LIFESTYLE_CHOICES = [
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('with_Meat', 'with meat'),
    ]
    style = models.CharField(max_length=50, choices=LIFESTYLE_CHOICES)
    def calculate_emission(self):
        emission_daten = {
           'vegetarian':6.57,
           'vegan':5.14,
           'with_Meat':8.71
        }
        emission = emission_daten.get(self.style, 0)
        return emission

class TrafficModel(models.Model):
    MODE_CHOICES = [
        ('private_car_elec', 'Private_car_elec'),
        ('private_car_gasoline', 'Private_car_gasoline'),
        ('bus', 'Bus'),
        ('train', 'Train'),
        ('bike', 'Bike'),
        ('metro', 'Metro'),
        ('walk', 'Walk')
    ]
    mode = models.CharField(max_length=50, choices=MODE_CHOICES)
    distance = models.FloatField()

    def calculate_emission(self):
        emission_factors = {
            'private_car_elec': 0.18, 
            'private_car_gasoline': 0.289,
            'bus': 0.045,                   
            'train': 0.0799,   
            'metro': 0.0719,              
            'bike': 0.0399,                    
            'walk': 0,                 
        }

        emission_factor = emission_factors.get(self.mode, 0)
        return self.distance * emission_factor

class HouseholdModel(models.Model):
    number_of_people = models.IntegerField()
    size_of_housing = models.FloatField()
    country = models.CharField(max_length=100)

    def calculate_emission(self):
       return self.size_of_housing / self.number_of_people * 0.274

class DailyActivityModel(models.Model):
    date = models.DateField()
