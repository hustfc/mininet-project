from scapy.all import sniff, sendp
from scapy.all import Ether, IP, ICMP, UDP
from mininet.log import info

import time

import fire
import random

from NC.FileToM import *

#python APSend.py 10.0.0.1 AP-wlan0 10.0.0.2 10.0.0.3 0 False(True)
#python DU_receive.py 10.0.0.3 DU-wlan0
#python RU_receive_AP.py 10.0.0.2 RU-wlan0

file = '/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log'

filename1 = '%s/msg.txt' % file
results = FToMatrix(filename1)
#matrix = results[0]
filename2 = '%s/APSend.txt' % file
f2 = open(filename2, 'a+')

def send(src, iface, dst1, dst2, num, resend = False, miss_pkt='',pow=5, times=10,send_pkt=[]):
    matrix = results[num]
    if resend == False:
        index = 0
        lenth = len(matrix)
        total = lenth
        while index < lenth:
            #time.sleep(0.3)
            now = time.time()
            data = str(matrix[index])
            print('index', index)
            print('data', data)
            f2.write(data)
            f2.write('\n')
            msg = "send_time: " + "%.6f" % float(now) + "total:%d" % total + "index:%d" % index + "data:" + data
            p = Ether() / IP(src=src, dst=dst1) / ICMP() / msg
            sendp(p, iface=iface)
            p = Ether() / IP(src=src, dst=dst2) / ICMP() / msg
            sendp(p, iface = iface)
            index += 1
        f2.write('\n')
        f2.close()
    else:
        index = 0
        lenth = len(matrix)
        total = lenth
        while index < lenth:
            # time.sleep(0.3)
            now = time.time()
            data = str(matrix[index])
            print('index', index)
            print('data', data)
            msg = "send_time: " + "%.6f" % float(now) + "total:%d" % total + "index:%d" % index + "data:" + data
            p = Ether() / IP(src=src, dst=dst1) / ICMP() / msg
            sendp(p, iface=iface)
            index += 1
fire.Fire(send)