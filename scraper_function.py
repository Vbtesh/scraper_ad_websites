#Import relevant function
import requests
import csv
from lxml import html
from random import randint 
from time import sleep
import pandas as pd
import os 
import glob
import pickle
import datetime
import openpyxl 
from sys import platform

######                             #####
######  GENERAL PURPOSE FUNCTIONS  #####
######                             #####

def pickle_get(file_path):
    pickle_file = open(file_path, "rb")
    data = pickle.load(pickle_file)
    return data

def excel_extract(list_in, file_path, df_column_labels):
    file_data = pd.DataFrame(list_in, columns=df_column_labels)
    print("creating Excel file...")
    file_data.to_excel(file_path, encoding='utf-8')
    print("DONE. File saved as : {y}.".format(y = file_path))

def xlsx_extract_mac(list_in, df_column_labels, site_id):
    # name = input("Enter file name (no spaces, dots or comas): ")
    name = "data"
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    cwd = os.getcwd()

    # Create dataframe
    file_data = pd.DataFrame(list_in, columns=df_column_labels)

    print("creating Excel file...")
    file_data.to_excel(cwd + "/excel_files/excel_{w}/{x}_{y}.xlsx".format(w = site_id, x = name, y = date), encoding='utf-8')
    print("DONE. {x} file saved at : {y}/excel_files/excel_{w}/{x}_{z}.xlsx".format(w = site_id, y = cwd, x = name, z = date))

def xlsx_extract_pc(list_in, df_column_labels, site_id):
    # name = input("Enter file name (no spaces, dots or comas): ")
    name = "data"
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    cwd = os.getcwd()

    # Create dataframe
    file_data = pd.DataFrame(list_in, columns=df_column_labels)

    print("creating Excel file...")
    file_data.to_excel(cwd + "\\excel_files\\excel_{w}\\{x}_{y}.xlsx".format(w = site_id, x = name, y = date), encoding='utf-8')
    print("DONE. {x} file saved at : {y}\\excel_files\\excel_{w}\\{x}_{z}.xlsx".format(w = site_id, y = cwd, x = name, z = date))

def wait():
    sleep(randint(1, 3))

def check_duplicate(ad, id_list):
    id_number = ad[0]
    if id_number in id_list:
        #print("duplicate found. Id {number} found at index {location}.".format(number = id_number, location = id_list.index(id_number)))
        return True
    else:
        return False

def get_data_pc(site_id):
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    cwd = os.getcwd()

    try:
        print("recovering id list...")
        pickle_file = open(cwd + "\\pickles\\ids_{id}\\id_list_{date}.pkl".format(id = site_id, date=date), "rb")
        id_list = pickle.load(pickle_file)
        print("Id list recovered and has {} indices.".format(len(id_list)))
    except:
        print("no id list found for {date}, creating new id list...".format(date=date))
        id_list = []

    # Data file
    try:
        print("recovering data...")
        pickle_file = open(cwd + "\\pickles\\data_{id}\\data_{date}.pkl".format(id = site_id, date=date), "rb")
        user_global_data = pickle.load(pickle_file)
        print("Data recovered and list has {} indices.".format(len(user_global_data)))
        # Only useful for 1
        last_index = user_global_data[-1][-1]
    except:
        print("no data found for {date}, creating new array...".format(date=date))
        user_global_data = []
        last_index = False

    # Duplicates
    try:
        print("recovering id list...")
        pickle_file = open(cwd + "\\pickles\\duplicates_{id}\\dups_{date}.pkl".format(id = site_id, date=date), "rb")
        dups_list = pickle.load(pickle_file)
        print("Duplicates list recovered and has {} indices.".format(len(dups_list)))
    except:
        print("no id list found for {date}, creating new id list...".format(date=date))
        dups_list = []
    
    return id_list, user_global_data, dups_list, last_index

def get_data_mac(site_id):
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    cwd = os.getcwd()

    try:
        print("recovering id list...")
        pickle_file = open(cwd + "/pickles/ids_{id}/id_list_{date}.pkl".format(id = site_id, date=date), "rb")
        id_list = pickle.load(pickle_file)
        print("Id list recovered and has {} indices.".format(len(id_list)))
    except:
        print("no id list found for {date}, creating new id list...".format(date=date))
        id_list = []

    # Data file
    try:
        print("recovering data...")
        pickle_file = open(cwd + "/pickles/data_{id}/data_{date}.pkl".format(id = site_id, date=date), "rb")
        user_global_data = pickle.load(pickle_file)
        print("Data recovered and list has {} indices.".format(len(user_global_data)))
        # Only useful for 1
        last_index = user_global_data[-1][-1]
    except:
        print("no data found for {date}, creating new array...".format(date=date))
        user_global_data = []
        last_index = False
 
    # Duplicates
    try:
        print("recovering id list...")
        pickle_file = open(cwd + "/pickles/duplicates_{id}/dups_{date}.pkl".format(id = site_id, date=date), "rb")
        dups_list = pickle.load(pickle_file)
        print("Duplicates list recovered and has {} indices.".format(len(dups_list)))
    except:
        print("no id list found for {date}, creating new id list...".format(date=date))
        dups_list = []
    
    return id_list, user_global_data, dups_list, last_index

