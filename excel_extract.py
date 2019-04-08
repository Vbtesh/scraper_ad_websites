from random import randint 
from time import sleep
import pandas as pd
import os 
import glob
import pickle
import datetime
import openpyxl 
from sys import platform
from scraper_function import pickle_get
from scraper_function import excel_extract
from scraper_function import six_column_labels
from scraper_function import sm_column_labels

pc_mac = platform

# Get Website ID.
site_id = input("""Which website do you need data from?
    [1] 1_website.com    [2] 2_website.com
    Answer: """)

if site_id == "1":
    site_id = 1
    url = "https://www.1_website.com"
elif site_id == "2":
    site_id = 2
    url = "https://www.2_website.com/"

print("Recovering data from {site}...".format(site = url))

last_extract = input("""Do you want the last extract data?
    [y] YES (default)   [n] NO, show me all available files
    Answer: """)

cwd = os.getcwd()
if pc_mac == "win32":
    dir_list = os.listdir(cwd + "\\pickles\\data_{id}".format(id = site_id))
    directory = cwd + "\\pickles\\data_{id}\\".format(id = site_id)
else:
    dir_list = os.listdir(cwd + "/pickles/data_{id}".format(id = site_id))
    directory = cwd + "/pickles/data_{id}/".format(id = site_id)

if last_extract == "n":
    print("Got it, printing available files...")
    # show available data
    for filename in dir_list:
        print(filename)
    while True:
        date_wished = input("""Enter the date of the file you want to extract. Format : YYYY-MM-DD.
            Enter date: """)
        file_wished = "data_" + date_wished + ".pkl"
        if file_wished in dir_list:
            file_path = directory + file_wished
            break
else: 
    file_wished = dir_list[-1]
    file_path = directory + file_wished
            

print("OK. Extracting {file}...".format(file = file_wished))
file_path = directory + file_wished
if site_id == 1:
    columns = sm_column_labels()
else:
    columns = six_column_labels()

data = pickle_get(file_path)

if pc_mac == "win32":
    final_path = cwd + "\\excel_manual_extractions\\" + "{id}_".format(id = site_id) + file_wished[:-3] + "xlsx"
else:
    final_path = cwd + "/excel_manual_extractions/" + "{id}_".format(id = site_id) + file_wished[:-3] + "xlsx"

excel_extract(data, final_path, columns)






