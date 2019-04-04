from scapy.all import sniff, sendp
from scapy.all import Packet
from scapy.all import ShortField, IntField, LongField, BitField

import sys
import struct
import time
from collections import Counter
import fire
import json

packet_counts = Counter() 
packet_queue = []


class action:
    def __init__(self, IP, rc_pkt):
        self.ip = IP
        self.rc_pkt = rc_pkt
    def custom_action(self, packet):
        key = tuple([packet[0][1].src, packet[0][1].dst])

        if packet[0][1].dst == self.ip:   # receive.py  second param is its own ip 
            
            
            packet_queue.append(packet[0][3].load)
            self.rc_pkt.append(packet[0][3].load)
            packet_counts.update([key])           
            info=packet[0][3].load
            filename='/home/shlled/mininet-wifi/Log/BSLog.json'
            #f=open(filename,"a+")
            temp = {}                       #temp for storage
            data = []
            info=json.loads(info)
            temp["UEIP"]=packet[0][1].src
            temp["UEPOWER"]=info["POWER"]
            temp["UEPRICE"]=info["PRICE"]
            temp["UELOSS"]=info["LOSS"]
            temp["UEMAX"]=info["MAX"]
            data.append(temp)
            with open(filename,'a+') as f:
                json.dump(data,f)
                f.write("\n")
        sys.stdout.flush()

def receive(ip, iface, filter="icmp", rc_pkt=[]):

    sniff(iface = iface, filter= filter,timeout=20,prn = action(ip, rc_pkt).custom_action)
    

def packetQueue():
    print(packet_counts)
    print(packet_queue)

fire.Fire(receive)
#packetQueue()