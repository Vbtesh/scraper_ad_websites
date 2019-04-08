from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from scraper_function import wait
from scraper_function import pickle_save_pc_sm
from scraper_function import pickle_save_mac_sm
import pickle 
import os
from sys import platform
import datetime

mac_pc = platform
if mac_pc == "win32":
    # driver = webdriver.Edge(executable_path=r'C:\\Utility\\BrowserDrivers\\MicrosoftWebDriver.exe')
    torexe = os.popen(r'C:\\Utility\\Browser\\Tor Browser\\Browser\\firefox.exe')
    profile = FirefoxProfile(r'C:\\Utility\\Browser\\Tor Browser\\Browser\\TorBrowser\\Data\\Browser\\profile.default')
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.socks', '127.0.0.1')
    profile.set_preference('network.proxy.socks_port', 9150)
    profile.set_preference("network.proxy.socks_remote_dns", False)
    profile.update_preferences()
    driver = webdriver.Firefox(firefox_profile= profile, executable_path=r'C:\\Utility\\BrowserDrivers\\geckodriver.exe')
else:
    driver = webdriver.Firefox() 

url = "https://www.website.com/"
driver.get(url)

# Click on age verification
age_button = driver.find_element_by_xpath('//a[@class="save"]')
age_button.click()

wait()

# Toggle department summary
dep_button = driver.find_element_by_xpath('//a[@href="#s_departments"]')
dep_button.click()

wait()

# Click on full department list
all_dep_button = driver.find_element_by_xpath('//a[@href="/all-departments-females/"]')
all_dep_button.click()

# Scrape for url list
html = driver.page_source
soup = BeautifulSoup(html, "lxml")

dep_dict = soup.findAll("div", attrs = {"id":"s_departments"})
deps = dep_dict[0]
deps_a = deps.findAll("a")

# Create url list
deps_url = []
for d in deps_a:
    deps_url.append(d["href"])

# Delete last item (not a department url)
deps_url.pop()

print(len(deps_url))

# Add males and couples
couples = "/profiles/couples/"
males = "/profiles/males/"

deps_url.append(couples)
deps_url.append(males)

print(len(deps_url))

# Create pickle file for future use
if mac_pc == "win32":
    pickle_save_pc_sm(deps_url)
else:
    pickle_save_mac_sm(deps_url)
    


driver.quit()
wait()
wait()
os.system("taskkill /im firefox.exe /f")