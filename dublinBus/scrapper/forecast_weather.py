#!/usr/bin/env python3

import requests
import os
import django
import sys
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'dublinBus.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dublinBus.settings")
django.setup()

from scrapper.models import ForecastWeather

# Add API info
apiKey = 'ac8d0dd5f40c8d6da60fd0785a3f75c4'
q = 'dublin'

forecast_weather_link = "http://api.openweathermap.org/data/2.5/forecast?q=" + q + "&appid=" + apiKey

# get response
response = requests.get(forecast_weather_link)
print("status code: ", response.status_code)

forecast_weather = response.json()
# delete object model and create a new one
#ForecastWeather.objects.all().delete()
def validateSixDay():
    """Range smaller than today and greater than 6 days after will be filtered out"""
    sixth_day = datetime.date.today() + datetime.timedelta(days=5)
    #Range smaller than today and greater than 6 days after will be filtered out
    res = ForecastWeather.objects.filter(dt_iso__gt=sixth_day, dt_iso__lt=datetime.date.today())
    #samples1 = ForecastWeather.objects.filter(dt_iso__lte=test).delete()
    print(res)

def convertToDate(time):
    """Reformate the data into correct date"""
    dayOfWeek = datetime.datetime.fromtimestamp(time).weekday()
    month = datetime.datetime.fromtimestamp(time).month
    # int value range: 0-6, monday-sunday from api convert to format that will be used for modeling.
    weekDayConverter = {
        0: "1",
        1: "2",
        2: "3",
        3: "4",
        4: "5",
        5: "6",
        6: "7"
    }
    dayOfWeek = weekDayConverter.get(dayOfWeek)
    return {
        "dayOfWeek": dayOfWeek,
        "month": month
    }


for each in forecast_weather['list']:
    if each.get("rain"):
        if each.get("rain").keys() == '1h':
            rain = each['rain']['1h']
        if each.get("rain").keys() == '3h':
            rain = each['rain']['3h']
    else:
        rain = 0

    try:
        w = ForecastWeather()
        w.dt = each['dt']
        w.dt_iso = each['dt_txt']
        w.temp = round(each['main']['temp'] - 273.15)
        w.temp_min = round(each['main']['temp_min'] - 273.15)
        w.temp_max = round(each['main']['temp_max'] - 273.15)
        w.pressure = each['main']['pressure']
        w.humidity = each['main']['humidity']
        w.wind_speed = each['wind']['speed']
        w.wind_deg = each['wind']['deg']
        w.clouds_all = each['clouds']['all']
        w.weather_id = each['weather'][0]['id']
        w.weather_main = each['weather'][0]['main']
        w.weather_description = each['weather'][0]['description']
        w.weather_icon = each['weather'][0]['icon']
        w.feels_like = round(each['main']['feels_like'] - 273.15)
        w.rain_1h = rain
        w.weekday = convertToDate(each['dt'])['dayOfWeek']
        w.month = convertToDate(each['dt'])['month']
        w.save()
    except Exception as e:
        print(e)
        continue
#filter out database data in the end
validateSixDay()
print("Finished")