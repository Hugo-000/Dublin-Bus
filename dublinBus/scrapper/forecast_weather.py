#!/usr/bin/env python3

import requests
import os
import django
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'dublinBus.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dublinBus.settings")
django.setup()

from scrapper.models import ForecastWeather
#Add API info

#Add API info
apiKey = 'ac8d0dd5f40c8d6da60fd0785a3f75c4'
q = 'dublin'

forecast_weather_link = "http://api.openweathermap.org/data/2.5/forecast?q="+q+"&appid="+apiKey

#get response
response = requests.get(forecast_weather_link)
print("status code: ", response.status_code)

forecast_weather = response.json()
#delete object model and create a new one
ForecastWeather.objects.all().delete()
for each in forecast_weather['list']:
    try:
        w = ForecastWeather()
        w.dt = each['dt']
        w.dt_iso = each['dt_txt']
        w.temp = round(each['main']['temp'] - 273.15)
        w.temp_min = round(each['main']['temp_min'] - 273.15)
        w.temp_max = round(each['main']['temp_max']- 273.15)
        w.pressure = each['main']['pressure']
        w.humidity = each['main']['humidity']
        w.wind_speed = each['wind']['speed']
        w.wind_deg = each['wind']['deg']
        w.clouds_all = each['clouds']['all']
        w.weather_id = each['weather'][0]['id']
        w.weather_main = each['weather'][0]['main']
        w.weather_description = each['weather'][0]['description']
        w.weather_icon = each['weather'][0]['icon']
        w.save()
    except Exception as e:
        print(e)
        continue
