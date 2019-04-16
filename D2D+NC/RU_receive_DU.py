# -*- coding: utf-8 -*-
from scapy.all import sniff, sendp
from mininet.log import info

#python DU_send.py 10.0.0.3 RU-wlan0 10.0.0.2
#python RU_receive_DU.py 10.0.0.2 RU-wlan0

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
Pkts = {}  #Pkts from DU
coe = {}   #store coe matrix dictionary
enc = {}
coe_DU = []  #保存来自DU的系数矩阵
enc_DU = []  #保存来自DU的编码数组

#pretreatment
for i in range(total):
    Pkts[i] = False
    coe[i] = []
    enc[i] = []

def stringToList(s):
    if s == '':
        return []
    s = s[1:len(s)-1]
    s = s.replace(' ', '')
    print(s)
    return [int(i) for i in s.split(',')]

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
            span5 = re.search('coe:', packet[0][3].load).span()
            s5 = span5[0]
            e5 = span5[1]
            span6 = re.search('enc:', packet[0][3].load).span()
            s6 = span6[0]
            e6 = span6[1]
            # global flag
            global total
            total = packet[0][3].load[e3:s4]
            index = packet[0][3].load[e4:s5]
            coe_string = packet[0][3].load[e5:s6]
            enc_string = packet[0][3].load[e6:]
            print('coe_string', coe_string, 'enc_string', enc_string)
            Pkts[int(index)] = True
            coe[int(index)] = stringToList(coe_string)
            enc[int(index)] = stringToList(enc_string)
            coe_DU.append(stringToList(coe_string))
            enc_DU.append(stringToList(enc_string))
            print(Pkts, coe, enc)

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

pkts_AP = {}
datas_AP = {}   #data receive from AP


#读取之间AP给RU发送的文件
def readAPtoRU():
    filename1 = '/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/RU_count_AP.txt'
    filename2 = '/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/RU_pkts_AP.txt'
    filename3 = '/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/RU_datas_AP.txt'
    with open(filename1, 'r') as f1:
        buffer1 = f1.readlines()
        length = int(buffer1[-1])
        print('length', length)
    with open(filename2, 'r') as f2:
        buffer2 = f2.readlines()
    with open(filename3, 'r') as f3:
        buffer3 = f3.readlines()
    pkt_start = len(buffer2) - (length + 1)
    data_start = len(buffer3) - (length + 1)
    # print(buffer2[pkt_start:])
    # print(buffer3[data_start:])
    for i in range(length):
        index = int(buffer2[pkt_start + i])
        pkts_AP[index] = True
        vector = stringToList(buffer3[data_start + i][0:-1])  # take out '\n'
        # print(vector)
        datas_AP[index] = vector

#将矩阵转化为列
def GetMatrixCol(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    result = []
    for j in range(cols):
        result.append([matrix[i][j] for i in range(rows)])
    return result

def Decode():
    #参数：pkts_AP & datas_AP ：建立稀疏矩阵    coe_DU & enc_DU : 建立增广矩阵   Pkts ：确定填充的位置
    coe_matrix = []  #总的系数矩阵
    encoded_matrix = []  #总的编码矩阵
    for i in range(len(pkts_AP)):
        if pkts_AP[i] == True:
            coe_vector = [0] * size
            coe_vector[i] = 1
            enc_vector = datas_AP[i]
            coe_matrix.append(coe_vector)
            encoded_matrix.append(enc_vector)
    print('coe:', coe_matrix)
    print('enc:', encoded_matrix)
    #建立增广矩阵
    augment_matrix = [([0] * size) for i in range(len(coe_DU))]        #len(coe_DU) * size
    #coe_cols = GetMatrixCol(coe_DU)
    index = 0  # 指向列的指针
    for j in range(len(Pkts)):
        if Pkts[j] == True:
            for i in range(len(augment_matrix)):
                augment_matrix[i][j] = coe_DU[i][index]
            index += 1
    coe_matrix.extend(augment_matrix)
    encoded_matrix.extend(enc_DU)
    print('coe_matrix', coe_matrix)
    print('encoded_matrix', encoded_matrix)
    return coe_matrix, encoded_matrix




def receive(ip, iface, filter="udp", rc_pkt=[]):
    sniff(iface=iface, filter=filter, timeout=5, prn=action(ip, rc_pkt).custom_action)
    "after sniff,check the packet num and return the missing number"

    filename4 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/RU_pkts.txt"
    with open(filename4, 'a+') as f4:
        f4.write(str(Pkts) + '\n')

    filename5 = "/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/RU_datas.txt"
    with open(filename5, 'a+') as f5:
        f5.write('RU receive from DU coefficient matrix:\n')
        f5.write(str(coe) + '\n')
        f5.write('RU receive from DU encoded matrix:\n')
        f5.write(str(enc) + '\n')

    print("RU begin Decode>>>>>>>>>")
    #read AP to RU file and receive



def packetQueue():
    print(packet_counts)
    print(packet_queue)


fire.Fire(receive)
#packetQueue()