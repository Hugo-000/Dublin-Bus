import pandas as pd
import numpy as np
import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from base.models import Routes

df = pd.read_csv(BASE_DIR + "/base/static/routes_dublin_bus.txt")
result = df
#get the 2nd column and 3rd column
cols = [2 , 3]
result = result[result.columns[cols]]

#Iterate row by row
for row in result.iterrows():
    try:
        #set up models instance first
        item = Routes()
        #print(row[1][0])
        item.route_number_id = row[1][0]
        item.save()
    except Exception as e:
        print("Error: " ,e)
        pass



