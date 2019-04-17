# -*- coding: utf-8 -*-
from scapy.all import sniff, sendp
from scapy.all import Ether, IP, ICMP, UDP
from mininet.log import info

import time

import fire
import random

filename1 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/DU_coe.txt"
filename2 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/DU_encoded.txt"
filename3 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/DU_count.txt"
filename4 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/DU_pkts.txt"

size = 32
pkts = {}
datas = {}   #data receive from AP
for i in range(size):
    pkts[i] = False
    datas[i] = ''

def send(src, iface, dst1, filename = '', flag = True, miss_pkt='',pow=5, times=10,send_pkt=[]):
    index = 0
    with open(filename3, 'r') as f3:
        buffer3 = f3.readlines()
        lenth = int(buffer3[-1])
        print('length', lenth)
    with open(filename4, 'r') as f4:
        buffer4 = f4.readlines()
    pkt_start = len(buffer4) - (lenth + 1)
    for i in range(lenth):
        index = int(buffer4[pkt_start + i])
        pkts[index] = True
    f1 = open(filename1, 'r')
    f2 = open(filename2, 'r')
    buffer1 = f1.readlines()
    buffer2 = f2.readlines()
    coe_start = len(buffer1) - (lenth + 1)
    encode_start = len(buffer2) - (lenth + 1)
    # print('pkts', pkts)
    # print('coe', buffer1[coe_start])
    i = 0  #由于系数矩阵的文件是没有空的
    for index in range(size):
        if pkts[index] == True:
            time.sleep(0.3)
            now = time.time()
            coe = buffer1[coe_start + i][:-1]   #take out '\n'
            enc = buffer2[encode_start + i][:-1]
            #data_send = ''.join(data)
            # print('index', index)
            # print('coe', coe)
            # print('enc', enc)
            msg = "send_time: " + "%.6f" % float(now) + "total:%d" % size + "index:%d" % index + "coe:" + coe + "enc:" + enc
            print(msg)
            p = Ether() / IP(src=src, dst=dst1) / UDP() / msg
            sendp(p, iface=iface)
            i += 1
    f1.close()
    f2.close()
fire.Fire(send)

#Unit Test
#python DU_send.py 10.0.0.3 DU-wlan0 10.0.0.10