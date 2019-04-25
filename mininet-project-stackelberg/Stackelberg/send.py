# -*- coding: utf8 -*-

from scapy.all import sniff, sendp
from scapy.all import Packet
from scapy.all import ShortField, IntField, LongField, BitField
from scapy.all import Ether, IP, ICMP
from mininet.log import info

import time

import sys
import fire
import json
import random
def stringToList(s):
    if s == '':
        return []
    s = s[1:len(s)-1]
    s = s.replace(' ', '')
    print(s)
    return [int(i) for i in s.split(',')]
''' 
    --num  the number of the packet
    --pow  the power of sending msg
    --times the max time of sending
    --flag  if flag = false ,that means sending the missing packet using miss_pkt params
'''
def send(src, iface, dst, distance, pow, gain, filename, flag = True, miss_pkt='',times=10,send_pkt=[]):
    info(distance)
    count = 0.0 # 记录实际发送了多少个包
    total = 0
    if distance <= 4:
        loss = 0
    else:
        loss = 0.1
    if flag:
        index = 0
        #filename1='/home/shlled/mininet-wifi/Log/%s' % filename
        filename1 = '/media/psf/Home/Documents/GitHub/mininet-project/mininet-project-stackelberg/Stackelberg/Log/%s' % filename
        f1=open(filename1,'r')
        buffer=f1.readlines()
        lenth=len(buffer)
        total=lenth
        while index<lenth:
            time.sleep(0.1)
            now = time.time()
            alpha=buffer[index]
            #alpha=buffer[index].strip()
            msg = "send_time: " + "%.6f" % float(now) + " filename:%s" % filename  + "total:%d" % total + "index:%d" % index + "data:" + alpha
            send_pkt.append(msg)
            print(msg)
            p = Ether() / IP(src=src, dst=dst) / ICMP() / msg

            "miss packet"
            top=int(100-100*loss)
            key=random.randint(1,100)
            if key in range(1,top):
                sendp(p, iface = iface)
                count += 1
            else:
                print("can't send the packet\n")

            index+=1
        f1.close()
    else:
        #filename1='/home/shlled/mininet-wifi/Log/%s' % filename
        filename1 = '/media/psf/Home/Documents/GitHub/mininet-project/mininet-project-stackelberg/Stackelberg/Log/%s' % filename
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
                miss_pkt.pop(0)
            else:
                miss_pkt.pop(0)
                print("can't send the packet\n")
        f1.close()
    filename2='/media/psf/Home/Documents/GitHub/mininet-project/mininet-project-stackelberg/Stackelberg/Log/UE%s.json' % src[7:8]
    
    #第一次发送包时才更新能量和收益，重传时不考虑
    if flag:
        with open(filename2,'r+') as f2:
            buffer = f2.readlines()
            lenth = len(buffer)            
            data = json.loads(buffer[lenth-1])
            data["POWER"] -= pow
            data["Gains"] += gain 
            integ =  count / total
            data["Integrity"] = integ
            json.dump(data,f2)
            f2.write("\n")
fire.Fire(send)
