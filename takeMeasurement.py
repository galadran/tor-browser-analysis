
#iterate through the list of URLS
#Record size / requests
#If something fails, count it as a failure, but attempt to load it a second time for the benefit of the cache. 
#Store all the performance results in the cache (JS, total sizes transferred.)
#Store results as row + blob of perf timings. 
#Visually inspect size over time to check for mismatches?

#Format: driver - sequence - url - blob of perf measurements - unique session id. 
from uuid import uuid4
import sqlite3
from tqdm import tqdm
from base64 import b64encode
from pickle import dumps 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException,JavascriptException,WebDriverException,StaleElementReferenceException
from selenium.webdriver.firefox.options import Options
from tbselenium.tbdriver import TorBrowserDriver

filename = "data.sqlite"
db = sqlite3.connect(filename)
sql = db.cursor() 

def timings(driver):
        perf_timings = driver.execute_script("return window.performance.getEntries()")
        paint_timings = driver.execute_script("return window.performance.timing")
        return (paint_timings,perf_timings)

def measurement(driver,url):
    driver.set_page_load_timeout(60)
    try:
        driver.get(url)
        t = timings(driver)
    except JavascriptException as E: 
        #Nothing we can do, return failure
        return None 
    except TimeoutException as E:
        #Attempt to grab current timings, refresh to load the page into cache. 
        #Return either partial results or failure. s
        try:
            t1,t2 = timings(driver)
            t1['failed'] = True
            try:
                driver.get(url)
            except: 
                return (t1,t2)
            return (t1,t2)
        except:
            return None 
    except Exception as E:
        print("Failed Measurement: " + str(E))
        return None

def makeMeasurement(driver,url):
    measurements = []
    m = measurement(driver,url)
    if m is None:
        m = 'FAILED'
    measurements.append(m)
    return measurements

def saveResult(id,p,url,d,m):
    insert = """INSERT INTO sessions VALUES (
                '""" + str(id) + """',
                '""" + str(p) + """',
                '""" + str(url) + """',
                '""" + str(d.db_name) + """',
                '""" + (dumps(m)).hex() + """' 
    )"""
    sql.execute(insert)
    db.commit()

def measureSession(driver,path):
    sessionID = uuid4()
    for i in tqdm(range(len(path))):
        url = path[i]
        measurements = makeMeasurement(driver,url)
        for m in measurements:
            saveResult(sessionID,i,url,driver,m)


with open('specimenSession.txt', 'r') as url_file:
    path = url_file.readlines()

def getFirefoxDriver():
    profile = webdriver.FirefoxProfile()
    profile.set_preference('privacy.trackingprotection.enabled',False)
    profile.set_preference('dom.performance.time_to_contentful_paint.enabled',True)
    profile.set_preference('dom.performance.time_to_non_blank_paint.enabled',True)
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options,firefox_profile=profile)
    driver.db_name = 'Firefox'
    return driver

tor_dir = '../tor-browser-patched/Primary/'
def getTorDriver(): 
    driver = TorBrowserDriver(tor_dir)
    driver.db_name = 'TorBrowser'
    return driver

def getTorFirefoxDriver():
    profile = webdriver.FirefoxProfile()
    profile.set_preference('privacy.trackingprotection.enabled',False)
    profile.set_preference('dom.performance.time_to_contentful_paint.enabled',True)
    profile.set_preference('dom.performance.time_to_non_blank_paint.enabled',True)
    profile.set_preference( "network.proxy.type", 1 )
    profile.set_preference( "network.proxy.socks_version", 5 )
    profile.set_preference( "network.proxy.socks", '127.0.0.1' )
    profile.set_preference( "network.proxy.socks_port", 9050 )
    profile.set_preference( "network.proxy.socks_remote_dns", True )
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options,firefox_profile=profile)
    driver.db_name = 'Firefox-Over-Tor'
    return driver

from time import sleep 
while True:
    d = getTorDriver()
    measureSession(d,path)
    d.quit()
    sleep(120)