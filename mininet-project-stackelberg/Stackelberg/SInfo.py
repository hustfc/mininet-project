from scapy.all import sniff, sendp
from scapy.all import Packet
from scapy.all import ShortField, IntField, LongField, BitField
from scapy.all import Ether, IP, ICMP

import time

import sys
import fire
import random

def send(src, iface, dst, times=15, send_pkt=[]):

    #filename='/home/shlled/mininet-wifi/Log/UE%s.json' % src[7:8]
    filename = '/media/psf/Home/Documents/GitHub/mininet-project/mininet-project-stackelberg/Stackelberg/Log/UE%s.json' % src[7:8]
    f=open(filename,'r')
    buffer=f.readlines()
    lenth=len(buffer)
    time.sleep(1)
    "send the latest info to BS "
    alpha=buffer[lenth-1]
    msg = alpha
    send_pkt.append(msg)
    p = Ether() / IP(src=src, dst=dst) / ICMP() / msg
    "wait random seconds, then send in case of collision"
    t = random.randint(1,10)
    t = float(t) / 10.0
    time.sleep(t)
    sendp(p, iface = iface)
    f.close()
fire.Fire(send)
