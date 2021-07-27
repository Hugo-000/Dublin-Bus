import re
from django.shortcuts import render
from django.template import loader, Context, Template
from django.views.generic import View
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
import json

from .forms import JourneyPlannerForm

from .leap_card import leap_info

from scrapper.models import Stops, Routes, AllStopsWithRoute, ForecastWeather, CurrentWeather, Covid, RoutePrediction

import pickleModels 
import predictions

import datetime
import os.path
import pickle
import numpy as np

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class JourneyPlanner(View):
    # def get(self, request, *args, **kwargs):
    #     return render(request, 'journey-planner.html')

    def get(self, request):
        return render(request, 'journeyPlanner.html', {'form': JourneyPlannerForm()})

    def post(self, request, *args, **kwargs):
        if request.content_type == "application/json":
            request_body = self.fetchJSON(request.body)            
            busStepInfo = predictions.getBusStepInfo(request_body)
            travel_date = predictions.getTravelDate(request_body)
            travel_time = predictions.getTravelTime(request_body)
            weather = predictions.getWeather(travel_date, travel_time)
            inputValues = predictions.getInputValues(weather, travel_date, travel_time)
            busStepTimes = predictions.getBusStepTimes(busStepInfo, inputValues)
            totalBusTime = sum(busStepTimes)
            return JsonResponse({'estimatedTime': totalBusTime})
        
        else:
            form = JourneyPlannerForm(request.POST)

            if form.is_valid():
                context = self.info(form)
                return render(request, 'journeyPlanner/showRoute.html', context= context)
            else:
                return render(request, 'journeyPlanner.html', { 'form': form })

    def info(self, form):
        fd = form.cleaned_data
        origin = fd.get('origin_location')
        destination = fd.get('destination_location')
        travel_date = fd.get('travel_date')
        travel_time = fd.get('travel_time')

        print('*************************')
        print()
        print('type info travel_date', type(travel_date))
        print('type info travel_date', travel_date)
        print()
        print('type info travel_time', type(travel_time))
        print('type info travel_time', travel_time)
        print()
        print('*************************')

        user_unix_time = self.toUnix(form)

        weather = predictions.getWeather(travel_date, travel_time)

        print('*************************')
        print()
        print('Weather Dictionary', type(weather), weather)
        print('Weather icon', weather['weather_icon'])
        print()
        print('*************************')        
        
        # user_forecast_datetime = self.forecastDatetime(travel_date, travel_time)
        # forecast_weather = ForecastWeather.objects.get(dt_iso=user_forecast_datetime)
        # weather = model_to_dict(forecast_weather)
        iconFromDB = weather["weather_icon"]
        iconToHTML = self.iconMatching(iconFromDB)

        context = {
            'origin': origin,
            'destination': destination,
            'travel_date': travel_date,
            'travel_time': travel_time,
            'form': form,
            'weather' : weather,
            # 'user_forecast_datetime': user_forecast_datetime,
            'weather_icon': iconToHTML,
            'userUnix': user_unix_time
        }
        return context

    def fetchJSON(self, request_body):
        info = json.loads(request_body)

        print('*************************')
        print()
        print('type of info', type(info))
        print()
        print('*************************')
        print()
        print('Type Travel Date before strf', type(info['travel_date']), info['travel_date'] )
        print('Type Travel Time before strf', type(info['travel_time']), info['travel_time'] )
        print()
        print('*************************')
        
        info['travel_time'] = datetime.datetime.strptime(info['travel_time'], '%H:%M:%S').time()
        info['travel_date'] = datetime.datetime.strptime(info['travel_date'], '%Y-%m-%d').date()

        print()
        print('Type Travel Date after strf', type(info['travel_date']), info['travel_date'] )
        print('Type Travel Time after strf', type(info['travel_time']), info['travel_time'] )
        print()
        print('*************************')

        # print(info)
        print(info)
        return info

    def toUnix(self, form):
        fd = form.cleaned_data
        travel_date = fd.get('travel_date')
        travel_time = fd.get('travel_time')
        today = datetime.date.today()
        if travel_time != None:
            print('Have time')
            user_datetime = datetime.datetime.combine(travel_date, travel_time)
            user_unix_time = datetime.datetime.timestamp(user_datetime)
            return user_unix_time
        if travel_date == today and travel_time == None:
            print('have not time')
            user_datetime = datetime.datetime.now()
            user_unix_time = datetime.datetime.timestamp(user_datetime)
            return user_unix_time
        return "error"

    def iconMatching(self, key):
        dict = {
            "01n":"images/01d.png",
            "01d":"images/01n.png",
            "02n":"images/02.png",
            "02d": "images/02.png",
            "03d": "images/03.png",
            "03n": "images/03.png",
            "04d": "images/04.png",
            "04n": "images/04.png",
            "09d": "images/09.png",
            "09n": "images/09.png",
            "10d": "images/10.png",
            "10n": "images/10.png",
            "11d": "images/11.png",
            "11n": "images/11.png",
            "13d": "images/13.png",
            "13n": "images/13.png",
            "50d": "images/50.png",
            "50n": "images/50.png",
        }
        icon = dict.get(key)
        return icon


