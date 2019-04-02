from scapy.all import sniff, sendp
from scapy.all import Packet
from scapy.all import ShortField, IntField, LongField, BitField

import sys
import struct
import time
from collections import Counter
import fire
import random
import re

packet_counts = Counter() 
packet_queue = []


class action:
    def __init__(self, IP, rc_pkt):
        self.ip = IP
        self.rc_pkt = rc_pkt
    def custom_action(self, packet):

        key = tuple([packet[0][1].src, packet[0][1].dst])

        if packet[0][1].dst == self.ip:   # receive.py  second param is its own ip 
            # filename=[]
            # filename.append(packet[0][1].dst)
            # filename.append(".txt")
            filename1='/Users/fanc/Documents/GitHub/mininet-wifi-project/Stackelberg/Log/%s.txt' % packet[0][1].dst[7:9]
            f1=open(filename1,"a+")
            filename2='/Users/fanc/Documents/GitHub/mininet-wifi-project/Stackelberg/Log/final.txt'
            f2=open(filename2,'a+')
            packet_queue.append(packet[0][3].load)
            self.rc_pkt.append(packet[0][3].load)
            packet_counts.update([key])
            now = time.time()
            info="receive_time: " + "%.6f" % float(now) + " " + packet[0][3].load
            f1.write('Receive Packet #%d: %s ==> %s : %s\n' % (sum(packet_counts.values()), packet[0][1].src, packet[0][1].dst,info))
            
            "find the start of the data"
            span=re.search('msg:',packet[0][3].load).span()
            start=span[1]
            data=packet[0][3].load[start+1:]

            f2.write(data)
            #f2.write('\n')  

            f1.close()
            f2.close()
        sys.stdout.flush()

def receive(ip, iface, loss,filter="icmp", rc_pkt=[]):
    
    top=int(100-100*loss)

    key=random.randint(1,100)

    if key in range(1,top):

        sniff(iface = iface, filter= filter,timeout=15,prn = action(ip, rc_pkt).custom_action)
        
    else:
        print("can't receive the packet\n")

def packetQueue():
    print(packet_counts)
    print(packet_queue)

fire.Fire(receive)
#packetQueue()