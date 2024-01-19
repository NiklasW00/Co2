from django.shortcuts import render, redirect
# this decorators is applyed for decorate dashboard site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import DailyActivityForm, Lifestyle, TrafficForm, Household
from .models import DailyActivityModel, LifestyleModel, TrafficModel, HouseholdModel, CalculationResult
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

#without login the dashboard shouldnot be shown--> need "login required" -->decorate
# this function create a dashboard website after user login
@login_required
def dashboard(request):
    if request.method == 'POST': #Determine whether the user has made a submission.
        daily_activity_form = DailyActivityForm(request.POST)
        lifestyle_form = Lifestyle(request.POST)
        household_form = Household(request.POST)
        traffic_form = TrafficForm(request.POST)

        if daily_activity_form.is_valid() and lifestyle_form.is_valid() and household_form.is_valid() and traffic_form.is_valid(): #Validate whether the form submitted by the user is correct.
            
            try: #if the submitted forms are correct, then do this part
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

                # call the function defined in models.py to calculate carbon emissions.
                total_emission = (lifestyle.calculate_emission() + 
                                    traffic.calculate_emission() + 
                                    household.calculate_emission())
                
                total_emission = round(total_emission, 2)
                calculate_result = CalculationResult(
                    date = daily_activity.date,
                    value = total_emission
                )
                
                # check if timestamp is already existed in database
                # object CalaulationResult only need to be updated if timestamp existed
                if check_timestamp(CalculationResult, daily_activity.date) == False:
                    calculate_result.save()
                else:
                    calculate_result_update = CalculationResult.objects.get(date = daily_activity.date)
                    calculate_result_update.value = total_emission
                    calculate_result_update.save()
                    
                output_content = f"your daily CO2 emission is {total_emission} kg"
                return HttpResponse(output_content)
                
            
            except Exception as e: #if the submitted forms are invalid, then return to the error
                return HttpResponse('Error: {}'.format(e))
        else:
            return HttpResponse('form invalid')
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

    dashboard = [daily_activity_form, lifestyle_form, household_form, traffic_form,]
    
    return render(
        request, 'userinput/dashboard.html',{'dashboard':dashboard}
    )


def check_timestamp(CalculationResult, myDate):
    if CalculationResult.objects.filter(date = myDate).exists():
        return True
    else:
        return False