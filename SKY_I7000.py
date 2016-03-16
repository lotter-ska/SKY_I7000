# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 07:44:03 2015

@author: lkock
How to:
    From Skymon export results as CSV
    Copy onto local PC
    Run this script
    Open CSV file
"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from Tkinter import Tk
from tkFileDialog import askopenfilename
import time


from matplotlib.dates import date2num, num2date,\
        datestr2num, strpdate2num, drange,\
        epoch2num, num2epoch, mx2num,\
        DateFormatter, IndexDateFormatter, DateLocator,\
        RRuleLocator, YearLocator, MonthLocator, WeekdayLocator,\
        DayLocator, HourLocator, MinuteLocator, SecondLocator,\
        rrule, MO, TU, WE, TH, FR, SA, SU, YEARLY, MONTHLY,\
        WEEKLY, DAILY, HOURLY, MINUTELY, SECONDLY, relativedelta

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

data= np.genfromtxt(filename,delimiter=',',dtype=None)
data=data[1:-1]
s=np.size(data[:,1])

#Define data variables
freq=(data[1:s,2]).astype(np.float)
dbm=(data[1:s,3]).astype(np.float)
time_data=datestr2num(data[1:s,0])

tot_time_data=num2date(time_data[-1])-num2date(time_data[0])
tot_time_data=tot_time_data.seconds
tot_time_data=float(tot_time_data)
time_data_d=tot_time_data/600
ch=(data[1:s,1]).astype(np.float)
quan_measure=((num2date(time_data[-1])-num2date(time_data[0])).seconds/60.0) / (max(np.diff(num2date(time_data))).seconds/60.0)

# scatter plot of detections: power vs freq
#fig = plt.figure()
fig = plt.figure(figsize=(18.8,9.8))
ab=fig.add_subplot(221)
ab.scatter(freq,dbm,s=3,c=dbm, lw = 0)
#plt.xlim(min(freq)-1000,max(freq)+1000)
ab.grid()
plt.xlabel('Frequency [Hz]')
plt.title('18dB above noise floor detections: levels vs frequency')
plt.ylabel('dBm')
ab.hold

#plot occupancy
aa = fig.add_subplot(223)
a=np.histogram(freq,(np.unique(freq)))
#a=np.histogram(freq,np.unique(freq))
oc=100*a[0]/quan_measure
ff=a[1]
ff=ff[0:-1]
aa.stem(ff,oc)
plt.ylim(0,100)
#plt.xlim(min(freq),max(freq))
plt.xlabel('Frequency [Hz]')
plt.title('Freq Occupancy')
plt.ylabel('%')
plt.grid()



w = fig.add_subplot(122)
w.scatter(freq,time_data,s=7,c=dbm, lw = 0)
plt.grid()
tick_i=np.arange(min(time_data),max(time_data)+(max(time_data)-min(time_data))/32,(max(time_data)-min(time_data))/16)
tick_label=np.arange(1,len(time_data)+1,len(time_data)/16)
tlabel=data[tick_label,0]
lab=tlabel[0][0:16]

for x in tlabel[1::]:
    lab=np.append(lab,x[0:16])
        
plt.yticks(tick_i,lab,size='small')
plt.autoscale(enable=True, axis='both', tight=True)
plt.title('Detection Plot')
flnm=time.strftime("%Y%m%d")+"SKY_I7000_plot"
plt.savefig(flnm,dpi=100)