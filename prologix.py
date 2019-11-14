# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 18:39:30 2018

@author: vbh
"""
import telnetlib
import time

class gpibEthernetAdapter:
    gpibAddr = 1
    ipAddr = "192.168.0.23"
    port = 1234
    timeOut = 10
    waitTime = 0.1
    dev = 0
    
    def __init__(self, ip, gpib):
        self.gpibAddr = gpib
        self.ipAddr = ip
        
    def setTimeout(self, timeO):
        self.timeOut = timeO

    def connect(self):
        self.dev = telnetlib.Telnet(self.ipAddr, self.port, self.timeOut) 
        self.dev.write(("++addr "+str(self.gpibAddr)+"\n").encode('ascii'))

    def close(self):
        self.dev.close()
            
    def write(self, toWrite):
        if self.dev == 0:
            self.connect()
        
        self.dev.write((toWrite+"\n").encode("ascii"))
    
    def read(self):
        if self.dev == 0:
            self.connect()        
        return str(self.dev.read_until('\n'.encode('ascii'), self.timeOut).strip())[2:-1]
    
    def query(self, toWrite, readWaitTime=0):
        self.write(toWrite)
        if readWaitTime == 0:
            time.sleep(self.waitTime)
        else:
            time.sleep(readWaitTime)
        try:
            res = self.read()
        except:
            print("Error on read from instrument.")
            res = 0
        return res
        