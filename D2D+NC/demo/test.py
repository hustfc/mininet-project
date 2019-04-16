# -*- coding: utf-8 -*-
filename1 = '/Users/fanc/Documents/GitHub/mininet-project/D2D+NC/Log/RU_count_AP.txt'
filename2 = '/Users/fanc/Documents/GitHub/mininet-project/D2D+NC/Log/RU_pkts_AP.txt'
filename3 = '/Users/fanc/Documents/GitHub/mininet-project/D2D+NC/Log/RU_datas_AP.txt'
size = 32
pkts = {}
datas = {}
#中文注释
for i in range(size):
    pkts[i] = False
    datas[i] = []

def stringToList(s):
    if s == '':
        return []
    s = s[1:len(s)-1]
    s = s.replace(' ', '')
    return [int(i) for i in s.split(',')]

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
print(buffer2[pkt_start:])
print(buffer3[data_start:])
for i in range(length):
    index = int(buffer2[pkt_start + i])
    pkts[index] = True
    vector = stringToList(buffer3[data_start + i][0:-1])   #take out '\n'
    #print(vector)
    datas[index] = vector
print('pkts', pkts)
print('datas', datas)