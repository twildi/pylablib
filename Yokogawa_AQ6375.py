"""
Reads Keysight PXA N9030A Signal Analyzer
"""

# commands taken from https://literature.cdn.keysight.com/litweb/pdf/N5180-90004.pdf?id=855498

import visa
import numpy as np
import time

class Yokogawa_AQ6375 :
    
    traceNames = ['TRA', 'TRB', 'TRC', 'TRD', 'TRE', 'TRF', 'TRG']
        
    def __init__(self, visaP):
        self.visaAddress = visaP 
        self.rm = None
        self.dev = None

    def connect(self, visaDLL = None):
        if self.dev == None:         
            self.rm = visa.ResourceManager()
            self.dev = self.rm.open_resource(self.visaAddress)
            self.dev.timeout = 20000
            self.dev.read_termination = '\r\n'
            self.dev.write_termination = '\r\n'
            self.dev.write('OPEN "anonymous"')
            self.dev.read()
            self.dev.write('*CLS')
            self.dev.read()
            
            #self.dev.flush(visa.constants.VI_READ_BUF_DISCARD)
           
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
            
            self.dev.write(':TRAC:y? '+self.traceNames[trace-1])
            a = self.dev.read()
            res[str(trace)]['y'] = np.fromstring(a, sep=',')
            
            self.dev.write(':TRAC:x? '+self.traceNames[trace-1])
            a = self.dev.read()
            res[str(trace)]['x'] = np.fromstring(a, sep=',')
        
        self.dev.clear()
        res['rbw'] =  float(self.dev.query(':SENS:BAND?'))
        res['idn'] = self.dev.query("*IDN?").strip()
        res['time'] = time.asctime(time.localtime())
        
        
        if wasConnected != 1:
            self.close()
        
        return res
       
    




    
    



    
    
    
    




