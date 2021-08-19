#!/usr/bin/env python3
"""
This script file is automated scripting file to run the weather scrapping once a day and insert it into database.
Job Scheduling with django
Reminder: To set up the correct path of virtualenv
https://github.com/kraiz/django-crontab
"""
import os
import subprocess
import sys

def my_scheduled_job():
  os.system("open /Users/chowsy/PycharmProjects/G1_RP_Dublin-Bus-App/backend/base/hello.txt")

def scheduling_curr_weather():
  print("testing current weather is running")
  
  #print("testing venv", getcwd())


  BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
  print("Base_DIR", BASE_DIR)
  sys.path.append(BASE_DIR)
  print(BASE_DIR)
  #result = subprocess.run(["source " + BASE_DIR + "/myenv/bin/activate" +";" + "python3 "+ "/Users/chowsy/PycharmProjects/G1_RP_Dublin-Bus-App/backend/base/scrapper/current_weather.py"],shell=True)
  #result = subprocess.run(["source " + BASE_DIR + "/myenv/bin/activate" +";" + "python3 "+ BASE_DIR + "/dublinBus/scrapper/current_weather.py"],shell=True)
  #,env={"PATH":'~/venv/bin/activate'},
  result = subprocess.run(["source ~/venv/bin/python3" +";" + "~/venv/bin/python3 "+ BASE_DIR + "/dublinBus/scrapper/current_weather.py"],shell=True)
  print("Result " , result)
  print("check return code", result.check_returncode())
  print()
  print()
  print()

def scheduling_forecast_weather():
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
  sys.path.append(BASE_DIR)
  print(BASE_DIR)
  #result = subprocess.run(["source " + BASE_DIR + "/myenv/bin/activate" +";" + "python3 "+ BASE_DIR + "/dublinBus/scrapper/forecast_weather.py"],shell=True)
  result = subprocess.run([ "source ~/venv/bin/python3" +";" + "~/venv/bin/python3 "+BASE_DIR + "/dublinBus/scrapper/forecast_weather.py"],shell=True)

def realtime_traffic():
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
  sys.path.append(BASE_DIR)
  print(BASE_DIR)
  #result = subprocess.run(["source " + BASE_DIR + "/myenv/bin/activate" +";" + "python3 "+ BASE_DIR + "/dublinBus/scrapper/realtime_traffic.py"],shell=True)
  result = subprocess.run([ "source ~/venv/bin/python3" +";" + "~/venv/bin/python3 "+BASE_DIR + "/dublinBus/scrapper/realtime_traffic.py"],shell=True)

def covid_data():
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
  sys.path.append(BASE_DIR)
  print(BASE_DIR)
  #result = subprocess.run(["source " + BASE_DIR + "/myenv/bin/activate" +";" + "python3 "+ BASE_DIR + "/dublinBus/scrapper/covid_data.py"],shell=True)
  result = subprocess.run([ "source ~/venv/bin/python3" +";" + "~/venv/bin/python3 "+BASE_DIR + "/dublinBus/scrapper/covid_data.py"],shell=True)

