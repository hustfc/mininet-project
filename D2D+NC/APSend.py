from scapy.all import sniff, sendp
from scapy.all import Ether, IP, ICMP, UDP
from mininet.log import info

import time

import fire
import random

from NC.FileToM import *

#python APSend.py 10.0.0.1 AP-wlan0 10.0.0.2 10.0.0.3
#python DU_receive.py 10.0.0.3 DU-wlan0
#python RU_receive_AP.py 10.0.0.2 RU-wlan0

file = '/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log'

filename1 = '%s/msg.txt' % file
results = FToMatrix(filename1)
matrix = results[0]


def send(src, iface, dst1, dst2, filename = '', flag = True, miss_pkt='',pow=5, times=10,send_pkt=[]):
    if flag:
        index = 0
        lenth = len(matrix)
        total = lenth
        while index < lenth:
            #time.sleep(0.3)
            now = time.time()
            data = str(matrix[index])
            print('index', index)
            print('data', data)
            msg = "send_time: " + "%.6f" % float(now) + "total:%d" % total + "index:%d" % index + "data:" + data
            p = Ether() / IP(src=src, dst=dst1) / ICMP() / msg
            sendp(p, iface=iface)
            p = Ether() / IP(src=src, dst=dst2) / ICMP() / msg
            sendp(p, iface = iface)
            index += 1
    else:
        #filename1='/home/shlled/mininet-wifi/Log/%s' % filename

        filename1 = '/media/psf/Home/Documents/GitHub/mininet-project/Stackelberg/Log/%s' % filename
        f1=open(filename1,'r')
        buffer=f1.readlines()
        lenth=len(buffer)
        total=lenth
        #miss_pkt = stringToList(miss_pkt)
        while miss_pkt!=[]:
            info("miss_pkt in send.py:", miss_pkt)
            print(miss_pkt)
            time.sleep(0.1)
            now = time.time()
            alpha=buffer[int(miss_pkt[0])]
            print('alpha', alpha)
            msg = "send_time: " + "%.6f" % float(now) + " filename:%s" % filename  + "total:%d" % total + "index:%d" % miss_pkt[0] + "data:" + alpha
            send_pkt.append(msg)
            print(msg)
            p = Ether() / IP(src=src, dst=dst) / ICMP() / msg
            "miss packet"
            top = int(100 - 100 * loss)
            key = random.randint(1, 100)
            if key in range(1, top):
                sendp(p, iface=iface)
            else:
                print("can't send the packet\n")
            miss_pkt.pop(0)
        f1.close()
fire.Fire(send)