class BusRoutes(View):
    def get(self, request, *args, **kwargs):
        routes=Routes.objects.all()
        route_number_set=set(())
        for route in routes:
            route_number_set.add(route.route_name)
        #all_route_Info=[]
        #all_route_Info={}
        #for route_number_chosed in route_number_set:
            #route_chosed = AllStopsWithRoute.objects.raw('SELECT * FROM Dublin_Bus.scrapper_allstopswithroute inner join Dublin_Bus.scrapper_stops where scrapper_allstopswithroute.stop_id = scrapper_stops.stop_id and route_number = "'+route_number_chosed+'";')
            #route_chosed=AllStopsWithRoute.objects.select_related('stop').filter(route_number=route_number_chosed)
            #route_info=[]
            #route_info={}
            #for stop_chosed in route_chosed:
                #stop_coordinate=str(stop_chosed.stop.lat)+","+str(stop_chosed.stop.lng)
                #route_info.append(stop_of_chosed_route.stop.stop_name)
                #route_info.append(stop_coordinate)
                #route_info[stop_chosed.stop_sequence]={
                    #"stop_name":stop_chosed.stop.stop_name,
                    #"stop_coordinate":stop_coordinate,
                #}
            #all_route_Info[route_number_chosed]=route_info
            #all_route_Info.append(route_info)

        return render(request, 'routes.html',{"routes_name":route_number_set})
    def post(self, request, *args, **kwargs):
        routes=Routes.objects.all()
        route_number_set=set(())
        for route in routes:
            route_number_set.add(route.route_name)
        route_number_chosed = request.POST.get('route_name')
        #route_direction=request.POST.get('direction')
        route_chosed=AllStopsWithRoute.objects.select_related('stop').filter(route_number=route_number_chosed)
        #serializers.serialize("json",route_chosed)
        return render(request, 'routes.html',{"routes_name":route_number_set,"route_Info":route_chosed})



        
        

class CovidInfo(View):
    def get(self, request):
        try:
            covid_stat = Covid.objects.all().order_by('-dt')[0]
            #Get the last 14 dates records in DB
            covid_chart = Covid.objects.all().order_by('-dt')[:14][::-1]
        except Covid.DoesNotExist:
            raise Http404("Covid data does not exist")
        return render(request, 'covidInfo.html', {'covid': covid_stat,'covid_chart':covid_chart})

class LeapCard(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'leapCard.html')

    def post(self, request, *args, **kwargs): 
        leap_username = request.POST.get('leap_username')
        leap_password = request.POST.get('leap_password')
        #balance=dir(leap_info(leap_username,leap_password))
        #context = {
            #"leap_balance" : balance["balance"],
            #"leap_card_number" : balance["card_num"],
            #"leap_card_status" : balance["card_status"],
            #"leap_card_type" : balance["card_type"],
            #"leap_credit_status" : balance["credit_status"],
            #"leap_expiry_date" : balance["expiry_date"],
            #"leap_issue_date" : balance["issue_date"],
            #"leap_auto_topup" : balance["auto_topup"],
        #}
        context_hard = {
            "leap_balance" : "11",
            "leap_card_number" : leap_username,
            "leap_card_status" : "11",
            "leap_card_type" : "11",
            "leap_credit_status" : "11",
            "leap_expiry_date" : "11",
            "leap_issue_date" : "11",
            "leap_auto_topup" : "11",
        }
        return render(request, 'leapCard.html', context= context_hard)
        