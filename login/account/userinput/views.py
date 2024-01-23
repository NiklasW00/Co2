from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
# this decorators is applyed for decorate dashboard site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import DailyActivityForm, Lifestyle, TrafficForm, Household, DateSelectForm
from .models import DailyActivityModel, LifestyleModel, TrafficModel, HouseholdModel, CalculationResult
from django.http import HttpResponse
import matplotlib.pyplot as plt
import base64, io 
from datetime import date, timedelta

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
                # create a new object for alculationResult
                calculate_result = CalculationResult(
                    date = daily_activity.date,
                    value = total_emission
                )
                
                # save calculation result in database if the timestamp doesnot exist in database
                if check_timestamp(CalculationResult, daily_activity.date) == False:
                    calculate_result.save()
                else:
                    # update calculation result if timestamp exist
                    # find the object with timestamp and update the value
                    calculate_result_update = CalculationResult.objects.get(date = daily_activity.date)
                    calculate_result_update.value = total_emission
                    calculate_result_update.save()
                
                #plot calculation result
                graphic = plot_result(CalculationResult, daily_activity.date).decode('utf-8')
                
                # create form with elements graphic and user input date
                content = {"graphic":graphic,
                           "date":daily_activity.date}
                return render(
                     request, 'userinput/show_result.html',content
                )
            
            except Exception as e: #if the submitted forms are invalid, then return to the error
                return HttpResponse('Error: {}'.format(e))
        else:
            return HttpResponse('form invalid')
    else:
        daily_activity_form = DailyActivityForm()
        lifestyle_form = Lifestyle()
        household_form = Household()
        traffic_form = TrafficForm()

    dashboard = [daily_activity_form, lifestyle_form, household_form, traffic_form,]
    return render(
        request, 'userinput/dashboard.html',{'dashboard':dashboard}
    )

@login_required
def showHistory(request):
    # this function is applied to plot history data. User can select start and end date manuelly
    if request.method == 'POST': #Determine whether the user has made a submission.
        date_select_form = DateSelectForm(request.POST)
        if date_select_form.is_valid(): 
            start_date = date_select_form.cleaned_data["start_date"]
            end_date = date_select_form.cleaned_data["end_date"]
            graphic_history = plot_history(CalculationResult, start_date, end_date).decode('utf-8')
            return render(
                request, 'userinput/show_history.html',{'graphic_history':graphic_history}
            )
        else:
            return render(
                request, 'userinput/statistic.html',{'date_select_form':date_select_form}
            )
    else:
        date_select_form = DateSelectForm()
        return render(
         request, 'userinput/statistic.html',{'date_select_form':date_select_form}
    )

def plot_result(CalculationResult, myDate):
    # this function plots a diagramm for one-day calculation result
    if CalculationResult.objects.filter(date = myDate).exists():
        categories = ['You', 'mean of Germany', 'mean of the world']
        myResult = CalculationResult.objects.get(date = myDate) 
        myValue = myResult.value
        values = [float(myValue), 21.86, 12.88]
        my_grey = '#272626'
        my_green = '#3a8b63'
        my_yellow = '#ffd966'
        my_blue = '#53868b'
        diagram_color = [my_blue,my_yellow,my_green,]
        
        # let matplotlib works in background
        plt.switch_backend('Agg')
        plt.figure(figsize=(7, 5.24))
        plt.barh(categories, values, color=diagram_color, height=0.5)
        plt.title('CO2 Emission', color=my_grey)
        plt.xlabel('[kg/day]',color=my_grey)
        plt.xlim(0,max(values)*1.2)
        plt.tick_params(axis='x', colors=my_grey)
        plt.tick_params(axis='y', colors=my_grey)
        plt.tight_layout()
        # get ax object 
        ax = plt.gca()
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_color('grey')
        ax.spines['left'].set_color('grey')
        ax.spines['right'].set_color('none')
        
       
        # add data label on graphic 
        for index, value in enumerate(values):
            plt.text(value+1 , index, str(value), ha='left', va='center', color=my_grey)
       
        # save the grafic as io bytes data
        grafic_stream = io.BytesIO()
        plt.savefig(grafic_stream, format='png')
        plt.close()
        
        # transfer the image to base 64 code and output
        grafic_base64 = base64.b64encode(grafic_stream.getvalue())
        # return a URI with format base64 which can be loded in html directly
        return grafic_base64
    else:
        HttpResponse("object CalculationResult doesn't exist!")
        return None
    
