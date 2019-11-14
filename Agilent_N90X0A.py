"""
Reads Keysight PXA N9030A Signal Analyzer
"""

# commands taken from https://literature.cdn.keysight.com/litweb/pdf/N5180-90004.pdf?id=855498

import visa
import numpy as np
import time

class Agilent_N90X0A :
    
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
        "Returns the data from the given traces."
        
        if not (type(traces) == list):
            if type(traces) == int or len(traces) == 1:
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
            res[str(trace)]['y'] = np.fromstring(self.dev.query('TRAC:DATA? '+self.traceNames[trace-1]), sep=',')
            x_start = float(self.dev.query(':SENSe:FREQ:STAR?'))
            x_stop = float(self.dev.query(':SENSe:FREQ:STOP?'))

            res[str(trace)]['x'] = np.linspace(x_start, x_stop, np.size(res[str(trace)]['y']))
        
        time.sleep(0.02)    
        res['rbw'] =  float(self.dev.query(':SENSe:BAND:RES?'))
        res['idn'] = self.dev.query("*IDN?").strip()
        res['time'] = time.asctime(time.localtime())
        
        
        if wasConnected != 1:
            self.close()
        
        return res
       
    




    
    



    
    
    
    




