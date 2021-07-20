from django.shortcuts import render
from django.template import loader, Context, Template
from django.views.generic import View
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
import json

from .forms import JourneyPlannerForm,LeapCradForm

from .leap_card import leap_info

from scrapper.models import Stops, Routes, AllStopsWithRoute, ForecastWeather, CurrentWeather, Covid

#from G1_RP_Dublin-Bus-App.initial_basic_modelling.modelling_per_line.py import open_csv_create_models

#from G1_RP_Dublin-Bus-App.initial_basic_modelling.modelling_per_line.py import open_csv_create_models

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
            print('request_body', request_body)

            inputValues = self.getInputValues(request_body)

            print('*************************')
            print()
            print('inputValues', type(inputValues), inputValues)
            print()
            print('*************************')
            
            predicted_data = self.getPredictedEstimatedTime("130", "IB", inputValues)
            print("PREDICTED DATA", predicted_data)
            return JsonResponse({})
        
        else:
            form = JourneyPlannerForm(request.POST)

            if form.is_valid():
                context = self.info(form)

                print('*************************')
                print()
                print('Context', context)
                print()
                print('*************************')
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
        print('type info treavel_date', type(travel_date))
        print()
        print('type info travel_time', type(travel_time))
        print()
        print('*************************')

        user_unix_time = self.toUnix(form)

        if travel_date == '' and travel_time == '':
            weather = self.getCurrentWeather()
        else:
            weather = self.getForecastWeather(travel_date, travel_time)

        weather = model_to_dict(weather)

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

    def getCurrentWeather(self):
        current_weather = CurrentWeather.objects.all().last()
        return current_weather

    def getForecastWeather(self, travel_date, travel_time):
        user_forecast_datetime = self.forecastDatetime(travel_date, travel_time)
        forecast_weather = ForecastWeather.objects.get(dt_iso=user_forecast_datetime)
        return forecast_weather
    
    def getInputValues(self, request_body):
        # info = self.fetchJSON(request_body)
        travel_date = request_body['travel_date']
        travel_time = request_body['travel_time']
        travel_datetime = datetime.datetime.combine(travel_date, travel_time)

        print('*************************')
        print()
        print('type getInputValues treavel_date', type(travel_date))
        print()
        print('type getInputValues travel_time', type(travel_time))
        print()
        print('type getInputValues travel_datetime', type(travel_datetime), travel_datetime)
        print()
        print('*************************')

        if travel_date == '' and travel_time == '':
            weather = self.getCurrentWeather()
        else:
            weather = self.getForecastWeather(travel_date, travel_time)

        weather = model_to_dict(weather)

        month = travel_datetime.strftime('%-m')
        hour = travel_datetime.strftime('%-H')
        weekday = travel_datetime.strftime('%w')
        if weekday == '0':
            weekday = '7'
        weekdayName = travel_datetime.strftime('%a')
        print('*************************')
        print()
        print('Month', month)
        print('Hour', hour)
        print('weekday', type(weekday), weekday)
        print('weekday name', weekdayName)
        print()
        print('*************************')

        weatherMainDict = {"Rain": 1, "Clouds": 2,"Drizzle": 3,"Clear": 4,"Fog": 5,"Mist": 6,"Snow": 7,"Smoke": 8}

        weather['weather_main'] = weatherMainDict[weather['weather_main']]

        print('*************************')
        print()
        print('weather main', weather['weather_main'])
        print()
        print('*************************')


        InputValues = [int(weather["temp"]), 
                        int(weather['feels_like']), 
                        int(weather['humidity']),  
                        float(weather['wind_speed']),
                        int(weather['rain_1h']),
                        int(weather['clouds_all']),
                        int(weather['weather_main']),
                        int(weekday),
                        int(hour),
                        int(month),
        ]

        return InputValues

    def iconMatching(self,key):
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

    def forecastDatetime(self, travel_date, travel_time):
        forecast_6am = datetime.time(6,0,0)
        forecast_9am = datetime.time(9,0,0)
        forecast_12pm = datetime.time(12,0,0)
        forecast_15pm = datetime.time(15,0,0)
        forecast_18pm = datetime.time(18,0,0)
        forecast_21pm = datetime.time(21,0,0)
        forecast_00am = datetime.time(0,0,0)

        if travel_time > datetime.time(4,30) and travel_time <= datetime.time(7,30):
            user_forecast_datetime = datetime.datetime.combine( travel_date, forecast_6am)
        elif travel_time > datetime.time(7,30) and travel_time <= datetime.time(10,30):
            user_forecast_datetime = datetime.datetime.combine( travel_date, forecast_9am)
        elif travel_time > datetime.time(10,30) and travel_time <= datetime.time(13,30):
            user_forecast_datetime = datetime.datetime.combine( travel_date, forecast_12pm)
        elif travel_time > datetime.time(13,30) and travel_time <= datetime.time(16,30):
            user_forecast_datetime = datetime.datetime.combine( travel_date, forecast_15pm)
        elif travel_time > datetime.time(16,30) and travel_time <= datetime.time(19,30):
            user_forecast_datetime = datetime.datetime.combine( travel_date, forecast_18pm)
        elif travel_time > datetime.time(19,30) and travel_time <= datetime.time(22,30):
            user_forecast_datetime = datetime.datetime.combine( travel_date, forecast_21pm)
        elif travel_time > datetime.time(22,30) and travel_time <= datetime.time(0,0):
            travel_date += datetime.timedelta(days=1)
            user_forecast_datetime = datetime.datetime.combine( travel_date, forecast_00am)
        else:
            user_forecast_datetime = 'error'

        return user_forecast_datetime

    def toUnix(self, form):
        fd = form.cleaned_data
        travel_date = fd.get('travel_date')
        travel_time = fd.get('travel_time')

        user_datetime = datetime.datetime.combine(travel_date, travel_time)

        user_unix_time = datetime.datetime.timestamp(user_datetime)

        return user_unix_time

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
        info['travel_date'] = datetime.datetime.strptime(info['travel_date'], '%d/%m/%Y').date()

        print()
        print('Type Travel Date after strf', type(info['travel_date']), info['travel_date'] )
        print('Type Travel Time after strf', type(info['travel_time']), info['travel_time'] )
        print()
        print('*************************')

        # print(info)
        print(info)
        return info

    def getPredictedEstimatedTime(self, route, direction, inputValues):

        print('*************************')
        print()
        print('inputValues', type(inputValues), inputValues)
        print()
        print('*************************')
        
        filename = str(route) + "_" + str(direction)
        path = "../modelsNew/"+filename

        cwd = os.getcwd()
        print("CWD", cwd)
        # Load the Model back from file
        if os.path.isfile(path):
            print("success")
            with open(path, 'rb') as file:  
                busRoutePickleModel = pickle.load(file)

                input_vals = np.array(inputValues)
                x_test = input_vals.reshape(1, -1)
                pred = busRoutePickleModel.predict(x_test)
                prediction = int(pred)
                print(prediction, "mins")

                return prediction
                # arguments used to train the model
                #'temp', 'feels_like', 'humidity', 'wind_speed', 'rain_1h', 'clouds_all',’weather_main’,’weekday’ 'Hour', 'Month'

            print(busRoutePickleModel)
        else:
            print("failed")
            return "Error: Couldn't compute the prediction"


