# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 12:09:58 2019

@author: vbh
"""

import matplotlib.pyplot as plt

# for saving data
from LabIO import *

from LabInstruments import esa2

# read out traces
myData = esa2.getTrace(2)

# read some more data, default trace is 1
referenceData = esa2.getTrace()

# one could also read the two traces at the same time using 
#allData = esa2.getTrace([1,2])

plt.plot(myData['2']['x'], myData['2']['y'])

# use some of the meta data in the data sets
plt.title('Awesome measurement with RBW of '+str(myData['rbw']/1e3)+' kHz.')

# save data as MyDataSet.npz, ".npz" is attached automatically if it is not given
labSave({'esaData' : myData, 'referenceData' : referenceData}, 'MyDataSet')

# or without a filename, then the time is used as a file name as in e.g. DataSaved_2019-10-17_12h3m24s.npz :
#labSave({'esaData' : myData, 'referenceData' : referenceData})

# now laod data again
myDataSet = labLoad('MyDataSet')

# and plot a referenced data set
plt.plot(myDataSet['esaData']['2']['x'], myDataSet['esaData']['2']['y'] - myDataSet['referenceData']['1']['y'])

# get individual data sets from the dictionary
esaData = myDataSet['esaData']
referenceData = myDataSet['referenceData']