from scapy.all import sniff, sendp
from mininet.log import info

import sys
import time
from collections import Counter
import fire
import random
import re
import os

packet_counts = Counter()
packet_queue = []
global total
size = 32

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
            data = packet[0][3].load[e5 + 1:]
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
            f1.close()
        sys.stdout.flush()


def receive(ip, iface, filter="icmp", rc_pkt=[]):
    sniff(iface=iface, filter=filter, timeout=20, prn=action(ip, rc_pkt).custom_action)
    "after sniff,check the packet num and return the missing number"
    Pkts = {}
    datas = {}   #store data dictionary
    global total
    # print("global filename:%s\n" % filename)
    # print("global total:%s\n" % total)
    total = int(total)
    for i in range(0, total):
        Pkts["%d" % i] = False
    miss_pkt = []  # save the index of missing numbers

    filename1 = '/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/DU_Log.txt'

    with open(filename1, 'r+') as f:
        buffer = f.readlines()
        lenth = len(buffer) - 1

        "find which packet has been received"
        global count
        count = 0

        while lenth >= 0:
            global Flag
            Flag = True
            temp = buffer[lenth]
            # print(temp)
            span3 = re.search('total:', temp).span()
            s3 = span3[0]
            e3 = span3[1]
            span4 = re.search('index:', temp).span()
            s4 = span4[0]
            e4 = span4[1]
            span5 = re.search('data:', temp).span()
            s5 = span5[0]
            e5 = span5[1]
            "temp data of each line,use for cmp"
            T_index = temp[e4:s5]
            data = temp[e5+1:]   # True?**********

            # print("filename:%s filename:%s\n" % (T_filename,filename))
            Pkts["%d" % int(T_index)] = True
            datas["%d" % int(T_index)] = data
            count += 1
            # if all of the dic is true, then exit and consist the file
            # global Flag
            for i in range(0, total):
                if Pkts["%d" % i] == False:
                    # global Flag
                    Flag = False
            # global Flag
            if Flag:
                break
            lenth -= 1
        # print('pkts:', Pkts)
        #下一步工作：根据datas字典和Pkts字典来进行编码

        #filename4 = "/home/shlled/mininet-project-fc/Stackelberg/Log/pkts.txt"
        filename4 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/pkts.txt"
        with open(filename4, 'a+') as f4:
            f4.write(str(Pkts) + '\n')

    if Flag:   #all packages received
        "consist the file"
        #filename3 = "/home/shlled/mininet-project-fc/Stackelberg/Log/miss.txt"
        filename3 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/miss.txt"
        with open(filename3, 'a+') as f3:
            f3.write('None')
            f3.write('\n')
        with open(filename1, 'r') as f1:
            buffer = f1.readlines()
            lenth = len(buffer)
            # filename2 = '/home/shlled/mininet-wifi/Log/new%s' % filename
            filename2 = '/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/new%s' % filename
            f2 = open(filename2, 'a+')
            current_index = 0

            # while current_index < total:
            #     i = lenth - 1
            #     while i >= 0:
            #         temp = buffer[i]
            #         span1 = re.search('filename:', temp).span()
            #         s1 = span1[0]
            #         e1 = span1[1]
            #         span3 = re.search('total:', temp).span()
            #         s3 = span3[0]
            #         e3 = span3[1]
            #         span4 = re.search('index:', temp).span()
            #         s4 = span4[0]
            #         e4 = span4[1]
            #         span5 = re.search('data:', temp).span()
            #         s5 = span5[0]
            #         e5 = span5[1]
            #         T_index = int(temp[e4:s5])
            #         if T_index == current_index:
            #             f2.write(temp[e5:])
            #             current_index += 1
            #             break;
            f2.close()


    else:  #append miss packet
        "calculate the loss"

        loss = (float(total) - float(count)) / float(total)

        # print("total:%d count:%d loss:%f" % (total, count, loss))

        for i in range(0, total):
            if Pkts["%d" % i] == False:
                miss_pkt.append(i)
        info('miss in receive', miss_pkt)
        # filename3 = "/home/shlled/mininet-wifi/Log/miss.txt"
        # if miss_pkt == []:
        #     miss_pkt.append(-1)
        filename3 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/miss.txt"
        with open(filename3, 'a+') as f3:
            f3.write(str(miss_pkt))
            f3.write('\n')


def packetQueue():
    print(packet_counts)
    print(packet_queue)


fire.Fire(receive)
packetQueue()