import datetime
import os.path
import pickle
from django.forms import fields
import numpy as np

from django.forms.models import model_to_dict, modelformset_factory

from scrapper.models import AllStopsWithRoute, ForecastWeather, CurrentWeather, RoutePrediction, Stops, Routes, RealTimeTraffic

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
            agency = (transit['line']['agencies'][0]['name'])
            if agency != "Dublin Bus":
                routeDirection = {'Error' : 'Cannot determine route Direction for other agencies'}
                path = {'Error': 'Only have models for Dublin Bus'}
            else:
                routeDirection = getRouteDirection(routeNumber, headsign)
                path = getPath(routeNumber, routeDirection)
            googleDirectionString = journeySteps[i]['duration']['text']
            googleDirection = [int(character) for character in googleDirectionString.split() if character.isdigit()]
            busStepInfo[busNumber] = {
                'routeNumber':routeNumber, 
                'headsign':headsign, 
                'numStop':(transit['num_stops']), 
                'arrivalStop':(transit['arrival_stop']['name']), 
                'departureStop':(transit['departure_stop']['name']),
                'routeDirection': routeDirection,
                'path': path,
                'googleDuration': googleDirection[0],
                'agency':agency,
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
    today = datetime.date.today()
    nowTime = datetime.datetime.now().time()
    time18 = datetime.time(18,0,0)
    if travel_date == today and travel_time == None:
        weather = getCurrentWeather()
    elif travel_date == today and travel_time <= nowTime:
        weather = getCurrentWeather()
    elif travel_date == today and travel_time < time18:
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

    #  ['temp', 'feels_like', 'humidity', 'wind_speed', 'rain_1h', 'clouds_all',
    #    'weather_main', 'Weekday', 'Hour', 'Month', 'TimeOfDay', 'Seasons',
    #    'RushHour']
    try:
        rain = weather['rain_1h']
    except KeyError:
        rain = 0
    print('rainfall', rain)
    InputValues = [int(weather["temp"]), 
                    int(weather['feels_like']), 
                    int(weather['humidity']),  
                    float(weather['wind_speed']),
                    rain,
                    int(weather['clouds_all']),
                    int(weather['weather_main']),
                    int(weekday),
                    int(hour),
                    int(month),
    ]

    return InputValues

#Function 
def getBusStepTimes(busStepInfo, inputValues):
    print('**** getBusStepTimes ****')
    print()
    print('inputValues', inputValues)
    print('Bus Step Info', busStepInfo)

    busStepTimes = {}
    
    for i in range(len(busStepInfo)):
        print()
        print('Loop number', i)
        print()
        routeNumber = busStepInfo[i]['routeNumber']
        routeDirection = busStepInfo[i]['routeDirection']
        arrivalStopName = busStepInfo[i]['arrivalStop']
        departureStopName = busStepInfo[i]['departureStop']
        arrivalPercentDone = getStopPercentDone(arrivalStopName, routeNumber, routeDirection)
        departurePercentDone = getStopPercentDone(departureStopName, routeNumber, routeDirection)
        model = pickleModels.getPickleModel(busStepInfo[i]['path'])

        print()
        print('route number', routeNumber)
        print('route direction', routeDirection)
        print('arrivalStopName', arrivalStopName)
        print('departureStopName', departureStopName)
        print('arrivalPercentDone', arrivalPercentDone)
        print('departurePercentDone', departurePercentDone)
        print('model', model)
        if 'Error' in model or 'Error' in arrivalPercentDone or 'Error' in departurePercentDone:
            googleEstimatedTime = busStepInfo[i]['googleDuration']
            busStepTimes[i] = {'type':'google', 'time':googleEstimatedTime}
        else:
            routeTime = getRouteTime(model['ok'], inputValues)
            arrivalTime = routeTime * arrivalPercentDone['Percent']
            departureTime = routeTime * departurePercentDone['Percent']
            busStepTime = arrivalTime - departureTime
            busStepTimes[i] = {'type':'prediction', 'time':round(busStepTime, 2)}

    print()
    print('Bus Step Times', busStepTimes)
    print()
    print('*************************')

    return busStepTimes

#Function 
def getRouteTime(model, inputValues):

    print('***** getRouteTime ******')
    print()
    print('inputValues', inputValues)
    
    # arguments used to train the model
    #'temp', 'feels_like', 'humidity', 'wind_speed', 'rain_1h', 'clouds_all',’weather_main’,’weekday’ 'Hour', 'Month'
    input_vals = np.array(inputValues)
    x_test = input_vals.reshape(1, -1)
    pred = model.predict(x_test)
    routeTime = int(pred)

    print('Route Time', routeTime, "mins")
    print()
    return routeTime

#Function
def getStopPercentDone(stopName, routeNumber, busDirection):
    stopPercentDone = {}

    stopID = [int(character) for character in stopName.split() if character.isdigit()]

    print('**** getStopPercentDone ****')
    print()
    print('routeNumber', routeNumber, 'busDirection', busDirection)
    print('stop name', stopName)

    if 'Error' in busDirection:
        return {'Error':'Bus Direction does not exist'}

    elif len(stopID) == 0:
        try:
            stopInfoList = Stops.objects.filter(stop_name__contains = stopName)
            print('success')
            print('stopInfoList: ', stopInfoList)
            print()
        except Stops.DoesNotExist:
            print('fail')
            return None
        
        stopInfoDict = {}
        routeInfoDict = {}
        routeDirectionName = model_to_dict
        for i in range(len(stopInfoList)):
            stopInfoDict[i] = model_to_dict(stopInfoList[i])
        
        print('Stop Name Information', stopInfoDict)
        print()

        for i in range(len(stopInfoDict)):
            stopID = stopInfoDict[i]['stop_id']
            print('stop id', type(stopID), stopID)
            try:
                routeInfoList = AllStopsWithRoute.objects.filter(stop = stopID, route_number = routeNumber)
                print('routeInfoList', routeInfoList)
                print()
            except:
                return None
            routeInfoDict[i] = model_to_dict(routeInfoList[0])
            print('Stop Name Route Information', routeInfoDict)
        
        print()

        for i in range(len(routeInfoDict)):
            routeDirectionName = routeInfoDict[i]['direction']
            stopIDSearch = routeInfoDict[i]['stop']
            print('Stop Name Route Direction', routeDirectionName)
            print('Stop bus route direction', busDirection)
            if routeDirectionName == busDirection:
                stopNumberList = Stops.objects.filter(stop_id = stopIDSearch)
                stopNumberDict = model_to_dict(stopNumberList[0])
                print('stop number dict', stopNumberDict)
                stopNumber = stopNumberDict['stop_number']
                print('stopNumber', stopNumber)
                try: 
                    stopDoneDict = model_to_dict(RoutePrediction.objects.get(StopID = stopNumber, Route=routeNumber))
                except RoutePrediction.DoesNotExist:
                    print('failed')
                    return {'Error':'Stop and Route combination does not exist'}
                break
    else:
        try: 
            stopDoneDict = model_to_dict(RoutePrediction.objects.get(StopID = stopID[-1], Route=routeNumber))
        except RoutePrediction.DoesNotExist:
            print('failed')
            return {'Error':'Stop and Route combination does not exist'}

    print('Stop Name', stopName)
    print('Stop ID', stopID)

    try: 
        stopDoneDict = model_to_dict(RoutePrediction.objects.get(StopID = stopID[-1], Route=routeNumber))
    except RoutePrediction.DoesNotExist:
        error = 'Stop does not exist'

    print('Stop ID info Done', stopDoneDict)
    print()

    stopPercentDone['Percent'] = float(stopDoneDict['PercentDone']) / 100

    print('Stop Percent', stopPercentDone)
    print()

    print('complete')

    return stopPercentDone

#Function
def sumBusTimes(busStepTimes):
    totalBusTimes = {}
    time = 0
    for i in range(len(busStepTimes)):
        if busStepTimes[i]['type'] == 'google':
            print('google')
            totalBusTimes['type'] = 'google'
        else:
            print('predictions')
            totalBusTimes['type'] = 'predictions'
        time += busStepTimes[i]['time']
    totalBusTimes['time'] = time
    return totalBusTimes

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








