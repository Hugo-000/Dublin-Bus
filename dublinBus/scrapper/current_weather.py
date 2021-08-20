#!/usr/bin/env python3

import requests
import os
import django
import sys

from django.conf import settings


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print("current_weather base", BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'dublinBus.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dublinBus.settings")
django.setup()

from scrapper.models import CurrentWeather
#Add API info

apiKey = settings.OPEN_WEATHER_MAPS_API_KEY
q = 'dublin'
curr_weather_link = "https://api.openweathermap.org/data/2.5/weather?q="+q+"&appid="+apiKey

#get response
response = requests.get(curr_weather_link)
print("status code: ", response.status_code)

curr_weather = response.json()
print(curr_weather['dt'])

#delete object model and create a new one
CurrentWeather.objects.all().delete()

#create instance
weather = CurrentWeather()

w = CurrentWeather()
#put the json response to the model
try:
    if curr_weather.get("rain"):
        if curr_weather.get("rain").keys() == '1h':
            rain = w['rain']['1h']
        if curr_weather.get("rain").keys() == '3h':
            rain = w['rain']['3h']
        else:
            rain = 0
    else:
        rain = 0
    w.dt = curr_weather['dt']
    w.temp = round(curr_weather['main']['temp'] - 273.15)
    w.feels_like = round(curr_weather['main']['feels_like'] - 273.15)
    w.temp_min = round(curr_weather['main']['temp_min']- 273.15)
    w.temp_max = round(curr_weather['main']['temp_max']- 273.15)
    w.pressure = curr_weather['main']['pressure']
    w.humidity = curr_weather['main']['humidity']
    w.wind_speed = curr_weather['wind']['speed']
    w.wind_deg = curr_weather['wind']['deg']
    w.clouds_all = curr_weather['clouds']['all']
    w.weather_main = curr_weather['weather'][0]['main']
    w.weather_description = curr_weather['weather'][0]['description']
    w.weather_icon = curr_weather['weather'][0]['icon']
    w.rain = rain
    print(rain)
    w.weather_id = curr_weather['weather'][0]['id']
    w.save()
except Exception as e:
    print(e)
    pass