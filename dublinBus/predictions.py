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
    print('type getInputValues travel_time', type(travel_time), travel_time)
    print()
    print('type getInputValues travel_datetime', type(travel_datetime), travel_datetime)
    print()
    print('*************************')

    rushHour = ifRushHour(travel_time)
    timeOfDay = getTimeOfDay(travel_time)
    season = getSeason(travel_date)
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

    if "current" in weather:
        weather['current']['weather_main'] = weatherMainDict[weather['current']['weather_main']]
        rain = int(weather['current']['rain'])
        temp = int(weather['current']["temp"])
        feels_like = int(weather['current']['feels_like']) 
        humidity = int(weather['current']['humidity'])
        wind_speed = float(weather['current']['wind_speed'])
        clouds_all = int(weather['current']['clouds_all'])
        weather_main = int(weather['current']['weather_main'])
    elif "forecast" in weather:
        weather['forecast']['weather_main'] = weatherMainDict[weather['forecast']['weather_main']]
        rain = int(weather['forecast']['rain_1h'])
        temp = int(weather['forecast']["temp"])
        feels_like = int(weather['forecast']['feels_like']) 
        humidity = int(weather['forecast']['humidity'])
        wind_speed = float(weather['forecast']['wind_speed'])
        clouds_all = int(weather['forecast']['clouds_all'])
        weather_main = int(weather['forecast']['weather_main'])
    else:
        print("Weather has an error")
        return {"Error":"Couldn't get the weather data"}

    #  ['temp', 'feels_like', 'humidity', 'wind_speed', 'rain_1h', 'clouds_all',
    #    'weather_main', 'Weekday', 'Hour', 'Month', 'TimeOfDay', 'Seasons',
    #    'RushHour']


    InputValues = [
        temp, 
        feels_like, 
        humidity,  
        wind_speed,
        rain,
        clouds_all,
        weather_main,
        int(weekday),
        int(hour),
        int(month),
        timeOfDay,
        season,
        rushHour,
    ]

    return InputValues

def ifRushHour(travelTime):
    """ If time between 07:00 - 09:00 and 16:00 - 19:00 then it is during rush hour"""
    time9 = datetime.time(9,0,0)
    time7 = datetime.time(7,0,0)
    time16 = datetime.time(16,0,0)
    time19 = datetime.time(19,0,0)
    if time7 < travelTime < time9:
        return 1
    elif time16 < travelTime < time19:
        return 1
    else:
        return 0

def getSeason(travelDate):
    seasonsDict =  {1: "Spring", 2: "Summer", 3: "Autumn", 4: "Winter"}
    travelMonth = travelDate.month
    print('travel month', travelMonth)
    if 2 <= travelMonth <= 5:
        season = 1
    elif 6 <= travelMonth <= 8:
        season = 2
    elif 11 <= travelMonth <= 1:
        season = 4
    else:
        season = 3
    print('season', season, seasonsDict[season])
    return season

def getTimeOfDay(travelTime):
    timeOfDayDict = {"Morning": 1, "Afternoon": 2,"Evening": 3,"Night": 4}
    time7 = datetime.time(7,0,0)
    time11 = datetime.time(11,0,0)
    time15 = datetime.time(15,0,0)
    time23 = datetime.time(23,0,0)
    if time7 <= travelTime < time11:
        return 1
    elif time11 <= travelTime < time15:
        return 2
    elif time15 <= travelTime < time23:
        return 3
    else:
        return 4

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
        if 'Error' in model or 'Error' in arrivalPercentDone or 'Error' in departurePercentDone or 'Error' in inputValues:
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
    #'temp', 'feels_like', 'humidity', 'wind_speed', 'rain_1h', 'clouds_all',’weather_main’,’weekday’ 'Hour', 'Month', timeOfDay, Season, rushhour

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

    print('**** getStopPercentDone ****')
    print()
    print('routeNumber', routeNumber, 'busDirection', busDirection)
    print('stop name', stopName)

    stopNumber = getStopNumber(stopName, routeNumber, busDirection)
    # stopID = getStopID(stopNumber)

    print('Stop Number', stopNumber, type(stopNumber))
    # print('Stop ID', stopID, type(stopID))

    if stopNumber == None or 'Error' in stopNumber:
        return {'Error':'Number could not be found'}
    else:    
        try: 
            stopDoneDict = model_to_dict(RoutePrediction.objects.get(
                StopID = stopNumber['OK'],
                Route=routeNumber,
                Direction=busDirection + "B"
            ))
        except RoutePrediction.DoesNotExist:
            print('failed')
            return {'Error':'Stop and Route combination does not exist'}

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
        return {"current" : current_weather}
    except ForecastWeather.DoesNotExist:
        return {"Error":"Current weather is not available"}

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
        return {"forecast" : forecast_weather}
    except ForecastWeather.DoesNotExist:
        return {"Error" : "Forecast weather is not available"}

