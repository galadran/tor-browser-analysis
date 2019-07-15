import time
import csv
import random
import json
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException,JavascriptException,WebDriverException
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm


profile = webdriver.FirefoxProfile()
profile.set_preference('privacy.trackingprotection.enabled',True)
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options,firefox_profile=profile)

# open list of urls for testing
with open('markMeasureResults.txt', 'r') as url_file:
    test_urls = url_file.readlines()

driver.set_page_load_timeout(15)

# do 10 runs
uses = 0
notUses = 0
inconclusive = 0
f = open('markMeasureResultsTP.txt','w')
for url in tqdm(test_urls):  
    url = url.replace('\n','')        
    try:
        # request url from list
        #print("Fetching " + str(url),end='')
        if 'https://' not in url:
            url = 'https://' + url 
        driver.get(url) 
        # pull window.performance.timing after loading the page and add information about url and number of run
        perf_timings = driver.execute_script("return window.performance.getEntries()")
        #print(perf_timings)
        entryTypes = set(map(lambda x : x['entryType'],perf_timings))
        if 'mark' in entryTypes or 'measure' in entryTypes:
            #print(url + ' uses mark/measure')
            f.write(url + '\n')
            f.flush()
            uses += 1
        else:
            #print(url + ' does not use mark/measure')
            notUses += 1
        #Put in Database(url)
    except JavascriptException as E: 
        #print("Failed to load page " + str(url) + ' Javascript Error: '+ str(E))
        inconclusive += 1 
    except TimeoutException as E: # what to do in case that an exception is thrown (which happens usually upon page load timeout)
        # also pull data and store it to the results file
        #print("Failed to load page " + str(url) + ' Error: '+ str(E))
        try:
            perf_timings = driver.execute_script("return window.performance.getEntries()")
        except: 
            inconclusive += 1
            continue 
        entryTypes = set(map(lambda x : x['entryType'],perf_timings))
        if 'mark' in entryTypes or 'measure' in entryTypes:
            #print(url + ' uses mark/measure')
            f.write(url + '\n')
            f.flush()
            uses += 1
        else:
            #print(url + ' is inconclusive.')
            inconclusive += 1 
    except WebDriverException as E: 
        print(url)
        print(E)
        inconclusive += 1
#driver.quit()
f.close()
print('Uses: '+str(uses))
print('Does not Use: ' + str(notUses))
print('Inconclusive: ' + str(inconclusive))
driver.quit()