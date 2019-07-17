import time
import csv
import random
import json
import os
from datetime import datetime

from tbselenium.tbdriver import TorBrowserDriver
from xvfbwrapper import Xvfb
import sqlite3 


# define unique results file for this run
filename = "data.sqlite"
db = sqlite3.connect(filename)
sql = db.cursor() 

colList = ['timestamp','path','cached', 'connectEnd', 'connectStart', 'domComplete', 
    'domContentLoadedEventEnd', 'domContentLoadedEventStart', 'domInteractive', 
    'domLoading', 'domainLookupEnd', 'domainLookupStart', 'fetchStart', 
    'loadEventEnd', 'loadEventStart', 'navigationStart', 'redirectEnd', 
    'redirectStart', 'requestStart', 'responseEnd', 'responseStart', 
    'secureConnectionStart', 'timeToNonBlankPaint', 'unloadEventEnd', 
    'unloadEventStart', 'url', 'error']

columns = str(sorted(colList)).replace('[','').replace(']','')

sql.execute("""
    CREATE TABLE IF NOT EXISTS requests (""" + columns + """)
""")

def insertDict(sql,d):
    query = "INSERT INTO requests VALUES ("
    for k in sorted(d.keys()):
        if query == "INSERT INTO requests VALUES (":
            query += "'"+str(d[k])+"'"
        else:
            query = query + ", '"+str(d[k])+"'"
    query = query + ')'
    sql.execute(query)
# Select path to Firefox binary
# this is the default path on macOS
tor_dir = '../tor-browser-patched/Primary/'

#vdisplay = Xvfb()
#vdisplay.start()

# open list of urls for testing
with open('markMeasureResults.txt', 'r') as url_file:
    test_urls = url_file.readlines()

driver = TorBrowserDriver(tor_dir)#, pref_dict=rfp)
driver.set_page_load_timeout(60)
cached = set() 
# do 10 runs
while True:
    random.shuffle(test_urls)
    for i, url in enumerate(test_urls):          
        try:
            # request url from list
            print("Fetching " + str(url),end='')
            driver.get(url) 
            
            # pull window.performance.timing after loading the page and add information about url and number of run
            perf_timings = driver.execute_script("return window.performance.timing")
            perf_timings['timestamp'] = datetime.now()
            perf_timings['path'] = tor_dir
            perf_timings['cached'] = str(url in cached) 
            perf_timings['url'] = str(url)
            perf_timings['error'] = 'NONE'

            #print(str(set(perf_timings.keys())-set(colList)))
            #TODO Put in Database
            insertDict(sql,perf_timings)
            cached.add(url)
        except Exception as E: # what to do in case that an exception is thrown (which happens usually upon page load timeout)
            # also pull data and store it to the results file
            perf_timings = driver.execute_script("return window.performance.timing")
            perf_timings['timestamp'] = datetime.now()
            perf_timings['path'] = tor_dir
            perf_timings['cached'] = str(url in cached) 
            perf_timings['url'] = str(url)
            perf_timings['error'] = str(E)
            #print(str(set(perf_timings.keys())-set(colList)))
            insertDict(sql,perf_timings)
            #Put in Database
        db.commit()
    #driver.quit()
#vdisplay.stop()