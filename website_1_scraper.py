#Import relevant function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os
from bs4 import BeautifulSoup
from scraper_function import wait
from scraper_function import check_duplicate
from scraper_function import scrape_ad_1
from scraper_function import get_data_mac
from scraper_function import get_data_pc
from scraper_function import setup_url_list_mac
from scraper_function import setup_url_list_pc
from scraper_function import pickle_save_mac
from scraper_function import pickle_save_pc
from scraper_function import xlsx_extract_pc
from scraper_function import xlsx_extract_mac
from scraper_function import sm_column_labels
from sys import platform
import datetime 

print("/n")
print("Advertisement scraper.")
# VARIABLES 
print("Calibrating variables...")

# Website iD = 1
site_id = 1

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
last_index = tuple_data[3]
    
print("DONE.")
print("\n")
print("Engaging main process...") 

# Set up urls and launch browser.
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
url = "website"

# Create iterable url list
if mac_pc == "win32":
    print("Recovering department list from .\\pickles\\0_websites\\1_website\\dep_list.pkl and compiling iterable url list...")
    dep_list = setup_url_list_pc(url) 
else:
    print("Recovering department list from ./pickles/0_websites/1_website/dep_list.pkl and compiling iterable url list...")
    dep_list = setup_url_list_mac(url)

#Create iterable list
iterable_dep_list = dep_list[last_index:]

print("Data found today, {date} for previous departments. Starting at index {last_index} : {url}.".format(date=date, last_index=last_index, url = dep_list[last_index]))
print("")

### SCRAPING LOOP ###
while iterable_dep_list:
    current_index = iterable_dep_list.pop(0)
    # Get Url
    driver.get(current_index)

    # Scroll down until bottom of page
    print("Scrolling down {dep}".format(dep = current_index))

    lastHeight = driver.execute_script("return document.body.scrollHeight")
    scrolls = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait()
        newHeight = driver.execute_script("return document.body.scrollHeight")
        scrolls += 1
        if newHeight == lastHeight:
            break

        lastHeight = newHeight

    print("Bottom reached.")

    wait()

    print("Scraping...")

    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")  
    users = soup.findAll("div", attrs="search_user_container")

    # Duplicates variables
    new_ad_count = 0
    global_dups_count = 0

    for u in users:
        ad = scrape_ad_1(u)
        ad.append(dep_list.index(current_index))
        if check_duplicate(ad, id_list) == False:
            id_url = [ad[0], ad[-2]]
            id_list.append(id_url)
            user_global_data.append(ad)
            new_ad_count += 1
        else: 
            global_dups_count += 1
            if ad not in dups_list:
                dups_list.append(ad)

    print("{x} duplicates found. {y} new ads found. Proportion of new is {z} %".format(x=global_dups_count, y=new_ad_count, z=(new_ad_count/len(users))*100))
    
    print("Total number of unique ads is {number}.".format(number = len(user_global_data)))

    if mac_pc == "win32":
        pickle_save_pc(site_id, id_list, user_global_data, dups_list)
    else:
        pickle_save_mac(site_id, id_list, user_global_data, dups_list)
    
    print("{dep} scraped.\n".format(dep = current_index))

    wait() 

print("All departments scraped.")
print("Closing browser...")
driver.quit()
wait()
wait()
os.system("taskkill /im firefox.exe /f")

# xlsx = input("Do you want to export unique user data to excel? Enter \"y\" to extract or press enter to pass: ")
xlsx = "y"
if xlsx == "y":
    column_labels = sm_column_labels()
    if mac_pc == "win32":
        xlsx_extract_pc(user_global_data, column_labels, site_id)
    else:
        xlsx_extract_mac(user_global_data, column_labels, site_id) 

print("ALL DONE.")