class BusRoutes(View):
    def get(self, request, *args, **kwargs):
        routes=Routes.objects.all()
        route_number_set=set(())
        all_route_Info={}

        for route in routes:
            route_number_set.add(route.route_name)

        for route_number_chosed in route_number_set:
            route_chosed=AllStopsWithRoute.objects.select_related("stop").defer("id").filter(route_number=route_number_chosed)
            route_info={}
            for stop_of_chosed_route in route_chosed:
                route_info[stop_of_chosed_route.stop_sequence]={
                    "stop_name":stop_of_chosed_route.stop_name,
                    "stop_headsign":stop_of_chosed_route.stop_headsign,
                    "position":""+stop_of_chosed_route.lat+","+stop_of_chosed_route.lng,
                    "lat":stop_of_chosed_route.lat,
                    "lng":stop_of_chosed_route.lng,
                }
            all_route_Info[route_number_chosed]=route_info
        return render(request, 'routes.html',{ 'routes': all_route_Info })
    #def post(self, request, *args, **kwargs):
        allStopsWithRoute=AllStopsWithRoute.objects.all()
        stops=Stops.objects.all()
        form = searchRoute(request.POST)
        if form.is_valid():
            context = self.info(form)
            print('Context', context)
            return render(request, 'routes.html', context= context)
        else:
            return render(request, 'routes.html',{"form":form})
        
        

class CovidInfo(View):
    def get(self, request):
        try:
            covid_stat = Covid.objects.all().order_by('-dt')[0]
            #Get the last 14 dates records in DB
            covid_chart = Covid.objects.all().order_by('-dt')[:14][::-1]
        except Covid.DoesNotExist:
            raise Http404("Covid data does not exist")
        return render(request, 'covidInfo.html', {'covid': covid_stat,'covid_chart':covid_chart})

class LeapCard(View):
    def get(self, request):
        return render(request, 'leapCard.html', {'form': LeapCradForm()})

    def post(self, request, *args, **kwargs):
        form = LeapCradForm(request.POST)
        if form.is_valid():
            fd = form.cleaned_data
            leap_username = fd.get('leap_username')
            leap_password = fd.get('leap_password')
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
                "leap_card_number" : "11",
                "leap_card_status" : "11",
                "leap_card_type" : "11",
                "leap_credit_status" : "11",
                "leap_expiry_date" : "11",
                "leap_issue_date" : "11",
                "leap_auto_topup" : "11",
            }
            return render(request, 'leapCard/showLeap.html', context= context_hard)
        else:
            return render(request, 'leapCard.html', { 'form': form })