#Function 
def getPath(routeNumber, routeDirection):
    pathDirection = '_' + str(routeDirection) + 'B'
    filename = str(routeNumber) + pathDirection
    path = './modelsNew/' + filename
    return path

#Function
def getStopNumber(stopName, routeNumber, busDirection):
    stopNumberList = [int(character) for character in stopName.split() if character.isdigit()]
    
    if 'Error' in busDirection:
        # print('Error in the direction')
        return {'Error': 'Bus Direction does not exist'}
    
    if len(stopNumberList) != 0:
        # stopNumber = stopNumberList[0]
        # print('stop number', stopNumber)
        # print('stop number complete')
        return {'OK': stopNumberList[0]}

    # print('Stop number is empty')
    try:
        stopInfoList = Stops.objects.filter(stop_name__contains = stopName)
        # print('success')
        # print('stopInfoList: ', stopInfoList)
        # print()
    except Stops.DoesNotExist:
        # print('fail')
        return {'Error': 'Could not find stop numbers'}

    stopInfoDict = {}
    routeInfoDict = {}
    for i in range(len(stopInfoList)):
        stopInfoDict[i] = model_to_dict(stopInfoList[i])
    
    # print('Stop Name Information', stopInfoDict)
    # print()

    for i in range(len(stopInfoDict)):
        stopID = stopInfoDict[i]['stop_id']
        # print('stop id', type(stopID), stopID)
        try:
            routeInfoList = AllStopsWithRoute.objects.get(stop = stopID, route_number = routeNumber)
            # print('routeInfoList', routeInfoList.first())
            # print()
        except:
            return None

        # TODO: Handle routeInfoList being emoty
        routeInfoDict[i] = model_to_dict(routeInfoList.first())
        # print('Stop Name Route Information', routeInfoDict)
    
    # print()

    for i in range(len(routeInfoDict)):
        routeDirectionName = routeInfoDict[i]['direction']
        stopIDSearch = routeInfoDict[i]['stop']
        # print('Stop Name Route Direction', routeDirectionName)
        # print('Stop bus route direction', busDirection)
        if routeDirectionName == busDirection:
            # print('Directions Equal')
            stopNumberList = Stops.objects.filter(stop_id = stopIDSearch)
            stopNumberDict = model_to_dict(stopNumberList[0])
            # print('stop number dict', stopNumberDict)
            # stopNumber = stopNumberDict['stop_number']
            # print('stopNumber', stopNumber)
            # print('stop number complete')
            return {'OK': stopNumberDict['stop_number']}
    
    
#Function
def getStopID(stopNumber):
    print('stop number', stopNumber['OK'])
    if 'Error' in stopNumber or stopNumber == '':
        return{'Error': 'Stop ID could not be retrieved'}
    try:
        stopInfo = Stops.objects.filter(stop_number = stopNumber['OK'])
    except Stops.DoesNotExist:
        return{'Error': 'Stop ID could not be retrieved'}
    print('stopInfo', stopInfo)
    stopInfoDict = model_to_dict(stopInfo[0])
    print('StopInfoDict', stopInfoDict)
    stopID = stopInfoDict['stop_id']
    return stopID