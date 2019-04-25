# -*- coding:utf-8 -*-
#!/usr/bin/python
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, _4address
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
# from send import send
# from receive import receive
from Params.params import getDistance

import threading
import json
from game import game
class MyThread(threading.Thread):

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


"function for exec cmd"


def command(host, arg):
    result = host.cmd(arg)
    return result


# "function for create a thread for sending a certern packet "


def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       wmediumd_mode=interference)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid="ap1-ssid", mode="g",
                             channel="1", position='5,6,0',range=40)
    # ap2 = net.addAccessPoint('ap2', ssid="ap2-ssid", mode="g",
    #                          channel="1", position='10,10,0',range=40)

    "h6 is askinng for datas while h1,h2,h3 are the UE "

    h1 = net.addStation('h1', position='5,5,0', ip = '10.0.0.1',mac='00:00:00:00:00:01', range=5)
    h2 = net.addStation('h2', position='10,5,0', ip = '10.0.0.2',mac='00:00:00:00:00:02', range=5)
    h3 = net.addStation('h3', position='0,5,0', ip = '10.0.0.3',mac='00:00:00:00:00:03', range=5)
    # h4 = net.addStation('h4', position='5,5,0', ip = '10.0.0.4',mac='00:00:00:00:00:04', range=5)
    # h5 = net.addStation('h5', position='5,5,0', ip = '10.0.0.5',mac='00:00:00:00:00:05', range=5)
    h6 = net.addStation('h6', position='5,5,0', ip = '10.0.0.6',mac='00:00:00:00:00:06', range=5)
    BS = net.addStation('BS', position='5,5,0', ip = '10.0.0.7',mac='00:00:00:00:00:07', range=5)

    c0 = net.addController('c0')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    # print(h1.params['position'])

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Adding Link\n")
    # net.addLink(ap1, ap2, cls=_4address)  
    net.addLink(h1, ap1)
    net.addLink(h2, ap1)
    net.addLink(h3, ap1)
    # net.addLink(h4, ap1)
    # net.addLink(h5, ap1)
    net.addLink(h6, ap1)
    net.addLink(BS, ap1)
    # net.plotGraph(max_x=100, max_y=100)

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    #ap2.start([c0])

    info("*** first cycle BS collect the info of UE\n")
    thread_list = []
    t1 = threading.Thread(target=command, args=(BS,"python RInfo.py 10.0.0.7 BS-wlan0"))
    thread_list.append(t1)
    t1.start()
    t2 = threading.Thread(target=command, args=(h1,"python SInfo.py 10.0.0.1 h1-wlan0 10.0.0.7"))
    thread_list.append(t2)
    t2.start()
    t2.join()
    t3 = threading.Thread(target=command, args=(h2,"python SInfo.py 10.0.0.2 h2-wlan0 10.0.0.7"))
    thread_list.append(t3)
    t3.start()
    t3.join()
    t4 = threading.Thread(target=command, args=(h3,"python SInfo.py 10.0.0.3 h3-wlan0 10.0.0.7"))
    thread_list.append(t4)
    t4.start()
    t4.join()
    
    t1.join()
    #wait for collect UE info

    print("*** first cycle finish")

    # the BS start to create the UE's info
    BSLog={
        "h1":{},
        "h2":{},
        "h3":{}
    }
    BSLog["h1"]["flag"]=False
    BSLog["h2"]["flag"]=False
    BSLog["h3"]["flag"]=False
    filename1 = "/media/psf/Home/Documents/GitHub/mininet-project/mininet-project-stackelberg/Stackelberg/Log/BSLog.json"
    with open(filename1,'r') as f1:
        buffer=f1.readlines()
        lenth=len(buffer)
        print(lenth)
        while lenth>0:
            temp=buffer[lenth-1]
            temp=json.loads(temp)
            if temp[0]["UEIP"] == "10.0.0.1" and BSLog["h1"]["flag"] == False:
                BSLog["h1"]["flag"] = True
                BSLog["h1"]["IP"] = temp[0]["UEIP"]
                BSLog["h1"]["POWER"] = temp[0]["UEPOWER"]
                # BSLog["h1"]["PRICE"] = temp[0]["UEPRICE"]
                BSLog["h1"]["Integrity"] = temp[0]["Integrity"]
                BSLog["h1"]["MAX"] = temp[0]["UEMAX"]
            elif temp[0]["UEIP"] == "10.0.0.2" and BSLog["h2"]["flag"] == False:
                BSLog["h2"]["flag"] = True
                BSLog["h2"]["IP"] = temp[0]["UEIP"]
                BSLog["h2"]["POWER"] = temp[0]["UEPOWER"]
                # BSLog["h2"]["PRICE"] = temp[0]["UEPRICE"]
                BSLog["h2"]["Integrity"] = temp[0]["Integrity"]
                BSLog["h2"]["MAX"] = temp[0]["UEMAX"]
            elif temp[0]["UEIP"] == "10.0.0.3" and BSLog["h3"]["flag"] == False:
                BSLog["h3"]["flag"] = True
                BSLog["h3"]["IP"] = temp[0]["UEIP"]
                BSLog["h3"]["POWER"] = temp[0]["UEPOWER"]
                # BSLog["h3"]["PRICE"] = temp[0]["UEPRICE"]
                BSLog["h3"]["Integrity"] = temp[0]["Integrity"]
                BSLog["h3"]["MAX"] = temp[0]["UEMAX"]
            lenth-=1
            if BSLog["h1"]["flag"] == True and BSLog["h2"]["flag"] == True and BSLog["h3"]["flag"]==True:
               break
    # print(BSLog)
    
    "BS use UE info to decide which UE send which packet"
    "求出均衡时每个博弈对的价格和功率，然后排序"
    Balance = []
    
    for i in range(1,4):
        # print(game(BSLog["h%d" % i]["Integrity"]))
        result = game(BSLog["h%d" % i]["Integrity"]) #博弈函数，传入参数为上一轮的完整性因子
        BSLog["h%d" % i]["P_k"] = result[0]#将返回结果写入字典
        BSLog["h%d" % i]["b_k"] = result[1]
        BSLog["h%d" % i]["F_BS"] = result[2]
        BSLog["h%d" % i]["F_UE"] = result[3]
        Balance.append(BSLog["h%d" % i])
    Balance = sorted(Balance,key = lambda x:x['F_BS'],reverse = True)#将中继设备按照基站收益排序
    print(Balance)
    # result1 = game()

    "确定用哪个中继设备来进行传输"
    index = 0 
    K = len(Balance)

    while index < K:
        Power = Balance[index]["POWER"]
        Pow = Balance[index]["P_k"]
        if Power > Pow:
            UEIP = Balance[index]["IP"]
            break
        index += 1
    if UEIP == '10.0.0.1':
        host = h1
        hostip = '10.0.0.1'
        hostname = 'h1'
        P_k = Balance[0]["P_k"]
        F_UE = Balance[0]["F_UE"]
    elif UEIP == '10.0.0.2':
        host = h2
        hostip = '10.0.0.2'
        hostname = 'h2'
        P_k = Balance[0]["P_k"]
        F_UE = Balance[0]["F_UE"]
    elif UEIP == '10.0.0.3':
        host = h3
        hostip = '10.0.0.3'
        hostname = 'h3'
        P_k = Balance[0]["P_k"]
        F_UE = Balance[0]["F_UE"]
    else :
        "基站的功率和收益怎么计算还没想好"
        host = BS
        hostip = '10.0.0.7'
        hostname = 'BS'
        P_k = 0
        F_UE = 0
    print("best choice:",hostname)
    info("*** Start sending first information\n")

    "before sending clear the cahce"
    
    filename1 = '/media/psf/Home/Documents/GitHub/mininet-project/mininet-project-stackelberg/Stackelberg/Log/6.txt'
    with open(filename1,'r+') as f1:
        f1.truncate()

    "BS should not control the behavior of UE,what UE has send isn't full"
    thread_list = []
    t1 = MyThread(command, args=(h6, "python receive.py 10.0.0.6 h6-wlan0"))
    thread_list.append(t1)
    distance = getDistance(host, h6)

    # info("python send.py  %s %s-wlan0 10.0.0.6 %s %s %s msg.txt\n" % (hostip, hostname, distance, P_k, F_UE))

    t2 = MyThread(command, args=(host,
             "python send.py  %s %s-wlan0 10.0.0.6 %s %s %s msg.txt" % (hostip, hostname, distance, P_k, F_UE)))
    # t2 = MyThread(command, args=(h1, "python send.py  10.0.0.1 h1-wlan0 10.0.0.2 %s 5 5 msgs.txt" % (distance)))
    
    thread_list.append(t2)
    t1.start()
    t2.start()
    for t in thread_list:
        t.join()
    info("*** Start sending the miss pkg\n")
    filename4 = '/media/psf/Home/Documents/GitHub/mininet-project/mininet-project-stackelberg/Stackelberg/Log/miss.txt'
    #filename4 = '/media/psf/Home/Documents/GitHub/mininet-project/Stackelberg/Log/miss.txt'
    while True:
        with open(filename4, 'r+') as f4:
            buffer = f4.readlines()
            lenth = len(buffer)
            miss_pkt = buffer[lenth - 1]
        info('miss:', miss_pkt)
        if miss_pkt == 'None\n':
            print("finish collet")
            break
        t3 = threading.Thread(target=command, args=(h6, "python receive.py 10.0.0.6 h6-wlan0"))
        thread_list.append(t3)
        # print("python send.py  %s %s-wlan0 10.0.0.6 %s %s %s msg.txt False '%s'\n" % (hostip, hostname, distance, P_k, F_UE, miss_pkt))
        t4 = threading.Thread(target=command,
                              args=(host, 
                            #   "python send.py 10.0.0.1 h1-wlan0 10.0.0.2 %s 5 5 msg.txt False '%s'" % (distance, miss_pkt)))
                              "python send.py  %s %s-wlan0 10.0.0.6 %s %s %s msg.txt False '%s'" % (hostip, hostname, distance, P_k, F_UE, miss_pkt)))
        thread_list.append(t4)
        t3.start()
        t4.start()
        for t in thread_list:
            t.join()

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
