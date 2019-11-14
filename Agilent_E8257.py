"""
Reads Keysight PXA N9030A Signal Analyzer
"""

# commands taken from https://literature.cdn.keysight.com/litweb/pdf/N5180-90004.pdf?id=855498

import visa
import numpy as np
import time

class Agilent_E8257 :

    def __init__(self, visaP):
        self.visaAddress = visaP 
        self.rm = None
        self.dev = None
    
    def connect(self, visaDLL = None):
        "Initializes the connection to the device"
        if self.rm == None:
            if visaDLL == None:
                self.rm = visa.ResourceManager()
            else:
                self.rm = visa.resourceManager(visaDLL) 
                
        if self.dev == None:         
            self.dev = self.rm.open_resource(self.visaAddress)
            self.dev.timeout = 1000
           
    def close(self):
        if self.dev != None:
            self.dev.close()
            self.dev = None
        # the resource manager self.rm is on purpose not closed because this can interfere with other instruments
         
    def setFreq(self, freq = 0):
        "Sets the generator frequency in Hz"
        
        # connect do device
        if self.dev == None:
            self.connect()
            wasConnected = 0
        else:
            wasConnected = 1
        time.sleep(0.02)
       
        # do useful stuff here
        self.dev.timeout = 10000
        self.dev.write('*CLS')
        self.dev.write('FREQ:CW ' + str(freq))        
        
        # potentially disconnect device again
        if wasConnected != 1:
            self.close()
        
        # return result, if anz
        return 1
    



    
    
    
    




