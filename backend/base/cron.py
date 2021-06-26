#!/usr/bin/env python3
"""
Job Scheduling with django
https://github.com/kraiz/django-crontab
"""
import os
import subprocess
import sys

def my_scheduled_job():
  os.system("open /Users/chowsy/PycharmProjects/G1_RP_Dublin-Bus-App/backend/base/hello.txt")

def scheduling_curr_weather():
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
  sys.path.append(BASE_DIR)
  print(BASE_DIR)
  #result = subprocess.run(["source " + BASE_DIR + "/myenv/bin/activate" +";" + "python3 "+ "/Users/chowsy/PycharmProjects/G1_RP_Dublin-Bus-App/backend/base/scrapper/current_weather.py"],shell=True)
  result = subprocess.run(["source " + BASE_DIR + "/myenv/bin/activate" +";" + "python3 "+ BASE_DIR + "/backend/base/scrapper/current_weather.py"],shell=True)
  #print("Result " , result)

def scheduling_forecast_weather():
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
  sys.path.append(BASE_DIR)
  print(BASE_DIR)
  result = subprocess.run(["source " + BASE_DIR + "/myenv/bin/activate" +";" + "python3 "+ BASE_DIR + "/backend/base/scrapper/forecast_weather.py"],shell=True)

