import datetime
import os.path
import pickle
import numpy as np

from django.forms.models import model_to_dict

from scrapper.models import AllStopsWithRoute, ForecastWeather, CurrentWeather, RoutePrediction

import pickleModels

#Function 1
def getBusStepInfo(request_body):
    journeySteps = request_body['Steps']
    busNumber = 0
    busStepInfo = {}
    for i in range(len(journeySteps)):
        step = journeySteps[i]
        if 'transit' in step:
            transit = step['transit']
            routeNumber = (transit['line']['short_name'])
            headsign = (transit['headsign'])
            routeDirection = getRouteDirection(routeNumber, headsign)
            path = getPath(routeNumber, routeDirection)
            busStepInfo[busNumber] = {
                'routeNumber':routeNumber, 
                'headsign':headsign, 
                'numStop':(transit['num_stops']), 
                'arrivalStop':(transit['arrival_stop']['name']), 
                'departureStop':(transit['departure_stop']['name']),
                'routeDirection': routeDirection,
                'path': path,
                }
            busNumber += 1
        else:
            print('transit not in step', i)
            
    print('**** getBusStepInfo *****')
    print()
    print('Bus Step Info', busStepInfo)
    print()
    print('*************************')

    return busStepInfo

#Function 2
def getTravelDate(request_body):
    travel_date = request_body['travel_date']
    return travel_date

#Function 3
def getTravelTime(request_body):
    travel_time = request_body['travel_time']
    return travel_time

#Function 4
def getWeather(travel_date, travel_time):
    if travel_date == '' and travel_time == '':
        weather = getCurrentWeather()
    else:
        weather = getForecastWeather(travel_date, travel_time)
    return weather

#Function 
def getInputValues(weather, travel_date, travel_time):
    travel_datetime = datetime.datetime.combine(travel_date, travel_time)

    print('**** getInputValues *****')
    print()
    print('type getInputValues treavel_date', type(travel_date))
    print()
    print('type getInputValues travel_time', type(travel_time))
    print()
    print('type getInputValues travel_datetime', type(travel_datetime), travel_datetime)
    print()
    print('*************************')

    month = travel_datetime.strftime('%-m')
    hour = travel_datetime.strftime('%-H')
    weekday = travel_datetime.strftime('%w')
    if weekday == '0':
        weekday = '7'
    weekdayName = travel_datetime.strftime('%a')

    print('**** getInputValues *****')
    print()
    print('Month', month)
    print('Hour', hour)
    print('weekday', type(weekday), weekday)
    print('weekday name', weekdayName)
    print()
    print('*************************')

    # Error checking required to make sure that the weather main is in the dictionary
    weatherMainDict = {"Rain": 1, "Clouds": 2,"Drizzle": 3,"Clear": 4,"Fog": 5,"Mist": 6,"Snow": 7,"Smoke": 8}

    weather['weather_main'] = weatherMainDict[weather['weather_main']]

    print('**** getInputValues *****')
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

#Function 
def getRouteTime(model, inputValues):

    print('***** getRouteTime ******')
    print()
    print('inputValues', inputValues)
    print()
    print('*************************')
    
    # arguments used to train the model
    #'temp', 'feels_like', 'humidity', 'wind_speed', 'rain_1h', 'clouds_all',’weather_main’,’weekday’ 'Hour', 'Month'
    input_vals = np.array(inputValues)
    x_test = input_vals.reshape(1, -1)
    pred = model.predict(x_test)
    routeTime = int(pred)
    print(routeTime, "mins")

    return routeTime

#Function 
def getBusStepTimes(busStepInfo, inputValues):
    print('**** getBusStepTimes ****')
    print()
    print('inputValues', inputValues)
    print('Bus Step Info', busStepInfo)
    print()
    print('*************************')

    busStepTimes = []
    
    for i in range(len(busStepInfo)):
        routeNumber = busStepInfo[i]['routeNumber']
        model = pickleModels.getPickleModel(busStepInfo[i]['path'])
        routeTime = getRouteTime(model, inputValues)
        arrivalStopName = busStepInfo[i]['arrivalStop']
        departureStopName = busStepInfo[i]['departureStop']

        arrivalStopID = [int(character) for character in arrivalStopName.split() if character.isdigit()]
        departureStopID = [int(character) for character in departureStopName.split() if character.isdigit()]

        print('**** getBusStepTimes ****')
        print()
        print('Arrival Stop Name', arrivalStopName)
        print('Arrival Stop ID', arrivalStopID)
        print('Departure Stop Name', departureStopName)
        print('Departure Stop ID', departureStopID)
        print()
        print('*************************')

        try: 
            arrivalDoneDict = model_to_dict(RoutePrediction.objects.get(StopID = arrivalStopID[-1], Route=routeNumber))
        except RoutePrediction.DoesNotExist:
            return 'Stop does not exist'
        
        try:
            departureDoneDict = model_to_dict(RoutePrediction.objects.get(StopID=departureStopID[-1], Route=routeNumber))
        except RoutePrediction.DoesNotExist:
            return 'Stop does not exist'

        print('**** getBusStepTimes ****')
        print()
        print('Arrival Stop Name', arrivalStopName)
        print('Arrival Stop ID info Done', arrivalDoneDict)
        print('Departure Stop Name', departureStopName)
        print('Departure Stop ID info Done', departureDoneDict)
        print()
        print('*************************')

        arrivalPercentDone = routeTime * (float(arrivalDoneDict['PercentDone']) / 100 )
        departurePercentDone = routeTime * (float(departureDoneDict['PercentDone']) / 100)

        print('**** getBusStepTimes ****')
        print()
        print('Arrival Stop Name', arrivalStopName)
        print('Arrival Stop ID Percent time', arrivalPercentDone)
        print('Departure Stop Name', departureStopName)
        print('Departure Stop ID Percent time', departurePercentDone)
        print()
        print('*************************')

        busStepTime = arrivalPercentDone - departurePercentDone
        busStepTimes.append(round(busStepTime, 2))

    print('**** getBusStepTimes ****')
    print()
    print('Bus Step Times', busStepTimes)
    print()
    print('*************************')

    return busStepTimes

#Function 
def getRouteDirection(routeNumber, headsign):
    print('Headsign', headsign)
    print('route number', routeNumber)
    try:
        temp = AllStopsWithRoute.objects.filter(route_number=routeNumber,stop_headsign=" " + headsign).first()
        temp = model_to_dict(temp)
        direction = temp['direction']
        print('****getRouteDirection****')
        print()
        print('direction', direction)
        print()
        print('*************************')
        return direction
    except AllStopsWithRoute.DoesNotExist:
        print('****getRouteDirection****')
        print()
        print('direction', 'did not work')
        print()
        print('*************************')
        return None

#Function 
def getCurrentWeather():
    try:
        current_weather = model_to_dict(CurrentWeather.objects.all().last())
        return current_weather
    except ForecastWeather.DoesNotExist:
        return "Current weather is not available"

#Function 
def forecastDatetime(travel_date, travel_time):
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

#Function 
def getForecastWeather(travel_date, travel_time):
    try:
        user_forecast_datetime = forecastDatetime(travel_date, travel_time)
        print(user_forecast_datetime)
        forecast_weather = model_to_dict(ForecastWeather.objects.get(dt_iso=user_forecast_datetime))
        return forecast_weather
    except ForecastWeather.DoesNotExist:
        return "Forecast weather is not available"

#Function 
def getPath(routeNumber, routeDirection):
    pathDirection = '_' + str(routeDirection) + 'B'
    filename = str(routeNumber) + pathDirection
    path = './modelsNew/' + filename
    return path








