#Import relevant function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os
from bs4 import BeautifulSoup
from scraper_function import wait
from scraper_function import check_duplicate
from scraper_function import scrape_gotds
from scraper_function import scrape_ad_2
from scraper_function import get_data_mac
from scraper_function import get_data_pc
from scraper_function import setup_url_list_mac
from scraper_function import setup_url_list_pc
from scraper_function import pickle_save_mac
from scraper_function import pickle_save_pc
from scraper_function import xlsx_extract_pc
from scraper_function import xlsx_extract_mac
from scraper_function import six_column_labels
from sys import platform  
import datetime 

print("/n")
print("Advertisement scraper.")
# VARIABLES 
print("Calibrating variables...")

# Website iD = 2
site_id = 2
 
# Operational variables
date = datetime.datetime.today().strftime('%Y-%m-%d')

# Device tracker
mac_pc = platform

# Retrieve data
if mac_pc == "win32":
    tuple_data = get_data_pc(site_id)
else:
    tuple_data = get_data_mac(site_id)

id_list = tuple_data[0]
user_global_data = tuple_data[1]
dups_list = tuple_data[2]

print("DONE.")
print("\n")
print("Engaging main process...")

# Launch browser and open url
if mac_pc == "win32":
    # driver = webdriver.Edge(executable_path=r'C:\\Utility\\BrowserDrivers\\MicrosoftWebDriver.exe')
    torexe = os.popen(r'C:\\Utility\\Browser\\Tor Browser\\Browser\\firefox.exe')
    profile = FirefoxProfile(r'C:\\Utility\\Browser\\Tor Browser\\Browser\\TorBrowser\\Data\\Browser\\profile.default')
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.socks', '127.0.0.1')
    profile.set_preference('network.proxy.socks_port', 9150)
    profile.set_preference("network.proxy.socks_remote_dns", False)
    profile.update_preferences()
    driver2 = webdriver.Firefox(firefox_profile= profile, executable_path=r'C:\\Utility\\BrowserDrivers\\geckodriver.exe')
else:
    driver2 = webdriver.Firefox() 

url = "https://www.website.com/"

print("Connecting to website...")
driver2.get(url)

# Click on age verification
print("We're in. Validating age...")

age_button = driver2.find_element_by_xpath('//a[@id="enter"]')
age_button.click()

print("Age done. Entering main page...")
wait()

print("Ok. Scrolling down... ")

lastHeight = driver2.execute_script("return document.body.scrollHeight")
scrolls = 0
wait()

while True:
    driver2.execute_script("window.scrollTo(0, 700);")
    wait()
    driver2.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait()
    newHeight = driver2.execute_script("return document.body.scrollHeight")
    scrolls += 1
    if newHeight == lastHeight:
        break
    lastHeight = newHeight

print("Bottom reached. Scrolled {x} times.".format(x = scrolls))

wait()

print("Scraping...")

html = driver2.page_source
soup = BeautifulSoup(html, "lxml")  


users = soup.findAll("div", attrs={"class" :"row"})

gotds = []
ads = []

for row in users:
    gotds += row.findAll("div", attrs={"class":"gotd-thumb h fr"})
    ads += row.findAll("div", attrs={"class":"escort h prem even"})
    ads += row.findAll("div", attrs={"class":"escort h prem odd"})
    ads += row.findAll("div", attrs={"class":"escort h even"})
    ads += row.findAll("div", attrs={"class":"escort h odd"})

print(len(gotds))
print(len(ads))

# Duplicates variables
new_ad_count = 0
global_dups_count = 0

### GOTDS ###
for u in gotds:
    ad = scrape_gotds(u)
    if check_duplicate(ad, id_list) == False:
        id_url = [ad[0], ad[-2]]
        id_list.append(id_url)
        user_global_data.append(ad)
        new_ad_count += 1
    else: 
        global_dups_count += 1
        if ad not in dups_list:
            dups_list.append(ad)

print("Girls of the month done.")
print("{x} duplicates found. {y} new ads found. Proportion of new is {z} %".format(x=global_dups_count, y=new_ad_count, z=(new_ad_count/len(gotds))*100))
print("")
print("Scraping regular ads...")
### REGULAR ADS ###
for u in ads:
    ad = scrape_ad_2(u)
    if check_duplicate(ad, id_list) == False:
        id_url = [ad[0], ad[-2]]
        id_list.append(id_url)
        user_global_data.append(ad)
        new_ad_count += 1
    else: 
        global_dups_count += 1
        if ad not in dups_list:
            dups_list.append(ad)

print("{x} duplicates found. {y} new ads found. Proportion of new is {z} %".format(x=global_dups_count, y=new_ad_count, z=(new_ad_count/(len(gotds)+len(ads)))*100))
print("Total number of unique ads is {number}.".format(number = len(user_global_data)))
print("")

if mac_pc == "win32":
    pickle_save_pc(site_id, id_list, user_global_data, dups_list)
else:
    pickle_save_mac(site_id, id_list, user_global_data, dups_list)

print("All page scraped.")
print("Closing browser...")
print("")

driver2.quit()
wait()
wait()
os.system("taskkill /im firefox.exe /f")

# xlsx = input("Do you want to export unique user data to excel? Enter \"y\" to extract or press enter to pass: ")
xlsx = "y"
if xlsx == "y":
    column_labels = six_column_labels()
    if mac_pc == "win32":
        xlsx_extract_pc(user_global_data, column_labels, site_id)
    else:
        xlsx_extract_mac(user_global_data, column_labels, site_id) 

print("ALL DONE.")