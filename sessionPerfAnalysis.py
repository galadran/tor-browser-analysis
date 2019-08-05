
#Grab complete 
#Plot the total request size over time. (and whether it failed or not)
#Heatmap? 

import sqlite3
from tqdm import tqdm 
from pickle import loads

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.io as pio
from collections import Counter 

def unpackMeasurement(b):
    #block back into python object
    #dehex, depickle 
    b = bytes.fromhex(b)
    b = loads(b)
    return b

filename = "data.sqlite"
db = sqlite3.connect(filename)
sql = db.cursor() 

sql.execute("""
    SELECT id,position,driver,measurements FROM sessions
""")

sessions = dict()
for (id,p,driver,m) in tqdm(sql.fetchall()):
    if p not in sessions.keys():
        sessions[p] = dict()
    if driver not in sessions[p].keys():
        sessions[p][driver] = list()
    sessions[p][driver].append(unpackMeasurement(b))

def getLast(m):
    timing,entries = m
    latestName = "" 
    latestFinish = 0.0
    for e in m: 
        if e["entryType"] not in ["mark","measure"]:
            continue 
        finishTime = float(e["startTime"]) + float(e["duration"])
        if finishTime > latestFinish:
            latestFinish = finishTime
            latestName = e["name" ]
    return latestName  
    #Given a measurement set, find the last measurement
    #Extract both the marks and measures. find the latests. 
    #Find the last mark? (how do we know the origin?)
    #Return the name as a string 

for i in sessions.keys():
    #Grab the Firefox measurements. Arrange each by order. Check agreement on which one is last. Take majority vote. 
    measurements = list(sessions[i]['Firefox'][1])
    last = map(getLast,m)
    counts = Counter(last)
    most,second = counts.most_common(2)
    if second*2 > most:
        print("Warning, no dominant element for: " +str(i))
    sessions[i]['lastMark'] = most 
    #Annotate this value 

def getMeasurements(m,lastMark):
    #Unpack the measurements
    timing,entries = m
    #calculate time to first byte
    TTFB = timing['responseStart'] - timing['requestStart'] #What about if we hit cache? Do we care? 
    #calculate tine to first content paint 
    TTFCP = timing['timeToContentfulPaint   ']
    #calculate time to last mark/measure

#Calculate the summary statistics. 
for d in sessions[0].keys():
    #produce a list of each measurement for every page load. 

#Print 1st/50th/99th percentile
#Draw histograms