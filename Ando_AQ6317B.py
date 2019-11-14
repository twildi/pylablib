# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 11:28:01 2018

@author: vbh
"""
import prologix
import numpy as np
import time

class Ando_AQ6317B :
           
    def __init__(self, ip):
        self.ip = ip
        self.dev = None
        
        self.sensModes = ("NONE", "HIGH 1", "HIGH 2", "HIGH 3", "NORM RANGE HOLD", "NORM RANGE AUTO", "MID")
        self.chData = ("dummy", "LDATA ", "LDATB ", "LDATC ")
        self.chAxis = ("dummy", "WDATA ", "WDATB ", "WDATC ")
        self.gpibAddr = 1

    def connect(self, visaDLL = None):
        if self.dev == None:                     
            self.dev = prologix.gpibEthernetAdapter(self.ip, self.gpibAddr)   
            self.dev.setTimeout(30)
            self.dev.connect()
           
    def close(self):
        if self.dev != None:
            self.dev.write("GTL")
            self.dev.close()
            self.dev = None
         
    def getTrace(self, traces=[1]):
        "Returns the data from the given traces. Use for example getTrace([1,3]) to read traces 1 and 3."
        
        if self.dev == None:
            self.connect()
            wasConnected = 0
        else:
            wasConnected = 1
        time.sleep(0.02)
        
        if traces == 0:
            traces = range(1, len(self.chData))
    
        if np.max(traces) > len(self.chData):
            print("Instrument only supports "+str(len(self.chData))+" channels. Higher numbers are ignored.")
            traces = traces[traces <= len(self.chData)]
    
        if(isinstance(traces, int)):
            traces = (traces,)
    

    
        res = dict()
        for ch in traces:
            res[str(ch)] = dict()
            res[str(ch)]['y'] = np.fromstring(self.dev.query(self.chData[ch]), sep=',', dtype=float)[1:]
            res[str(ch)]['x'] = np.fromstring(self.dev.query(self.chAxis[ch]), sep=',', dtype=float)[1:]
            
        res['time'] = time.asctime(time.localtime())
        res['idn'] = self.dev.query("*IDN?")
        res['res'] = float(self.dev.query("RESLN?"))
        res['sensMode'] = self.sensModes[int(self.dev.query("SENS?"))]
        res['numAvr'] = int(self.dev.query("AVG?"))
        # res['nrPts'] = int(dev.query("SMPL?"))            # gives 0 for some reason
            
        if wasConnected != 1:
            self.close()
    
        return res    

   

