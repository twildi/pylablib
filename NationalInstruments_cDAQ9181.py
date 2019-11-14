# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 09:22:52 2018

@author: vbh
"""
import PyDAQmx
import time
import ctypes
import numpy as np

class NationalInstruments_cDAQ9181 :
   
    def __init__(self, devName='cDAQ9181-187B837'):
        self.devName = devName 
        self.task = None
        self.connected = False
        self.numberPoints = 0
        self.samplingRate = 0
        self.channels = 0
        self.started = False
    
    def connect(self):
        # reserved the network device which can take a while
        if PyDAQmx.DAQmxReserveNetworkDevice(self.devName, True) == 0:
            self.connected = 1
        
    def setup(self, channelsP, numberPointsP, samplingRateP):
        self.numberPoints = numberPointsP
        self.samplingRate = samplingRateP
        
        if(isinstance(channelsP, int)):
            self.channels = (channelsP,)    
        else:
            self.channels = channelsP   
        
        self.connect()
    
        self.task = PyDAQmx.Task()
                       
        # DAQmx Configure Code
        for ch in self.channels:
            if ch <0 or ch > 3:
                print("Error: invalid channel number. Only 0 to 3 valid.")
                self.channels.remove(ch)
            else: 
                #print(self.devName+"Mod1/ai"+str(ch))
                self.task.CreateAIVoltageChan(self.devName+"Mod1/ai"+str(ch),"",PyDAQmx.DAQmx_Val_Cfg_Default,-10.0,10.0,PyDAQmx.DAQmx_Val_Volts,None)
        
        if len(self.channels) == 0:
            print("No valid channels.")
            return 0
            
        self.task.CfgSampClkTiming("",self.samplingRate, PyDAQmx.DAQmx_Val_Rising, PyDAQmx.DAQmx_Val_FiniteSamps, self.numberPoints)
        self.connected = True
    
    def start(self):
        if self.task != None and self.started == False :
            self.task.StartTask()
            self.started = True
                    
    
    def read(self, channelsP=0, numberPointsP=0, samplingRateP=0):
        
        if self.connected == 0 :
            self.connect()    
        
        if self.task == None :
            if numberPointsP != 0:
                self.setup(channelsP, numberPointsP, samplingRateP)
            else:
                print("Parameters required!")
                return -1              
        
        # DAQmx Start Code
        if self.started == False:
            self.task.StartTask()
            self.started = True
        
        # DAQmx Read Code
        timeout = self.numberPoints/self.samplingRate+5 
        pointsRead = PyDAQmx.int32()
        data = np.zeros((len(self.channels)*self.numberPoints,), dtype=np.float64)    
        self.task.ReadAnalogF64(self.numberPoints,timeout, PyDAQmx.DAQmx_Val_GroupByChannel,data,len(data), ctypes.byref(pointsRead),None)
        
        self.task.StopTask()
        self.started = False
        
        if pointsRead.value != self.numberPoints:
            print("Not all points read sucessfully.")
        
        res = dict()
        res['samplingRate'] = self.samplingRate
        res['numberPoints'] = self.numberPoints
        res['readCh'] = self.channels
        res['time'] = time.asctime(time.localtime())
        res['data'] = dict()
        res['idn'] = "cDAQ9181-187B837Mod1, 01770E97"
        res['unit'] = 'V'
        for i, ch in enumerate(self.channels):
            res['data'][str(ch)] = data[i*self.numberPoints:(i+1)*self.numberPoints]
        
        return res
