
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


filename = "data.sqlite"
db = sqlite3.connect(filename)
sql = db.cursor() 

sql.execute("""
    SELECT id,position,measurements FROM sessions
""")

sessions = dict()
for (id,p,m) in tqdm(sql.fetchall()):
    if id not in sessions.keys():
        sessions[id] = list()
    sessions[id].append((p,m))

def unpackMeasurement(b):
    #block back into python object
    #dehex, depickle 
    b = bytes.fromhex(b)
    b = loads(b)
    return b

def getSize(m):
    #measurement object into size
    if m == 'FAILED':
        return -1 
    total = 0
    for ms in m:
        if 'transferSize' in ms.keys():
            total += ms['transferSize']
        if 'paint' in str(ms.keys()):
            print(ms)
    return total 


traces = list()
for s in sessions.values():
    measurements = (map(lambda x: x[1],sorted(s,key=lambda x: x[0])))
    yValues = list(map(getSize,map(unpackMeasurement,measurements)))
    trace = go.Scatter(
        #name=source,
        x=list(range(len(yValues))),
        y=yValues,
        mode='lines')
    traces.append(trace)

plot(traces)