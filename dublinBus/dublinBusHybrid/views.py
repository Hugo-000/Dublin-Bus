from django.shortcuts import render
from django.views.generic import View
from django.http import Http404, JsonResponse
from django.conf import settings
import json

from .forms import JourneyPlannerForm
from scrapper.models import Routes, AllStopsWithRoute, Covid
from users.models import Addresses

import predictions
import datetime

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class JourneyPlanner(View):

    def get(self, request):
        context = {
            'api_key': settings.GOOGLE_MAPS_API_KEY,
            'form': JourneyPlannerForm(),
        }
        return render(request, 'journeyPlanner.html', context=context)

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
                context['api_key'] = settings.GOOGLE_MAPS_API_KEY
                return render(request, 'journeyPlanner/showRoute.html', context=context)
            else:
                context = {
                    'api_key': settings.GOOGLE_MAPS_API_KEY,
                    'form':form
                }
                return render(request, 'journeyPlanner.html', context=context)

    def getEstimatedTime(self, body):  
        """
            Function that fetches data from other functions in order to get the estimated time of each bus. 
            The function the sums the times and returns the total bus time along with a key indicating if the time
            contains any google estimated times.
        """         
        busStepInfo = predictions.getBusStepInfo(body)
        print("bus step info",busStepInfo)
        travel_date = predictions.getTravelDate(body)
        travel_time = predictions.getTravelTime(body)
        weather = predictions.getWeather(travel_date, travel_time)
        inputValues = predictions.getInputValues(weather, travel_date, travel_time)
        busStepTimes = predictions.getBusStepTimes(busStepInfo, inputValues)
        return predictions.sumBusTimes(busStepTimes)

    def info(self, form, user_id):
        """
            A function which fetches the information contained within the form and forms a context dictionary for the 
            html file. Additionally the function fetches the weather data fro the given date and time and adds it to the 
            dictionary for use in the weather card.
        """
        travel_date = self.getTravelDate(form)
        travel_time = self.getTravelTime(form)

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
        """
            Function which takes the information from the JSON link and converts it into data types which python understands 
            and returns a python dictionary
        """
        info = json.loads(request_body)
        
        info['travel_time'] = datetime.datetime.strptime(info['travel_time'], '%H:%M:%S').time()
        info['travel_date'] = datetime.datetime.strptime(info['travel_date'], '%Y-%m-%d').date()

        return info

    def toUnix(self, form):
        """
            converts the travel date and travel time into a unix timestap
        """
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
        """
            converts the weather icon values from the weather table to the images we have for the 
            weather types to be used in the weather card.
        """
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
        """
            function to determine if the user has any favourite addresses stored on the system
        """
        try: 
            json_address = Addresses.objects.get(user_id=user_id)
            return True
        except:
            return False
    
    def isFavourite(self, address, user_id):
        """
            Function to check if the address passed to it is a favourite key word.
            If so it returns True, if not it returns false
        """
        favouriteAddresses = Addresses.objects.get(user_id=user_id).addresses
        if address in favouriteAddresses:    
            return True
        else:
            return False
    
    def getFavouriteAddress(self, addressName, user_id):
        """
            Function to retirive the favourite addresses dictionary for the user from the database 
        """
        favouriteAddresses = Addresses.objects.get(user_id=user_id).addresses
        address = favouriteAddresses[addressName]
        return address
    
    def getFavouriteForm(self, user_id, form):
        """
            Function to regenerate the journeyPlannerForm after the user has entered a favourite address key word.
            This enables the google maps API to read the address required to generate the map instead of the key word.
        """
        origin = self.getOrigin(form).lower()
        destination = self.getDestination(form).lower()

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
        """
            Function to return the cleaned data from the form
        """
        cleanedForm = form.cleaned_data
        return cleanedForm
    
    def getOrigin(self, form):
        """
            function to get the origin address from the cleaned data of a form
        """
        cleanedForm = self.getCleanedForm(form)
        origin = cleanedForm.get('origin_location')
        return origin

    def getDestination(self, form):
        """
            function to get the destination address from the cleaned data of a form
        """
        cleanedForm = self.getCleanedForm(form)
        destination = cleanedForm.get('destination_location')
        return destination
    
    def getTravelDate( self, form):
        """
            function to get the travel date from the cleaned data of a form
        """
        cleanedForm = self.getCleanedForm(form)
        travelDate = cleanedForm.get('travel_date')
        return travelDate

    def getTravelTime(self, form):
        """
            function to get the travel time from the cleaned data of a form
        """
        cleanedForm = self.getCleanedForm(form)
        travelTime = cleanedForm.get('travel_time')
        return travelTime

    def getUserID(self, request):
        """
            Function to get the user id from an authenticated user
        """
        print({"getUSeR IC"})
        if request.user.is_authenticated:
            print(request.user)
            user_id = {'ok':request.user.id}
        else:
            user_id = {'Error':'User is not authenticated'}
        print(user_id)
        return user_id

class BusRoutes(View):
    def get(self, request, *args, **kwargs):
        routes=Routes.objects.all()
        context = {
            'api_key': settings.GOOGLE_MAPS_API_KEY,
            'routes_name': routes
        }
        return render(request, 'routes.html',context=context)

    def post(self, request, *args, **kwargs):
        routes=Routes.objects.all()
        route_number_set=set(())
        for route in routes:
            route_number_set.add(route.route_name)
        route_chosed = request.POST.get('route_name').split(",",1)
        route_number_chosed=route_chosed[0]
        if (len(route_chosed)==2):
            route_direction_chosed="O" if route_chosed[1]=="0" else "I"

        route_chosed=AllStopsWithRoute.objects.select_related('stop').filter(route_number=route_number_chosed).filter(direction=route_direction_chosed)
        
        context = {
            'api_key': settings.GOOGLE_MAPS_API_KEY,
            "routes_name":routes,
            "route_Info":route_chosed
        }
        return render(request, 'routes.html',context=context)
class CovidInfo(View):
    def get(self, request):
        try:
            covid_stat = Covid.objects.all().order_by('-dt')[0]
            #Get the last 14 dates records in DB
            covid_chart = Covid.objects.all().order_by('-dt')[:14][::-1]
        except Covid.DoesNotExist:
            raise Http404("Covid data does not exist")
        return render(request, 'covidInfo.html', {'covid': covid_stat,'covid_chart':covid_chart})

        