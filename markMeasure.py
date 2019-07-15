import time
import csv
import random
import json
import os
from datetime import datetime

from tbselenium.tbdriver import TorBrowserDriver
from xvfbwrapper import Xvfb

tor_dir = '../tor-browser-patched/Primary/'

vdisplay = Xvfb()
vdisplay.start()

# open list of urls for testing
with open('alexa-top-1000.txt', 'r') as url_file:
    test_urls = url_file.readlines()

driver = TorBrowserDriver(tor_dir)#, pref_dict=rfp)
driver.set_page_load_timeout(15)

# do 10 runs
uses = 0
notUses = 0
inconclusive = 0
for i, url in enumerate(test_urls):          
    try:
        # request url from list
        #print("Fetching " + str(url),end='')
        url = 'https://' + url 
        driver.get(url) 
        # pull window.performance.timing after loading the page and add information about url and number of run
        perf_timings = driver.execute_script("return window.performance.getEntries()")
        #print(perf_timings)
        entryTypes = set(map(lambda x : x['entryType'],perf_timings))
        if 'mark' in entryTypes or 'measure' in entryTypes:
            print(url + ' uses mark/measure')
            uses += 1
        else:
            print(url + ' does not use mark/measure')
            notUses += 1
        #Put in Database(url)
    except Exception as E: # what to do in case that an exception is thrown (which happens usually upon page load timeout)
        # also pull data and store it to the results file
        print("Failed to load page " + str(url) + ' Error: '+ str(E))
        perf_timings = driver.execute_script("return window.performance.getEntries()")
        entryTypes = set(map(lambda x : x['entryType'],perf_timings))
        if 'mark' in entryTypes or 'measure' in entryTypes:
            print(url + ' uses mark/measure')
            uses += 1
        else:
            print(url + ' is inconclusive.')
            inconclusive += 1 
#driver.quit()
print('Uses: '+str(uses))
print('Does not Use: ' + str(notUses))
print('Inconclusive: ' + str(inconclusive))
vdisplay.stop()