import re
from django.shortcuts import render
from django.template import loader, Context, Template
from django.views.generic import View
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
import json

from .forms import JourneyPlannerForm

from .leap_card import leap_info

from scrapper.models import Stops, Routes, AllStopsWithRoute, ForecastWeather, CurrentWeather, Covid, RoutePrediction

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
            estimatedTimes = self.getJourneyEstimatedRouteTimes(request_body)

            print('*************************')
            print()
            print('Estimated Bus Time', estimatedTimes)
            print()
            # totalBusTime = sum(estimatedTimes)
            # print('Total Bus Time', totalBusTime)
            # print()
            # print('*************************')

            return JsonResponse({'estimatedTime': estimatedTimes})
        
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

    def getJourneyEstimatedRouteTimes(self, request_body):
        inputValues = self.getInputValues(request_body)
        print('*************************')
        print()
        print('inputValues', type(inputValues), inputValues)
        print()
        print('*************************')

        busSteps = self.getbusInformation(request_body)

        print('*************************')
        print()
        print('Bus Info', type(busSteps), busSteps)
        print()
        print('*************************')
        
        estimatedRouteTimes = []
        estimatedTimes = []
        
        for i in range(len(busSteps)):
            routeNumber = busSteps[i]['routeNumber']
            intRouteNumber = int(routeNumber)
            headsign = busSteps[i]['headsign']
            # arrivalStop =
            direction = self.getRouteDirection(routeNumber, headsign)
            busSteps[i]['direction'] = direction
            print('*************************')
            print()
            print('direction I/O', busSteps[i]['direction']['direction'])
            print()
            print('*************************')
            temp = self.getPredictedEstimatedTime(routeNumber, busSteps[i]['direction']['direction'], inputValues)
            estimatedRouteTimes.append(int(temp))
            arrivalStopName = busSteps[i]['arrivalStop']
            departureStopName = busSteps[i]['departureStop']

            arrivalStopID = [int(character) for character in arrivalStopName.split() if character.isdigit()]
            departureStopID = [int(character) for character in departureStopName.split() if character.isdigit()]

            print('*************************')
            print()
            print('Arrival Stop Name', arrivalStopName)
            print('Arrival Stop ID', arrivalStopID)
            print('Departure Stop Name', departureStopName)
            print('Departure Stop ID', departureStopID)
            print()
            print('Route Number type', type(intRouteNumber))
            print()
            print('*************************')

            try: 
                arrivalDone = model_to_dict(RoutePrediction.objects.get(StopID = arrivalStopID[-1], Route=routeNumber))
            
            except RoutePrediction.DoesNotExist:
                return 'Stop does not exist'
            
            try:
                departureDone = model_to_dict(RoutePrediction.objects.get(StopID=departureStopID[-1], Route=routeNumber))

            except RoutePrediction.DoesNotExist:
                return 'Stop does not exist'
            print('*************************')
            print()
            print('Arrival Stop Name', arrivalStopName)
            print('Arrival Stop ID info Done', arrivalDone)
            print('Departure Stop Name', departureStopName)
            print('Departure Stop ID info Done', departureDone)
            print()
            print('*************************')

            arrivalPercentDone = temp * (float(arrivalDone['PercentDone']) / 100 )
            departurePercentDone = temp * (float(departureDone['PercentDone']) / 100)

            print('*************************')
            print()
            print('Arrival Stop Name', arrivalStopName)
            print('Arrival Stop ID Percent time', arrivalPercentDone)
            print('Departure Stop Name', departureStopName)
            print('Departure Stop ID Percent time', departurePercentDone)
            print()
            print('*************************')

            estimatedLegTime = arrivalPercentDone - departurePercentDone
            estimatedTimes.append(round(estimatedLegTime, 2))

        print('*************************')
        print()
        print('Estimated Times', estimatedTimes)
        print()
        print('*************************')

        return estimatedTimes
    
    
    def getRouteDirection(self, routeNumber, headsign):
        print('Headsign', headsign)
        print('route number', routeNumber)
        try:
            direction = AllStopsWithRoute.objects.filter(route_number=routeNumber,stop_headsign=" " + headsign).first()
            direction = model_to_dict(direction)
            print('*************************')
            print()
            print('direction', direction)
            print()
            print('*************************')

            return direction
        except AllStopsWithRoute.DoesNotExist:
            print('*************************')
            print()
            print('direction', 'did not work')
            print()
            print('*************************')
            return None

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
        try:
            user_forecast_datetime = self.forecastDatetime(travel_date, travel_time)
            print(user_forecast_datetime)
            forecast_weather = ForecastWeather.objects.get(dt_iso=user_forecast_datetime)
            return forecast_weather
        except ForecastWeather.DoesNotExist:
            return None
    
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

    def getbusInformation(self, request_body):
        journeySteps = request_body['Steps']
        j = 0
        busSteps = {}
        for i in range(len(journeySteps)):
            temp = journeySteps[i]
            if 'transit' in temp:
                transit = temp['transit']
                routeNumber = (transit['line']['short_name'])
                headsign = (transit['headsign'])
                numStop = (transit['num_stops'])
                arrivalStop = (transit['arrival_stop']['name'])
                departureStop = (transit['departure_stop']['name'])
                busNumber = (j)
                busSteps[busNumber] = {
                    'routeNumber':routeNumber, 
                    'headsign':headsign, 
                    'numStop':numStop, 
                    'arrivalStop':arrivalStop, 
                    'departureStop':departureStop
                    }
                j += 1
            else:
                print('transit not in step', i)
            i+=1
                
        print('*************************')
        print()
        print('Bus Steps', busSteps)
        print()
        print('*************************')

        return busSteps

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
        print('getPredictedEstimatedTime')
        print()
        print('*************************')
        print()
        print('inputValues', inputValues)
        print()
        print('Route', route)
        print()
        print('Direction', direction)
        print()
        print('*************************')
        
        filename = str(route) + "_" + str(direction) + "B"
        path = "../modelsNew/"+filename

        cwd = os.getcwd()
        print("CWD", cwd)
        # Load the Model back from file
        if os.path.isfile(path):
            print("success")
            with open(path, 'rb') as file:  
                # arguments used to train the model
                #'temp', 'feels_like', 'humidity', 'wind_speed', 'rain_1h', 'clouds_all',’weather_main’,’weekday’ 'Hour', 'Month'
                busRoutePickleModel = pickle.load(file)

                input_vals = np.array(inputValues)
                x_test = input_vals.reshape(1, -1)
                pred = busRoutePickleModel.predict(x_test)
                prediction = int(pred)
                print(prediction, "mins")

                return prediction

            print(busRoutePickleModel)
        else:
            print("failed")
            return "Error: Couldn't compute the prediction"


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

class LeapCard(View):
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
        