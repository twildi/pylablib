# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 11:28:01 2018

@author: vbh
"""
import telnetlib
import time

class Toptica_CTL1550:  
    controlPort = 1998
    timeOut = 10
    dev = None
    
    def __init__(self, ip):
        self.ipAddress = ip
    
    def connect(self):
        if self.dev == None:
            self.dev = telnetlib.Telnet(self.ipAddress, self.controlPort, self.timeOut)   
    
    def close(self):
        if self.dev != None:
            self.dev.close()
            self.dev = None
    
    def startScan(self):
        """ Start the scan """
        self.connect()
        self.dev.write("(exec 'laser1:ctl:scan:start)\n".encode("ascii"))
        time.sleep(0.2)
        self.close()
        return 0
    
    def initScan(self, startWl, stopWl, scanSpeed):
        """ Initializes the basic scan parameters
        
        Units are nm or nm/s """
        self.connect()
        
        self.dev.write( ("(param-set! 'laser1:ctl:wavelength-set "+str(startWl)+" )\n").encode("ascii"))
        
        self.dev.write( ("(param-set! 'laser1:ctl:scan:speed "+str(scanSpeed)+" )\n").encode("ascii"))
        self.dev.write( ("(param-set! 'laser1:ctl:scan:wavelength-begin "+str(startWl)+" )\n").encode("ascii"))
        self.dev.write( ("(param-set! 'laser1:ctl:scan:wavelength-end "+str(stopWl)+" )\n").encode("ascii"))
        time.sleep(0.2)
        self.dev.read_very_eager()
        self.dev.write( ("(param-ref 'laser1:ctl:state)\n").encode("ascii"))
        time.sleep(0.2)
        while int(chr(self.dev.read_eager()[-5])) == 1:
            time.sleep(0.2)
            self.dev.write( ("(param-ref 'laser1:ctl:state)\n").encode("ascii"))
            time.sleep(0.2)
        self.close()
        return 0        
    
    def setWavelength(self, wl):
        self.connect()
        self.dev.write( ("(param-set! 'laser1:ctl:wavelength-set "+str(wl)+" )\n").encode("ascii"))
        time.sleep(0.2)
        self.dev.read_very_eager()    
        self.dev.write( ("(param-ref 'laser1:ctl:state)\n").encode("ascii"))
        time.sleep(0.2)
        while int(chr(self.dev.read_eager()[-5])) == 1:
            time.sleep(0.2)
            self.dev.write( ("(param-ref 'laser1:ctl:state)\n").encode("ascii"))
            time.sleep(0.2)
        self.close()
        return 0
    
