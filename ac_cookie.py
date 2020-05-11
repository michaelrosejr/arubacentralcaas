#!/usr/bin/env python3 

import requests
import logging
import json, pickle
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import central_config as cfg

logging.basicConfig(level=logging.DEBUG)

#
# Edit the config.py
#
#
# This script uses Selenium to login to Aruba Central to grab the cookie that is needed for the CaaS API
# Please set your username and password here.
# If your central instances is configured for SSO, it is recommended you create a local account
#

# Set webdriver for Selenium
if cfg.webbrowser == "Firefox":
    driver = webdriver.Firefox()
elif cfg.webbrowser == "Chrome":
    driver = webdriver.Chrome()

# Connect to the URL and get data
driver.get(cfg.url)

# Login
driver.find_element_by_id("email").send_keys(cfg.username)
driver.find_element_by_id("signIn_button").click()
driver.find_element_by_id("password").send_keys(cfg.password)
driver.find_element_by_id("signIn_button").click()


#
# Begin - Customer Selector
#
wait = WebDriverWait(driver, 10)
timeout = 5  # seconds
try:
    element_present = EC.presence_of_element_located((By.ID, cfg.account_selection))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")
# wait.until(EC.title_is('Select Account'))
driver.find_element_by_id(cfg.account_selection).click()
#
# End - Customer Selector
#


#
# Code to select the Netowrk Operations page from the Account Home.
# This may not be necessary as there's a cookie set, but unknown if Netowrk Operations generates
# a new cookie or not
#
try:
    element_present = EC.presence_of_element_located(
        (By.CSS_SELECTOR, ".app-details-container-big:nth-child(1) .app-details-button")
    )
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")
driver.find_element_by_css_selector(
    ".app-details-container-big:nth-child(1) .app-details-button"
).click()

# Get cookies and save them to a file
pickle.dump(driver.get_cookies(), open(cfg.cookie_file, "wb"))

print("If there werent any issues, then you can now run caas.py. Please note that the Aruba Central cookies expire after 15min if idle")