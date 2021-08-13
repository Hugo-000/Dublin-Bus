#!/usr/bin/env python3

import requests
import os
import django
import sys
import pandas

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print("covid data base", BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'dublinBus.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dublinBus.settings")
django.setup()

from scrapper.models import Covid
#Add API info
url_covid = "https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/CovidStatisticsProfileHPSCIrelandOpenData/FeatureServer/0/query?where=1%3D1&outFields=Date,RequiringICUCovidCases,CommunityTransmission,TotalConfirmedCovidCases,TotalCovidDeaths,ConfirmedCovidCases,ConfirmedCovidDeaths,CloseContact,StatisticsProfileDate,FID,TravelAbroad,HospitalisedCovidCases&outSR=4326&f=json"

# get json response
res = requests.get(url_covid)
print("Status code: ", res.status_code)
covid = res.json()
featureList = covid['features']

# delete records anyway
Covid.objects.all().delete()

try:
    for each in featureList:
        # create an instace for ecery loop
        c = Covid()
        attribute = each["attributes"]
        d = attribute["Date"]
        c.dt = (str(pandas.to_datetime(d, unit='ms')))[:10]
        c.icu = attribute["RequiringICUCovidCases"]
        c.totalConfirmedCases = attribute["TotalConfirmedCovidCases"]
        c.totalDeaths = attribute["TotalCovidDeaths"]
        c.confirmedCases = attribute["ConfirmedCovidCases"]
        c.confirmedDeaths = attribute["ConfirmedCovidDeaths"]
        c.statisticsProfileDt = attribute["StatisticsProfileDate"]
        c.fid = attribute["FID"]
        c.hospitalisedCases = attribute["HospitalisedCovidCases"]
        c.save()
except Exception as e:
    print(e)
    pass

print("Finished")