def pickle_save_pc(site_id, ids, data, dups):
    print("creating pickles files...")
    cwd = os.getcwd()
    date = datetime.datetime.today().strftime('%Y-%m-%d')

    pkl_file = open(cwd + "\\pickles\\ids_{id}\\id_list_{date}.pkl".format(id = site_id, date=date), "wb")
    pickle.dump(ids, pkl_file)
    #print("Id list file saved at : {cwd}\\pickles\\ids_{id}\\id_list_{date}.pkl".format(cwd = cwd, id = site_id, date=date))

    pkl_file = open(cwd + "\\pickles\\data_{id}\\data_{date}.pkl".format(id = site_id, date=date), "wb")
    pickle.dump(data, pkl_file)
    #print("Data file saved at : {cwd}\\pickles\\data_{id}\\data_{date}.pkl".format(cwd = cwd, id = site_id, date=date))

    pkl_file = open(cwd + "\\pickles\\duplicates_{id}\\dups_{date}.pkl".format(id = site_id, date=date), "wb")
    pickle.dump(dups, pkl_file)
    #print("Duplicates file saved at : {cwd}\\pickles\\duplicates_{id}\\dups_{date}.pkl".format(cwd = cwd, id = site_id, date=date))

    print("Id list, data and duplicates saved in pickles\\ids_{x}, pickles\\data_{x} and pickles\\dups_{x}.".format(x=site_id))

def pickle_save_mac(site_id, ids, data, dups):
    print("creating pickles files...")
    cwd = os.getcwd()
    date = datetime.datetime.today().strftime('%Y-%m-%d')

    pkl_file = open(cwd + "/pickles/ids_{id}/id_list_{date}.pkl".format(id = site_id, date=date), "wb")
    pickle.dump(ids, pkl_file)
    #print("Id list file saved at : {cwd}/pickles/ids_{id}/id_list_{date}.pkl".format(cwd = cwd, id = site_id, date=date))

    pkl_file = open(cwd + "/pickles/data_{id}/data_{date}.pkl".format(id = site_id, date=date), "wb")
    pickle.dump(data, pkl_file)
    #print("Data file saved at : {cwd}/pickles/data_{id}/data_{date}.pkl".format(cwd = cwd, id = site_id, date=date))

    pkl_file = open(cwd + "/pickles/duplicates_{id}/dups_{date}.pkl".format(id = site_id, date=date), "wb")
    pickle.dump(dups, pkl_file)
    #print("Duplicates file saved at : {cwd}/pickles/duplicates_{id}/dups_{date}.pkl".format(cwd = cwd, id = site_id, date=date))

    print("Id list, data and duplicates saved in pickles/ids_{x}, pickles/data_{x} and pickles/dups_{x}.".format(x=site_id))

def pickle_save_pc_sm(data):
    print("creating pickles file for {x}...".format(x=data))
    cwd = os.getcwd()
    date = datetime.datetime.today().strftime('%Y-%m-%d')

    pkl_file = open(cwd + "\\pickles\\0_websites\\1_website\\dep_list.pkl", "wb")
    pickle.dump(data, pkl_file)
    print("Id list file saved at : {cwd}\\pickles\\0_websites\\1_website\\dep_list.pkl".format(cwd=cwd))

def pickle_save_mac_sm(data):
    print("creating pickles file for {x}...".format(x=data))
    cwd = os.getcwd()
    date = datetime.datetime.today().strftime('%Y-%m-%d')

    pkl_file = open(cwd + "/pickles/0_websites/1_website/dep_list.pkl", "wb")
    pickle.dump(data, pkl_file)
    print("Id list file saved at : {cwd}/pickles/0_websites/1_website/dep_list.pkl".format(cwd=cwd))

######                             #####
######         1_FUNCTIONS         #####
######                             #####

def setup_url_list_mac(url):
    #retrive department list
    cwd = os.getcwd()
    print("recovering department list...")
    pickle_file = open(cwd + "/pickles/0_websites/1_website/dep_list.pkl", "rb")
    tag_list = pickle.load(pickle_file)
    print("Department list recovered and has {} indices.".format(len(tag_list)))

    #Create urls
    url_list = []
    for tag in tag_list:
        url_list.append(url + tag)

    return url_list

