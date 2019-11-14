# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:30:50 2019

@author: vbh
"""

import numpy as np
import time

def labSave(dataDict, filename=''):
    if filename == '':
        saveTime = time.localtime()
        filename = 'DataSaved_'+str(saveTime[0])+'-'+str(saveTime[1])+'-'+str(saveTime[2])+'_'+str(saveTime[3])+'h'+str(saveTime[4])+'m'+str(saveTime[5])+'s.npz'
    if filename[-4:] != '.npz':
        filename = filename+'.npz'
    np.savez(filename, dataDict)
    
def labLoad(filename):
    if filename[-4:] != '.npz':
        filename = filename+'.npz'
    dataFile = np.load(filename)
    # not sure why you have to make it as complicated as this, but this is how it works:
    dataSet = dataFile.f.arr_0[()]
    return dataSet