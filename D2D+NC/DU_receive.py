from scapy.all import sniff, sendp
from mininet.log import info

import sys
import time
from collections import Counter
import fire
import random
import re
from NC.DU_encode import DU_Encode
import os

packet_counts = Counter()
packet_queue = []
global total
total = 32
size = 32
Pkts = {}
datas = {}   #store data dictionary
for i in range(total):
    Pkts[i] = False
    datas[i] = []

# flag = True # before log delete the previous log file
class action:
    def __init__(self, IP, rc_pkt):
        self.ip = IP
        self.rc_pkt = rc_pkt

    def custom_action(self, packet):
        loss = 0
        top = int(100 - 100 * loss)
        num = random.randint(1, 101)
        key = tuple([packet[0][1].src, packet[0][1].dst])
        if num in range(1, top + 1) and packet[0][1].dst == self.ip:  # receive.py  second param is its own ip
            "offload the msg from packet"
            span3 = re.search('total:', packet[0][3].load).span()
            s3 = span3[0]
            e3 = span3[1]
            span4 = re.search('index:', packet[0][3].load).span()
            s4 = span4[0]
            e4 = span4[1]
            span5 = re.search('data:', packet[0][3].load).span()
            s5 = span5[0]
            e5 = span5[1]
            # global flag
            global total
            total = packet[0][3].load[e3:s4]
            index = packet[0][3].load[e4:s5]
            data = list(packet[0][3].load[e5:])
            Pkts[int(index)] = True
            datas[int(index)] = data
            print(Pkts, datas)
            "write the data"
            filename1 = '/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/DU_Log.txt'

            f1 = open(filename1, "a+")
            packet_queue.append(packet[0][3].load)
            self.rc_pkt.append(packet[0][3].load)
            packet_counts.update([key])
            now = time.time()

            info = "receive_time: " + "%.6f" % float(now) + " " + packet[0][3].load
            print("info in action :", info)
            f1.write('Receive Packet #%d: %s ==> %s : %s' % (
                sum(packet_counts.values()), packet[0][1].src, packet[0][1].dst, info))
            f1.write('\n')
            f1.close()
        sys.stdout.flush()


def receive(ip, iface, filter="udp", rc_pkt=[]):
    sniff(iface=iface, filter=filter, timeout=80, prn=action(ip, rc_pkt).custom_action)
    "after sniff,check the packet num and return the missing number"

    filename4 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/pkts.txt"
    with open(filename4, 'a+') as f4:
        f4.write(str(Pkts) + '\n')

    filename5 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/datas.txt"
    with open(filename5, 'a+') as f5:
        f5.write(str(datas) + '\n')

    #next, encode pakts based pkts and datas
    coe_matrix, encode_matrix = DU_Encode(Pkts, datas, size)

    filename6 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/coe.txt"
    filename7 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/encoded.txt"

    with open(filename6, 'a+') as f6:
        f6.write(str(coe_matrix) + '\n')

    with open(filename7, 'a+') as f7:
        f7.write(str(encode_matrix) + '\n')


    #filename4 = "/home/shlled/mininet-project-fc/Stackelberg/Log/pkts.txt"


def packetQueue():
    print(packet_counts)
    print(packet_queue)


fire.Fire(receive)
#packetQueue()