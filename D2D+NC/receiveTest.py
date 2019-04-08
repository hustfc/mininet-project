from scapy.all import sniff, sendp
from scapy.all import Packet
from scapy.all import ShortField, IntField, LongField, BitField

import sys
import struct
import time
from collections import Counter
import fire

packet_counts = Counter()
packet_queue = []

class action:
    def __init__(self, IP, rc_pkt):
        self.ip = IP
        self.rc_pkt = rc_pkt
    def custom_action(self, packet):
        key = tuple([packet[0][1].src, packet[0][1].dst])
        #if packet[0][1].dst == self.ip:
        packet_queue.append(packet[0][3].load)
        self.rc_pkt.append(packet[0][3].load)
        packet_counts.update([key])
        print('Receive Packet #%d: %s ==> %s' % (sum(packet_counts.values()), packet[0][1].src, packet[0][1].dst))
        print(packet.sprintf("raw : %Raw.load%"))
        now = time.time()
        print("receive_time: " + "%.6f" % float(now) + "\n")
        sys.stdout.flush()

def receive(ip, iface, filter='udp', rc_pkt=[]):
    sniff(iface = iface, filter= filter, prn = action(ip, rc_pkt).custom_action)

def packetQueue():
    print(packet_counts)
    print(packet_queue)

fire.Fire(receive)
packetQueue()