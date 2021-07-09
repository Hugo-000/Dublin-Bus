from django.shortcuts import render
from django.template import loader, Context, Template
from django.views.generic import View

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404


from .forms import JourneyPlannerForm

from scrapper.models import Stops, Routes, AllStopsWithRoute, ForecastWeather, CurrentWeather

import datetime

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class JourneyPlanner(View):
    # def get(self, request, *args, **kwargs):
    #     return render(request, 'journey-planner.html')

    def get(self, request):
        return render(request, 'journeyPlanner.html', {'form': JourneyPlannerForm()})

    def post(self, request, *args, **kwargs):
        form = JourneyPlannerForm(request.POST)

        if form.is_valid():
            context = self.info(form)
            print('Context', context)
            return render(request, 'journeyPlanner/map.html', context= context)
        else:
            return render(request, 'journeyPlanner.html', { 'form': form })

    def info(self, form):
        # Generate counts of some of the main objects
        num_stops = Stops.objects.all().count()
        num_routes = Routes.objects.all().count()
        fd = form.cleaned_data
        start = fd.get('start_point')
        destination = fd.get('destination_point')
        travel_date = fd.get('travel_date')
        travel_time = fd.get('travel_time')

        current_weather = CurrentWeather.objects.all()
        forecast_weather = ForecastWeather.objects.all()

        context = {
            'num_stops': num_stops,
            'num_routes': num_routes,
            'start': start,
            'destination': destination,
            'travel_date': travel_date,
            'travel_time': travel_time,
            'form': form,
            'current_weather' : current_weather,
            'forecast_weather' : forecast_weather
        }
        return context
    