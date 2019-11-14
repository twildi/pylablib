# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 18:44:16 2019

@author: vbh
"""

try:
    from Agilent_E8257 import Agilent_E8257
    gen1 = Agilent_E8257("TCPIP0::10.1.28.37::inst0::INSTR")
    gen2 = Agilent_E8257("TCPIP0::10.1.28.56::inst0::INSTR")
except:
    print('Problems import ESA 1 - 3')

from Agilent_N90X0A import Agilent_N90X0A
esa1 = Agilent_N90X0A("TCPIP0::10.1.28.57::inst0::INSTR")
esa2 = Agilent_N90X0A("TCPIP0::10.1.28.51::inst0::INSTR")
esa3 = Agilent_N90X0A("TCPIP0::10.1.28.62::inst0::INSTR")

from Ando_AQ6317B import Ando_AQ6317B
osa3 = Ando_AQ6317B("10.1.28.59")

from Yokogawa_AQ6375 import Yokogawa_AQ6375
osa1 = Yokogawa_AQ6375("TCPIP0::10.1.28.67::10001::SOCKET")

try:
    from NationalInstruments_cDAQ9181 import NationalInstruments_cDAQ9181
    daq1 = NationalInstruments_cDAQ9181('cDAQ9181-187B837')
except:
    print('Problem importing daq1. Probably PyDAQmx package not installed')

from Toptica_CTL1550 import Toptica_CTL1550
las1 = Toptica_CTL1550('10.1.28.52')

from RohdeSchwarz_FPC1500 import RohdeSchwarz_FPC1500
esa4 = RohdeSchwarz_FPC1500("TCPIP0::10.1.28.60::inst0::INSTR")
esa5 = RohdeSchwarz_FPC1500("TCPIP0::10.1.28.71::inst0::INSTR")