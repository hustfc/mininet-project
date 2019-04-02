from scapy.all import sniff, sendp
from scapy.all import Packet
from scapy.all import ShortField, IntField, LongField, BitField
from scapy.all import Ether, IP, ICMP

import time

import sys
import fire

def send(src, iface, dst, times=15, send_pkt=[]):
    t = 0
    #filename='/home/shlled/mininet-wifi/Log/UE%s.txt' % src[7:9]
    filename = '/media/psf/Home/Documents/GitHub/mininet-project/Stackelberg/Log/UE%s.json' % src[7:9]
    f=open(filename,'r')
    buffer=f.readlines()
    lenth=len(buffer)
    time.sleep(1)
    "send the latest info to BS "
    alpha=buffer[lenth-1]
    msg = alpha
    send_pkt.append(msg)
    p = Ether() / IP(src=src, dst=dst) / ICMP() / msg
    sendp(p, iface = iface)
    t += 1
    f.close()
fire.Fire(send)
