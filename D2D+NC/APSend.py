from scapy.all import sniff, sendp
from scapy.all import Ether, IP, ICMP, UDP
from mininet.log import info

import time

import fire
import random

from NC.FileToM import *

#file = '/Users/fanc/Documents/GitHub/mininet-project/D2D+NC/Log'
file = '/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log'

filename1 = '%s/msg.txt' % file
results = FToMatrix(filename1)
matrix = results[0]

def send(src, iface, dst, filename = '', flag = True, miss_pkt='',pow=5, times=10,send_pkt=[]):
    if flag:
        index = 0
        lenth = len(matrix)
        total = lenth
        while index < lenth:
            now = time.time()
            data = matrix[index]
            data_send = ''.join(data)
            print('index', index)
            print(data_send)
            msg = "send_time: " + "%.6f" % float(now) + "total:%d" % total + "index:%d" % index + "data:" + data_send
            p = Ether() / IP(src=src, dst=dst) / UDP() / msg
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
    # filename2='/home/shlled/mininet-wifi/Log/UE%s.json' % src[7:9]
    # #update the pow after sending msg
    # with open(filename2,'r+') as f2:
        # buffer = f2.readlines()
        # lenth = len(buffer)
        # #data =buffer[0]
        # data = json.loads(buffer[lenth-1])
        # data["POWER"]-= pow
        # json.dump(data,f2)
        # f2.write("\n")

fire.Fire(send)