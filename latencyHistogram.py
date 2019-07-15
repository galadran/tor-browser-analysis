


#%%

from tqdm import tqdm
import csv 
import datetime
from statistics import median,mean,stdev
import numpy as np 
import sqlite3
import time
import numpy as np
import matplotlib.pyplot as plt

def drawHistogram(source,results,filename):
    #binBoundaries = np.linspace(0,10,1000)
    fig, ax = plt.subplots(3,1,figsize=(36,24))

    ax[0].set_xlim(0,60)
    n, bins, patches = ax[0].hist(results, bins='auto', range=(0,60),cumulative=False,density=False)
    #ax[0].set_ylim(0,max(n)*1.1)
    
    ax[1].set_xlim(0,10)
    n, bins, patches = ax[1].hist(results, bins='auto', range=(0,10),cumulative=False,density=False)
    #ax[1].set_ylim(0,max(n)*1.1)

    ax[2].set_xlim(10,60)
    n, bins, patches = ax[2].hist(results, bins='auto', range=(10,60),cumulative=False,density=False)
    #ax[2].set_ylim(0,max(n)*1.1)
    
    ax[2].set_xlabel("Latency (seconds)")
    ax[2].set_ylabel("Number of Measurements")
    ax[0].set_title("All Requests " + source)
    ax[1].set_title("Fast Requests " + source)
    ax[2].set_title("Slow Requests " + source)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

dbpath = 'data.sqlite'

db = sqlite3.connect(dbpath)
sql = db.cursor()
sql.execute("""SELECT requestStart,responseEnd FROM requests """)

results = list()

for (st,ft) in tqdm(sql.fetchall()):
        latency = (float(ft)-float(st)) / 1000.0
        results.append(latency)

drawHistogram('fetch-nonblank',results,'fetch-nonblank.png')