def setup_url_list_pc(url):
    #retrive department list
    cwd = os.getcwd()
    print("recovering department list...")
    pickle_file = open(cwd + "\\pickles\\0_websites\\1_website\\dep_list.pkl", "rb")
    tag_list = pickle.load(pickle_file)
    print("Department list recovered and has {} indices.".format(len(tag_list)))

    #Create urls
    url_list = []
    for tag in tag_list:
        url_list.append(url + tag)

    return url_list

def scrape_ad_1(user):

    # Get the the user's unique id
    if user.img["data-user-id"]:
        user_id = user.img["data-user-id"]
    else:
        user_id = "unknown"

    # Get the the user's pseudonyme
    if user.find(attrs={"class":"showname"}):
        user_pseudo = user.find(attrs={"class":"showname"}).text.strip()
    else:
        user_pseudo = "unknown"
    # Get the the user's status
    if user.findChild("div", attrs = {"class" : "top-x-sign"}):
        user_status = "TOP X"
    else:
        user_status = "Standard"
    # Get the the user's "rank" and "mark-exclusive status"
    user_exclusive = "none"
    if user.i:

        user_i = user.findAll("i")
        for r in user_i:
            if r.get("class") == "crown platinum-plus":
                user_rank = "crown platinum-plus"
            elif r.get("title") != None:
                user_rank = r["title"]
            else:
                user_exclusive = "mark-exclusive"
                user_rank = "none"           
    else :
        user_rank = "none"
        user_exclusive = "none"
    # Get the user's announced location
    if user.find(attrs={"class":"link"}):
        user_location = user.find(attrs={"class":"link"}).text.strip()
    else:
        user_location = "unknown"
    
    # Get the user's age and online status
    if user.find(attrs={"class":"location"}):
        user_infos = user.find(attrs={"class":"location"}).text.strip()
        user_age = ""
        user_online = False
        for l in user_infos:
            if l in ("0","1","2","3","4","5","6","7","8","9"):
                user_age += l
        if "en ligne" in user_infos:
            user_online = True
    else:
        user_age = "unknown"
        user_online = "unknown"
    
    # get the user's mark-vip status
    if user.find(attrs={"class":"mark vip"}):
        user_vip = "VIP" 
    else:
        user_vip = False

    # get the user's mark-plus status
    if user.find(attrs={"class":"mark plus"}):
        user_plus = "Plus" 
    else:
        user_plus = False

    # get the user's mark-premium status
    if user.find(attrs={"class":"mark premium"}):
        user_premium = "Premium" 
    else:
        user_premium = False
    
    # get the user's verified status
    if user.find(attrs={"class":"verified"}):
        user_verified = True
    else:
        user_verified = False
    
    # user_profile_url
    a_user = user.findAll("a")
    user_url = a_user[0]["href"]

    # Compile user data
    user_data = []
    # Users' information
    user_data.append(user_id)
    user_data.append(user_pseudo)
    user_data.append(user_location)
    user_data.append(user_age)
    user_data.append(user_online)
    # Users' status and subscription information
    user_data.append(user_status)
    user_data.append(user_rank)
    user_data.append(user_exclusive)
    user_data.append(user_verified)
    user_data.append(datetime.datetime.today().strftime('%Y-%m-%d'))
    user_data.append(user_vip)
    user_data.append(user_plus)
    user_data.append(user_premium)
    user_data.append(user_url)

    # Returns 9 user variables as a list
    return user_data

def sm_column_labels():
    column_labels = []
    column_labels.append("0_id")
    column_labels.append("1_pseudo")
    column_labels.append("2_location")
    column_labels.append("3_age")
    column_labels.append("4_online")
    column_labels.append("5_status")
    column_labels.append("6_rank")
    column_labels.append("7_exclusive")
    column_labels.append("8_verified")
    column_labels.append("9_extraction_date")
    column_labels.append("10_VIP")
    column_labels.append("11_plus")
    column_labels.append("12_premium")
    column_labels.append("13_url")
    column_labels.append("14_department_index")
    return column_labels
######                             #####
######           2_FUNCTIONS       #####
######                             #####

