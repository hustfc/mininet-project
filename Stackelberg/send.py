from scapy.all import sniff, sendp
from scapy.all import Packet
from scapy.all import ShortField, IntField, LongField, BitField
from scapy.all import Ether, IP, ICMP

import time

import sys
import fire
import json

''' 
    --num  the number of the packet
    --pow  the power of sending msg
    --times the max time of sending
'''
def send(src, iface, dst, num=0, pow=5,times=10,send_pkt=[]):
    t = 0
    index = 0+num*10
    filename1='/home/shlled/mininet-wifi/Log/msg.txt'
    f1=open(filename1,'r')
    buffer=f1.readlines()
    lenth=len(buffer)
    while index<lenth and t<times:
        time.sleep(1)
        now = time.time()
        alpha=buffer[index]
        msg = "send_time: " + "%.6f" % float(now) + " msg: " + alpha
        send_pkt.append(msg)
        print(msg)
        p = Ether() / IP(src=src, dst=dst) / ICMP() / msg
        sendp(p, iface = iface)
        t += 1
        index+=1
        # alpha = chr(ord(alpha) + 1)
    f1.close()
    filename2='/Users/fanc/Documents/GitHub/mininet-wifi-project/Stackelberg/Log/UE%s.json' % src[7:9]
    #update the pow after sending msg
    with open(filename2,'r+') as f2:
        buffer = f2.readlines()
        lenth = len(buffer)
        #data =buffer[0]
        data = json.loads(buffer[lenth-1])
        data["POWER"]-= pow 
        json.dump(data,f2)
        f2.write("\n")

fire.Fire(send)
