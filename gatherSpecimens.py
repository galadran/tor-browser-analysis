
#Using Firefox and Tor Firefox. 
#Fetch each website, spider it a few times. 
#Record the path and timings / resources / measurements. 
#Purpose of Tor Firefox is to check repeatability cheaply. 
#Store in a table as blobl (id - base url - list of links.)

# open list of urls for testing

from random import choice
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException,JavascriptException,WebDriverException,StaleElementReferenceException
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm

# def checkSpecimen(path,drivers):
#     #Given a session, run it through each driver
#     if len(path) == 0:
#         return False
#     for i in range(len(path)):
#         for d in drivers:
#             try:
#                 d.get(path[i])
#                 links = d.find_elements_by_tag_name('a')
#                 linkURLs = map(lambda x: x.get_attribute('href'),links)
#                 if i+1 == len(path) or path[i+1] in linkURLs:
#                     continue
#                 else:
#                     return False
#             except Exception as E:
#                 print('Error checking ' +str(E))
#                 return False
#     return True

def genSpecimen(baseURL,driver):
    #Given a url, create a specimen session 
    driver.set_page_load_timeout(15)
    maxLength = 5
    length = 0
    currentURL = baseURL
    path = []
    try:
        while length < maxLength:
            length += 1
            print('Fetching: '+str(currentURL))
            driver.get(currentURL) 
            path.append(currentURL)
            currentURL = None
            while currentURL is None or currentURL is "" or 'https' not in currentURL:
                links = list(driver.find_elements_by_tag_name('a'))
                if len(links) == 0:
                    return path
                currentURL = choice(links).get_attribute('href')
    except Exception as E:
        print('Error generating ' +str(E))
        return path
    return path 

def getFirefoxDriver():
    profile = webdriver.FirefoxProfile()
    profile.set_preference('privacy.trackingprotection.enabled',True)
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options,firefox_profile=profile)
    return driver

with open('markMeasureResultsTP.txt', 'r') as url_file:
    test_urls = url_file.readlines()

firefox = getFirefoxDriver()
firefoxTor = ""
torBrowser = ""
drivers = [firefox]#,firefoxTor,torBrowser]
specimens = list()
for url in tqdm(test_urls):
    specimen = genSpecimen(url.replace('\n',''),firefox)
    specimens.extend(specimen)

with open('specimenSession.txt','w') as out_file:
    for p in specimens:
        out_file.write(p.replace('\n','')+'\n')