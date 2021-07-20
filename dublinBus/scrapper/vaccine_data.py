#!/usr/bin/env python3

import os
import sys
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print("vaccine base", BASE_DIR)

res = requests.get("https://covid-19.geohive.ie/pages/vaccinations")

#print(res.status_code)
res = res.text
from shutil import which
from selenium import webdriver
FIREFOXPATH = which("firefox")
CHROMEPATH = which("chrome") or which("chromium")
def init_webdriver():
    """Simple Function to initialize and configure Webdriver"""
    if FIREFOXPATH != None:
        print(FIREFOXPATH)#cm
        from selenium.webdriver.firefox.options import Options

        options = Options()
        options.binary = FIREFOXPATH
        options.add_argument("-headless")
        return webdriver.Firefox(firefox_options=options, log_path="geckodriver.log")

    elif CHROMEPATH != None:
        print(CHROMEPATH)#cm
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.binary_location = CHROMEPATH
        options.add_argument("--headless")
        return webdriver.Chrome(chrome_options=options, service_args=['--verbose'], service_log_path="chromedriver.log")

driver = init_webdriver()
driver.close()
options = Options()
options.page_load_strategy = 'eager'
driver = webdriver.Firefox(firefox_options=options, executable_path='/path/to/geckodriver')
driver.get("https://covid-19.geohive.ie/pages/vaccinations")

soup = BeautifulSoup(driver.page_source, "html.parser")
div = soup.find_all('body')
print(div)
driver.close()
#print(soup.prettify())

#print(soup.body.div)



