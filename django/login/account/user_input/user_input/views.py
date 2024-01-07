from django.shortcuts import render, redirect
from .forms import DailyActivityForm, Lifestyle, TrafficForm, Household
from .models import DailyActivityModel, LifestyleModel, TrafficModel, HouseholdModel
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

def submit_daily_activity(request):
    if request.method == 'POST':
        daily_activity_form = DailyActivityForm(request.POST)
        lifestyle_form = Lifestyle(request.POST)
        household_form = Household(request.POST)
        traffic_form = TrafficForm(request.POST)

        if daily_activity_form.is_valid() and lifestyle_form.is_valid() and household_form.is_valid() and traffic_form.is_valid():
            
            try:
                daily_activity = DailyActivityModel(date=daily_activity_form.cleaned_data['datepicker'])
                daily_activity.save()

                # lifestyle 
                lifestyle_data = lifestyle_form.cleaned_data
                lifestyle = LifestyleModel(**lifestyle_data)
                lifestyle.save()

                
                # household
                household_data = household_form.cleaned_data
                household = HouseholdModel(**household_data)
                household.save()
                
                # traffic
                traffic_data = traffic_form.cleaned_data
                traffic = TrafficModel(**traffic_data)
                traffic.save()

                total_emission = 0

            
                total_emission = (lifestyle.calculate_emission() + 
                                    traffic.calculate_emission() + 
                                    household.calculate_emission())
                
                total_emission = round(total_emission, 2)


                return render(request, 'test.html', {'daily_activity_form': daily_activity_form, 'lifestyle_form': lifestyle_form, 'household_form': household_form, 'traffic_form': traffic_form,'total_emission': total_emission}) 

                
            
            except Exception as e:
                return HttpResponse('Error: {}'.format(e))
        
        '''
        #verify that the form was submitted successfully
        if daily_activity_form.is_valid() and lifestyle_form.is_valid() and household_form.is_valid() and traffic_form.is_valid():
            print("Daily Activity Form Data:", daily_activity_form.cleaned_data)
            print("Lifestyle Form Data:", lifestyle_form.cleaned_data)
            print("traffic Form DATA:",traffic_form.cleaned_data) 
            print(" household from data",household_form.cleaned_data)
            return HttpResponse('success')


        else:
            return HttpResponse('failed')
        '''
    else:
        daily_activity_form = DailyActivityForm()
        lifestyle_form = Lifestyle()
        household_form = Household()
        traffic_form = TrafficForm()


    return render(request, 'test.html', {'daily_activity_form': daily_activity_form, 'lifestyle_form': lifestyle_form, 'household_form': household_form, 'traffic_form': traffic_form,'total_emission': None})

