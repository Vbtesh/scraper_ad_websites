# scraper_ads
Scraper script w/o urls

This is a version of a personal project to scrape private advertisement websites (2 websites supported) for publicly available data. Urls of websites have been removed for confidentiality.

The purpuse of the script is to compile, every day, a list of unique ads published on the website, mainly gathering the users' unique id, subscription plan and location.
The end goal is to create a base of longitudinal data to be analysed for an investigation.

Process:
- Check if pickle files (list of ids, list of ads, list of duplicates) for the current date already exists
  - If True:
    recover the files to append the data gathered by the current instance of the script.
  - Else:
    create new lists
  
- Compile a list of urls to visit (from the dep_list.py script).
  - If data for the day already exists:
    start at the last visited url (dep_list[-1])
  - Else: 
    start at the beginning of dep_list.
  
- For each url in dep_list:
    - Open a selenium webdriver instance.
    - Scroll down to the bottom of the page to load all ads available.
    - Create Soup file of the source code using BeautifulSoup.
  
    - For each ad in url:
      Scrape and return a list of the recovered data.
      Check if it is a duplicate.
        If no.
          Append it to the main list.
        Else.
          Append it to the duplicates list.
    
    - Pickle the current state of the list.

- Append the data list to a pandas dataframe and save it as .xlsx.

- Close browser
- quit()

PACKAGES AND PYTHON: 

Python version: 3.7

Packages :
  - requests
  - lxml 
  - bs4 
  - selenium
  - pandas
  - openpyxl
  - os
  - datetime
  - pickle
