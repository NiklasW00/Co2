from django.shortcuts import render, redirect
from .forms import DailyActivityForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

def submit_daily_activity(request):
    if request.method == 'POST':
        form = DailyActivityForm(request.POST)
        if form.is_valid():
            # process the form data
            return HttpResponse('show result') 
    else:
        form = DailyActivityForm()

    return render(request, 'test.html', {'daily_activity_form': form})