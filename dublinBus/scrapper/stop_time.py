#!/usr/bin/env python3

import os
import sys
import csv
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print("Real Time Traffic", BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'dublinBus.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dublinBus.settings")
django.setup()

from scrapper.models import Agency, StopTimes, Trips, Routes, Stops

agency = "../../../../group1/google_transit_combined/agency.txt"
routes = "../../../../group1/google_transit_combined/routes.txt"
shapes = "../../../../group1/google_transit_combined/shapes.txt"
stop_times = "../../../../group1/google_transit_combined/stop_times.txt"
stops = "../../../../group1/google_transit_combined/stops.txt"
transfers = "../../../../group1/google_transit_combined/transfers.txt"
trips = "../../../../group1/google_transit_combined/trips.txt"

fileList = [agency, routes, shapes, stop_times, stops, transfers, trips]

cwd = os.getcwd()
print("CWD", cwd)

# Agencies

# if os.path.isfile(agency):
#     print("success", agency)
#     print()
#     with open(agency) as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         linecount = 0
#         for row in csv_reader:
#             if linecount == 0:
#                 linecount += 1
#                 continue
#             else:
#                 # create instance in db
#                 linecount += 1
#                 print('row 0', row[0])
#                 agency_id = row[0]
#                 agency_name = row[1]
#                 Agency.objects.create(agency_id=agency_id, agency_name=agency_name)
#         print("LineCount", linecount)
        
# else:
#     print("failed")
#     print()
#     error = "Couldn't load in the file"

# Stop times

if os.path.isfile(stop_times):
    print("success", stop_times)
    print()
    with open(stop_times) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        linecount = 0
        for row in csv_reader:
            if linecount == 0:
                linecount += 1
                continue
            else:
                print(linecount)
                linecount += 1
                trip_id = row[0]
                arrival_time = row[1]
                departure_time = row[2]
                stop_id = row[3]
                stop_sequence = row[4]
                StopTimes.objects.create(
                    trip_id=trip_id, 
                    arrival_time=arrival_time,
                    departure_time=departure_time,
                    stop_id=stop_id,
                    stop_sequence=stop_sequence
                    )
        print("LineCount", linecount)
        print('finished stoptime')
        
else:
    print("failed")
    print()
    error = "Couldn't load in the file"

# # Trips 

# if os.path.isfile(trips):
#     print("success", trips)
#     print()
#     with open(trips) as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         linecount = 0
#         selectedlinecount = 0
#         for row in csv_reader:
#             if linecount == 0:
#                 linecount += 1
#                 continue
#             else:
#                 print(linecount)
#                 linecount += 1
#                 if row[0].startswith("60-"):
#                     Trips.route_id = row[0]
#                     Trips.service_id = row[1]
#                     Trips.trip_id = row[2]
#                     Trips.trip_headsign = row[4]
#                     Trips.direction_id = row[5]
#                     selectedlinecount += 1
#                 elif row[0].startswith("2-"):
#                     Trips.route_id = row[0]
#                     Trips.service_id = row[1]
#                     Trips.trip_id = row[2]
#                     Trips.trip_headsign = row[4]
#                     Trips.direction_id = row[5]
#                     selectedlinecount += 1
#                 elif row[0].startswith("17-"):
#                     Trips.route_id = row[0]
#                     Trips.service_id = row[1]
#                     Trips.trip_id = row[2]
#                     Trips.trip_headsign = row[4]
#                     Trips.direction_id = row[5]
#                     selectedlinecount += 1
#                 else:
#                     continue
                
            
#         print("LineCount", linecount)
#         print("SelectedLineCount", selectedlinecount)
#         print("finished")
        
# else:
#     print("failed")
#     print()
#     error = "Couldn't load in the file"
