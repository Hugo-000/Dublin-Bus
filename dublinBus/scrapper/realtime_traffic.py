#!/usr/bin/env python3

import os
import sys
import requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print("Real Time Traffic", BASE_DIR)
#"https://api.openweathermap.org/data/2.5/weather?q="+q+"&appid="+apiKey
key="x-api-key"
apiKey="ef3b82de8cfe4dc9a53bb9ee7580c071"
#r = requests.get('<MY_URI>', headers={'Authorization': 'TOK:<MY_TOKEN>'})

res = requests.get("https://api.nationaltransport.ie/gtfsrtest/?format=json",auth=HTTPDigestAuth('x-api-key', apiKey))
print(res.content)

import requests

url = "https://api.nationaltransport.ie/gtfsrtest/?format=json"

headers = {
  'x-api-key': 'ef3b82de8cfe4dc9a53bb9ee7580c071'
}

response = requests.request("GET", url, headers=headers)

print(response.text)




