import re
Pkts = {}
datas = {}
filename1 = '/Users/fanc/Documents/GitHub/mininet-project/D2D+NC/Log/DU_Log.txt'

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
        print(temp)
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
        data = list(temp[e5:])   #string to list

        # print("filename:%s filename:%s\n" % (T_filename,filename))
        Pkts["%d" % int(T_index)] = True
        datas["%d" % int(T_index)] = data
        count += 1

        lenth -= 1
    print('pkts:', Pkts)
    print('datas', datas)