def plot_history(CalculationResult, startDate, endDate):
    # this function is for ploting history CO2 emission with date input
    plt.switch_backend('Agg')
    timestamp = []
    value = []
    # transfer string input "startDate" and "endDate" to Date format
    # start_date = date.strptime(startDate, '%Y-%m-%d').date()
    # end_date = date.strptime(endDate, '%Y-%m-%d').date()
    # filter the CalculationResult objects with date range. Objects are orded by "date" (see models.py)
    results_objects = CalculationResult.objects.all()
    results_date_filted = results_objects.filter(date__range=(startDate, endDate))
    print(results_date_filted)
    myStartDate = startDate
    myDateList = create_date_list(startDate,endDate)
    
    for mydate in myDateList:
        # iterate myDateList and check each related object in database, if the corresponding object exists 
        if CalculationResult.objects.filter(date = mydate).exists():
            myCalculationResult = CalculationResult.objects.get(date=mydate)
            # defomate the datetime.date to string
            formatted_date = myCalculationResult.date.strftime('%d-%m')
            print("date output when object exists: "+formatted_date)
            timestamp.append(formatted_date)
            value.append(myCalculationResult.value)
        else:
            # if object not exits, set the emossion value to 0 and append to value list
            formatted_date = mydate.strftime('%d-%m')
            print("date output when object is none: "+formatted_date)
            timestamp.append(formatted_date)
            value.append(0)
        
    # plot graphic
    plt.plot(timestamp,value, marker='o')
    # set the data range in x with value myTick
    myTick = int(len(timestamp) / 8) + 1
    plt.xticks(timestamp[::myTick])
    my_grey = '#272626'
    plt.title('CO2 Footprint',color=my_grey)
    plt.ylabel('[kg/day]',color=my_grey)
    #set the range of y 
    plt.ylim(0,max(value)*1.5)
    plt.xlabel('date', color=my_grey)
    plt.tick_params(axis='x', colors=my_grey)
    plt.tick_params(axis='y', colors=my_grey)
    # add grid on graphic
    plt.grid(color='#eeeeee', linestyle='--')
    
    #set color for each axes
    ax = plt.gca()
    ax.spines['top'].set_color('grey')
    ax.spines['bottom'].set_color('grey')
    ax.spines['left'].set_color('grey')
    ax.spines['right'].set_color('grey')
    
    # save and output the graphic 
    grafic = io.BytesIO()
    plt.savefig(grafic, format='png')
    plt.close()
    grafic_base64 = base64.b64encode(grafic.getvalue())
    return grafic_base64

def check_timestamp(CalculationResult, myDate):
    # this function is used to check if the timestamp is already existed in database
    if CalculationResult.objects.filter(date = myDate).exists():
        return True
    else:
        return False
    
def date_calculation(start_date, end_date):
    # calculate date difference between start- and end date
    days_diff = start_date - end_date
    return days_diff.days

def create_date_list(start_date, end_date):
    # use start_date and end_date to create a date list
    # start_date and end_date are datetime.date type
    date_list = []
    date_diff = abs(date_calculation(start_date, end_date))

    # following code checks if the start_date greater than end_date
    if start_date < end_date:
        for _ in range(date_diff + 1):
            date_list.append(start_date)
            start_date += timedelta(days=1)
    else:
        # if start and end_date are reversed, correct the order. 
        for _ in range(date_diff + 1):
            date_list.append(end_date)
            end_date += timedelta(days=1)
    print(date_list)
    return date_list

