# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 16:06:18 2018

Reads out Thorlabs PM100 powermeters.
At the very bottom some instances (PME100A, PME100B, ...) are already definied.
Access to only the read power at 1550nm e.g. via PME100A.read(1550)['val']

@author: vbh
"""

import visa
import numpy as np
import matplotlib.pyplot as plt
import time

class RohdeSchwarz_FPC1500 :

    traceNames = ['TRACE1', 'TRACE2', 'TRACE3', 'TRACE4', 'TRACE5', 'TRACE6']

    def __init__(self, visaP):
        self.visaAddress = visaP 
        self.rm = None
        self.dev = None
    
    def connect(self, visaDLL = None):
        if self.dev == None:         
            self.rm = visa.ResourceManager()
            self.dev = self.rm.open_resource(self.visaAddress)
            self.dev.timeout = 20000
           
    def close(self):
        if self.dev != None:
            self.dev.close()
            self.dev = None
        # the resource manager self.rm is on purpose not closed because this can interfere with other instruments
         
    def getTrace(self, traces=[1]):
        "Returns a dictonary with the measured power and some metadata"
        
        if not (type(traces) == list):
            if len(traces) == 1:
                traces = [traces]
            else:
                print('List of traces required as argument.')
        
        if self.dev == None:
            self.connect()
            wasConnected = 0
        else:
            wasConnected = 1
        time.sleep(0.02)
        
        res = dict()
        
        for trace in traces:
            res[str(trace)] = dict()
            res[str(trace)]['y'] = np.fromstring(self.dev.query('TRAC? '+self.traceNames[trace-1]), sep=',')
            fStart = float(self.dev.query('FREQ:start?'))
            fStop = float(self.dev.query('freq:stop?'))
            res[str(trace)]['x'] = np.linspace(fStart, fStop, len(res[str(trace)]['y']))
            res[str(trace)]['mode'] = self.dev.query('disp:trac'+str(trace)+':mode?').strip()
        
        time.sleep(0.02)        
        res['idn'] = self.dev.query("*IDN?").strip()
        res['time'] = time.asctime(time.localtime())
        
        
        if wasConnected != 1:
            self.close()
        
        return res





