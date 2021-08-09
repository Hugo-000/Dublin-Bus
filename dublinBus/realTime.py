import datetime
import os.path
import predictions

from django.forms.models import model_to_dict, modelformset_factory

from scrapper.models import AllStopsWithRoute, ForecastWeather, CurrentWeather, RoutePrediction, Stops, Routes, RealTimeTraffic

def getDepartureStopName(busInfo):
    departureStopName = busInfo['departureStop']
    return departureStopName

def getArrivalStopName(busInfo):
    arrivalStopName = busInfo['arrivalStop']
    return arrivalStopName

def getRouteNumber(busInfo):
    routeNumber = busInfo['routeNumber']
    return routeNumber

def getRouteDirection(busInfo):
    routeDirection = busInfo['routeDirection']
    return routeDirection

def getStopID(stopName, routeNumber, routeDirection):
    stopNumber = predictions.getStopNumber(stopName, routeNumber, routeDirection)
    stopID = predictions.getStopID(stopNumber)

def getRealTimeStopInfo(stopID):
    try:
        realTimeStopInfo = model_to_dict(RealTimeTraffic.objects.filter(stop_id = stopID))
    except:
        print('real time sop info failed')
        return None
    return realTimeStopInfo
    
def getRealTimeInfo(busStepInfo):
    realTimeInfo = {}
    for i in busStepInfo:
        busInfo = busStepInfo[i]
        departureStopName = getDepartureStopName(busInfo)
        routeNumber = getRouteNumber(busInfo)
        routeDirection = getRouteDirection(busInfo)
        stopID = getStopID(departureStopName, routeNumber, routeDirection)
        realTimeStopInfo = getRealTimeStopInfo(stopID)
        realTimeInfo[i] = realTimeStopInfo
        print('**** getRealTimeInfo ****')
        print()
        print('real time info', realTimeInfo)
        print()
        print('*************************')
    return realTimeInfo

