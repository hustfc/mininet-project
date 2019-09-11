# -*- coding: utf-8 -*-
from scapy.all import sniff, sendp
from mininet.log import info

#python APSend.py 10.0.0.1 AP-wlan0 10.0.0.2 10.0.0.3
#python RU_receive_AP.py 10.0.0.2 RU-wlan0

import time
from collections import Counter
import fire
import random
import re
import os
import sys

packet_counts = Counter()
packet_queue = []
global total
total = 32
size = 32
Pkts = {}
datas = {}   #store data dictionary
for i in range(total):
    Pkts[i] = False
    datas[i] = ''

# flag = True # before log delete the previous log file
class action:
    def __init__(self, IP, rc_pkt):
        self.ip = IP
        self.rc_pkt = rc_pkt

    def custom_action(self, packet):
        loss = 0.25
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
            data = packet[0][3].load[e5:]
            Pkts[int(index)] = True
            datas[int(index)] = data
            print(Pkts, datas)
            "write the data"
            filename1 = '/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/RU_Log.txt'

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

#re-receive:True，表示RU产生了丢包，需要AP重新发送编码数据
def receive(ip, iface, re_receive = False, filter="icmp", rc_pkt=[]):
    if re_receive == False:

        sniff(iface=iface, filter=filter, timeout=6, prn=action(ip, rc_pkt).custom_action)
        "after sniff,check the packet num and return the missing number"

        filename4 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/RU_pkts_AP.txt"
        filename5 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/RU_datas_AP.txt"
        filename6 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/RU_count_AP.txt"

        true_count = 0

        with open(filename4, 'a+') as f4:
            for i in range(len(Pkts)):
                if Pkts[i] == True:
                    f4.write(str(i) + '\n')
                    true_count += 1
            f4.write('\n')


        with open(filename5, 'a+') as f5:
            for i in range(len(datas)):
                if Pkts[i] == True:
                    f5.write(datas[i] + '\n')
            f5.write('\n')

        with open(filename6, 'a+') as f6:
            f6.write(str(true_count) + '\n')

    else:
        # python RU_receive_AP.py 10.0.0.2 RU-wlan0 True(必须与接收DU同时测试，要不然ACK已经压栈)
        filename7 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/RU_original.txt"
        original = []
        with open(filename7, 'r') as f7:
            buffer7 = f7.readlines()
            start = len(buffer7) - (size + 1)
            for i in range(size):
                original.append(stringToList(buffer7[start + i][0:-1]))
            print('original:', original)

        filename8 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/miss.txt"
        with open(filename8, 'r') as f8:
            buffer8 = f8.readlines()
            if buffer8[-1][0:-1] == 'ACK':
                miss_pkt = []
            else:
                miss_pkt = stringToList(buffer8[-1][0:-1])
        print('miss_pkt', miss_pkt)
        if miss_pkt != []:
            filename8 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/APSend.txt"
            with open(filename8, 'r') as f8:
                buffer8 = f8.readlines()
                send_start = len(buffer8) - (size + 1)
                new_pkt_string = []
                for item in miss_pkt:
                    new_pkt_string.append(buffer8[send_start + item])
                print('new_string', new_pkt_string)
                new_pkt_list = []
                for i in range(len(new_pkt_string)):
                    new_pkt_list.append(stringToList(new_pkt_string[i][0:-1]))
                print('new_list', new_pkt_list)
                print('0,1', new_pkt_list[0][0], new_pkt_list[0][1])
                for m in range(len(new_pkt_list)):
                    for i in range(len(new_pkt_list[m])):
                        original[i][miss_pkt[m]] = new_pkt_list[m][i]
        print('original', original)
        print("Decode Finish")
        print("Write to File>>>>>>>>>>")
        filename6 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/RU_msg.txt"
        original_string = ''
        for i in range(len(original)):
            for j in range(len(original[0])):
                original_string += chr(int(original[i][j]))
        print('txt:', original_string)
        with open(filename6, 'a+') as f6:
            f6.write(original_string)
        print("Write File Finished")
        time.sleep(1)
        print("Return ACK")
        # filename8 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/miss.txt"
        # with open(filename8, 'a+') as f8:
        #     f8.write('ACK\n')


def packetQueue():
    print(packet_counts)
    print(packet_queue)

def stringToList(s):
    if s == '':
        return []
    s = s[1:len(s)-1]
    s = s.replace(' ', '')
    return [int(i) for i in s.split(',')]





fire.Fire(receive)
#packetQueue()