from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CalculationResult, LifestyleModel, TrafficModel, HouseholdModel, DailyActivityModel
from datetime import date

class UserInputTest(TestCase):
    # enter cmd in project folder, then run commando: python manage.py test <app name>
    def setUp(self):
        # config urls, user reverse('<name of url in urls.py>') to call urls
        self.dashboard_url = reverse('dashboard')
        self.showhistory_url = reverse('show_history')
    
    def test_trafficModel(self):
        myTrafficModel = TrafficModel(mode='private_car_gasoline',distance=100)
        result = myTrafficModel.calculate_emission()
        # check if result correctly
        self.assertEqual(round(result,2), round(0.18*100,2))  

    def test_lifestyleModel(self):
        myLifestyleModel = LifestyleModel(style='with_Meat')
        result = myLifestyleModel.calculate_emission()
        # check if result correctly
        self.assertEqual(round(result,2), 8.71) 
    
    def test_householdModel(self):
        myHouseholdModel = HouseholdModel(number_of_people=2, size_of_housing = 88.5, country='Germany')
        result = myHouseholdModel.calculate_emission()
        # check if result correctly
        self.assertEqual(round(result,2), round(88.5 / 2 * 0.125,2))
        
    def test_calculationResult(self):
        # set the timestamp manually
        myDate = date(1996,8,8)
        myCalculationResult = CalculationResult(value=128.33,date=myDate)
        myCalculationResult.save()
        objectFromDataBase = CalculationResult.objects.get(date = myDate)
        result = objectFromDataBase.value
        # check if the value can be found in database
        self.assertEqual(result, 128.33)
        objectFromDataBase.delete()