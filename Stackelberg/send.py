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
def send(src, iface, dst, distance, filename,flag = True,miss_pkt='',pow=5, times=10,send_pkt=[]):
    info(distance)
    if distance <= 5:
        loss = 0
    else:
        loss = 0.3
    if flag:
        index = 0
        #filename1 = '/home/shlled/mininet-project-fc/Stackelberg/Log/%s' % filename
        filename1 = '/media/psf/Home/Documents/GitHub/mininet-project/Stackelberg/Log/%s' % filename
        f1=open(filename1,'r')
        buffer=f1.readlines()
        lenth=len(buffer)
        total=lenth
        while index<lenth:
            time.sleep(0.5)
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
            else:
                print("can't send the packet\n")

            index+=1
        f1.close()
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
                miss_pkt.pop(0)
            else:
                print("can't send the packet\n")
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