def scrape_gotds(user):
    # user's pseudonyme, location and age
    info_list = user.findAll("span",attrs = {"class":"strong"})
    if len(info_list) == 2:
        try:
            user_pseudo = info_list[0].text.strip()
        except:
            user_pseudo = None
        try:
            user_city = info_list[1].text.strip()
        except:
            user_city = None

        user_age = None

    else:
        try:
            user_pseudo = info_list[0].text.strip()
        except:
            user_pseudo = None

        try:
            user_age = info_list[1].text.strip()
        except:
            user_age = None

        try:
            user_city = info_list[2].text.strip()
        except:
            user_city = None

    # user's unique id
    a_user = user.findAll("a")
    ref_user = a_user[0]["href"]
    user_id = ref_user[8+len(user_pseudo)+1:]

    # user's status
    user_status = "x of the day"

    # user_profile_url
    user_url = ref_user

    # Learn about (may contain contact number or actual location)
    try:
        user_learn_about = user.find(attrs={"class":"l_about_text"}).text.strip()
    except:
        user_learn_about = "none"

    # Compile user data
    user_data = []
    # Users' information
    user_data.append(user_id)
    user_data.append(datetime.datetime.today().strftime('%Y-%m-%d'))
    user_data.append(user_pseudo)
    user_data.append(user_city)
    user_data.append(None)
    user_data.append(user_age)
    # Users' status and subscription information
    user_data.append(user_status)
    user_data.append(user_url)
    user_data.append(user_learn_about)
    user_data.append(None)
    user_data.append(None)
    user_data.append(None)
    user_data.append(None)
    user_data.append(None)

    return user_data

def scrape_ad_2(user):

    # user's unique id
    if user.img["id"]:
        user_id_raw = user.img["id"]
        user_id = user_id_raw[2:]
    else:
        user_id = "unknown"

    # user's pseudonyme
    if user.find(attrs={"class":"showname"}):
        user_pseudo = user.find(attrs={"class":"showname"}).text.strip()
    else:
        user_pseudo = "unknown"

    # user's status
    if user.findChild("span", attrs = {"class" : "diamond"}):
        user_status = "Diamond"
    elif user.findChild("span", attrs = {"class" : "gold"}):
        user_status = "Gold"
    else:
        user_status = "Standard"

    # City location
    if user.find(attrs={"class":"city"}):
        user_city_raw = user.find(attrs={"class":"city"}).text.strip()
        user_city = user_city_raw[7:]
    else:
        user_city = "location unknown"

    # City location (if in travel)
    try:
        if user.find(attrs={"class":"base-city"}):
            user_current_loc_raw = user.find(attrs={"class":"base-city"}).text.strip()
            user_current_loc = user_current_loc_raw[15:]
        else:
            user_current_loc = "not in travel"
    except:
        user_current_loc = "not in travel"

    # Last date modified (ad)
    if user.find(attrs={"class":"l_date_modified"}):
        user_l_date_modif = user.find(attrs={"class":"l_date_modified"}).text.strip()
    else:
        user_l_date_modif = "unknown"

    # Verified user 
    if user.find(attrs={"class":"p100s"}):
        user_verified = True
    else:
        user_verified = False

    # VIP
    if user.find(attrs={"class":"vip"}):
        user_vip = True
    else:
        user_vip = False

    # Suspicious
    if user.find(attrs={"class":"suspicious"}):
        user_suspect = True
    else:
        user_suspect = False

    # top 30
    if user.find(attrs={"class":"top30"}):
        user_top30 = True
    else:
        user_top30 = False

    # user profile_url
    a_user = user.findAll("a")
    user_ref = a_user[0]["href"]
    user_url = user_ref[:user_ref.index("?")]

    # Learn about (may contain contact number or actual location)
    try:
        user_learn_about = user.find(attrs={"class":"l_about_text"}).text.strip()
    except:
        user_learn_about = "none"

        # Compile user data
    user_data = []
    # Users' information
    user_data.append(user_id)
    user_data.append(datetime.datetime.today().strftime('%Y-%m-%d'))
    user_data.append(user_pseudo)
    user_data.append(user_city)
    user_data.append(user_current_loc)
    user_data.append(None)
    # Users' status and subscription information
    user_data.append(user_status)
    user_data.append(user_url)
    user_data.append(user_learn_about)
    user_data.append(user_l_date_modif)
    user_data.append(user_verified)
    user_data.append(user_vip)
    user_data.append(user_suspect)
    user_data.append(user_top30)

    return user_data

def six_column_labels():
    column_labels = []
    column_labels.append("0_id")
    column_labels.append("1_extraction_date")
    column_labels.append("2_pseudo")
    column_labels.append("3_city")
    column_labels.append("4_current_location")
    column_labels.append("5_age")
    column_labels.append("6_status")
    column_labels.append("7_url")
    column_labels.append("8_learn_about")
    column_labels.append("9_date_last_modif")
    column_labels.append("10_verified")
    column_labels.append("11_vip_2")
    column_labels.append("12_suspicious ad")
    column_labels.append("13_top30")
    return column_labels
