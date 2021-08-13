#!/usr/bin/env python3

import os
import sys
import requests
import django
from datetime import datetime
import time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print("Real Time Traffic", BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'dublinBus.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dublinBus.settings")
django.setup()

from scrapper.models import RealTimeTraffic

url = "https://api.nationaltransport.ie/gtfsrtest/?format=json"

headers = {
  'x-api-key': 'ef3b82de8cfe4dc9a53bb9ee7580c071'
}

start_request = False

while not start_request:
  res = requests.request("GET", url, headers=headers)
  print("Status code: ", res.status_code)
  if res.status_code == 200:
    start_request = True
    result = res.json()
    realtime_list = result['entity']
  else:
    print("sleep ofr 60 s")
    time.sleep(60)

#RealTimeTraffic.objects.all().delete()
# To delete the first Nth rows of table
RealTimeTraffic.objects.filter(id__in=list(RealTimeTraffic.objects.values_list('pk', flat=True)[:1000])).delete()
for each_trip in realtime_list:
  try:
    #print(each_trip)
    route_number = each_trip['trip_update']['trip']['route_id']
    print(route_number)
    route_number = route_number.split('-')[1]
    print(route_number)
    direction = each_trip['trip_update']['trip']['trip_id']
    direction = direction.split('.')[4]
    print(direction)
    start_time = each_trip['trip_update']['trip']['start_time']
    current_time = datetime.now().strftime("%H:%M:%S")
    print(current_time)
    start_date = each_trip['trip_update']['trip']['start_date']
    trip_schedule = each_trip['trip_update']['trip']['schedule_relationship']
    if 'stop_time_update' in each_trip['trip_update'].keys():
      stops_time_update = each_trip['trip_update']['stop_time_update']
      for each_stop in stops_time_update:
        # create instance in db
        each = RealTimeTraffic()
        #if there is delay key
        if 'departure' in each_stop.keys():
          if 'delay' in each_stop['departure'].keys():
            each.stop_departure_delay = int(each_stop['departure']['delay']) / 60
        #if there is arrival key
        if 'arrival' in each_stop.keys():
          if 'delay' in each_stop['arrival'].keys():
            each.stop_arrival_delay = int(each_stop['arrival']['delay']) / 60
        each.stop_id = each_stop['stop_id']
        print("sch",each_stop['schedule_relationship'])
        each.stop_schedule = each_stop['schedule_relationship']
        each.route_number = route_number
        each.direction = direction
        each.start_time = start_time
        each.start_date = start_date
        each.trip_schedule = trip_schedule
        each.save()
  except Exception as e:
    print("Error: ", e)
    continue

print("Finished")

