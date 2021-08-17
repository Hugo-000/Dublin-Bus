# from gitRepository.G1_RP_Dublin_Bus_App.dublinBus.scrapper.models import RealTimeTraffic
import re
from django.shortcuts import render
from django.template import loader, Context, Template
from django.views.generic import View
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse, request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import json

from .forms import JourneyPlannerForm

from .leap_card import leap_info

from scrapper.models import Stops, Routes, AllStopsWithRoute, ForecastWeather, CurrentWeather, Covid, RoutePrediction, RealTimeTraffic
from users.models import Addresses

import pickleModels 
import predictions
# import realTime

import datetime
import os.path
import pickle
import numpy as np

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class JourneyPlanner(View):

    def get(self, request):
        return render(request, 'journeyPlanner.html', {'form': JourneyPlannerForm()})

    def post(self, request, *args, **kwargs):
        user_id = self.getUserID(request)
        if request.content_type == "application/json":
            print('test')
            totalBusTime = self.getEstimatedTime(self.fetchJSON(request.body))
            return JsonResponse({ 'estimatedTime': totalBusTime })
        
        else:
            form = JourneyPlannerForm(request.POST)

            if form.is_valid():
                if not 'Error' in user_id:
                    user_id = user_id['ok']
                    print("User ID", user_id)
                    if self.hasAddresses(user_id):
                        favouriteForm = self.getFavouriteForm(user_id, form)
                        if not 'Error' in favouriteForm:
                            form = favouriteForm['OK']
                            print('Form', form)
                context = self.info(form, user_id)
                return render(request, 'journeyPlanner/showRoute.html', context=context)
            else:
                return render(request, 'journeyPlanner.html', { 'form': form })


    def getEstimatedTime(self, body):           
        busStepInfo = predictions.getBusStepInfo(body)
        print("bus step info",busStepInfo)
        travel_date = predictions.getTravelDate(body)
        travel_time = predictions.getTravelTime(body)
        weather = predictions.getWeather(travel_date, travel_time)
        inputValues = predictions.getInputValues(weather, travel_date, travel_time)
        busStepTimes = predictions.getBusStepTimes(busStepInfo, inputValues)
        return predictions.sumBusTimes(busStepTimes)

    def info(self, form, user_id):
        travel_date = self.getTravelDate(form)
        travel_time = self.getTravelTime(form)
        
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
        if "current" in weather:
            weather = weather["current"]
            iconFromDB = weather["weather_icon"]
        elif "forecast" in weather:
            weather = weather["forecast"]
            iconFromDB = weather["weather_icon"]
        else:
            return {"Error":"No weather information"}

        if not "error" in weather:
            iconToHTML = self.iconMatching(iconFromDB)

            context = {
                'travel_date': travel_date,
                'travel_time': travel_time,
                'form': form,
                'weather' : weather,
                'weather_icon': iconToHTML,
                'userUnix': user_unix_time
            }
            return context
        else:
            context = {
                'travel_date': travel_date,
                'travel_time': travel_time,
                'form': form,
                'weather' : "Error",
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

    def hasAddresses(self, user_id):
        try: 
            json_address = Addresses.objects.get(user_id=user_id)
            return True
        except:
            return False
    
    def isFavourite(self, address, user_id):
        favouriteAddresses = Addresses.objects.get(user_id=user_id).addresses
        if address in favouriteAddresses:    
            return True
        else:
            return False
    
    def getFavouriteAddress(self, addressName, user_id):
        favouriteAddresses = Addresses.objects.get(user_id=user_id).addresses
        address = favouriteAddresses[addressName]
        print('Address Name and address', addressName, address)
        return address
    
    def getFavouriteForm(self, user_id, form):
        origin = self.getOrigin(form)
        destination = self.getDestination(form)

        if not self.isFavourite(origin, user_id) and not self.isFavourite(destination, user_id):
            return {'Error':'Origin and Destination do not match user favourites'}

        if self.isFavourite(origin, user_id):
            origin = self.getFavouriteAddress(origin, user_id)

        if self.isFavourite(destination, user_id):
            destination = self.getFavouriteAddress(destination, user_id)

        newForm = JourneyPlannerForm({
            'origin_location': origin,
            'destination_location': destination,
            'travel_date': self.getTravelDate(form),
            'travel_time': self.getTravelTime(form)
        })
        
        return { 'OK': newForm }

    def getCleanedForm(self, form):
        cleanedForm = form.cleaned_data
        return cleanedForm
    
    def getOrigin(self, form):
        cleanedForm = self.getCleanedForm(form)
        origin = cleanedForm.get('origin_location')
        return origin

    def getDestination(self, form):
        cleanedForm = self.getCleanedForm(form)
        destination = cleanedForm.get('destination_location')
        return destination
    
    def getTravelDate( self, form):
        cleanedForm = self.getCleanedForm(form)
        travelDate = cleanedForm.get('travel_date')
        return travelDate

    def getTravelTime(self, form):
        cleanedForm = self.getCleanedForm(form)
        travelTime = cleanedForm.get('travel_time')
        return travelTime

    def getUserID(self, request):
        if request.user.is_authenticated:
            user_id = {'ok':request.user.id}
        else:
            user_id = {'Error':'User is not authenticated'}
        return user_id

class BusRoutes(View):
    def get(self, request, *args, **kwargs):
        routes=Routes.objects.all()
        #route_number_set=set(())
        #for route in routes:
            #route_number_set.add(route.route_name)
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

        return render(request, 'routes.html',{"routes_name":routes})
    def post(self, request, *args, **kwargs):
        routes=Routes.objects.all()
        route_number_set=set(())
        for route in routes:
            route_number_set.add(route.route_name)
        route_chosed = request.POST.get('route_name').split(",",1)
        route_number_chosed=route_chosed[0]
        if (len(route_chosed)==2):
            route_direction_chosed="O" if route_chosed[1]=="0" else "I"
        #route_direction_chosed=request.POST.get('direction')

        route_chosed=AllStopsWithRoute.objects.select_related('stop').filter(route_number=route_number_chosed).filter(direction=route_direction_chosed)
        #serializers.serialize("json",route_chosed)
        return render(request, 'routes.html',{"routes_name":routes,"route_Info":route_chosed})



        
        

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
        balance=dir(leap_info(leap_username,leap_password))
        print('leap card balance', balance)
        context = {
            "leap_balance" : balance["balance"],
            "leap_card_number" : balance["card_num"],
            "leap_card_status" : balance["card_status"],
            "leap_card_type" : balance["card_type"],
            "leap_credit_status" : balance["credit_status"],
            "leap_expiry_date" : balance["expiry_date"],
            "leap_issue_date" : balance["issue_date"],
            "leap_auto_topup" : balance["auto_topup"],
        }
        # context_hard = {
        #     "leap_balance" : "11",
        #     "leap_card_number" : leap_username,
        #     "leap_card_status" : "11",
        #     "leap_card_type" : "11",
        #     "leap_credit_status" : "11",
        #     "leap_expiry_date" : "11",
        #     "leap_issue_date" : "11",
        #     "leap_auto_topup" : "11",
        # }
        return render(request, 'leapCard.html', context= context)
        