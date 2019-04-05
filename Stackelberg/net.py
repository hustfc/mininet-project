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
# def sendpacket(src,dst,num):


def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       wmediumd_mode=interference, configure4addr=True)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid="ap1-ssid", mode="g",
                             channel="1", position='30,30,0')
    ap2 = net.addAccessPoint('ap2', ssid="ap2-ssid", mode="g",
                             channel="1", position='40,60,0')

    "h6 is askinng for datas while h1,h2,h3 are the UE "

    h1 = net.addHost('h1', ip="10.0.0.1", position='30,10,0')
    h2 = net.addHost('h2', ip="10.0.0.2", position='20,20,0')
    h3 = net.addHost('h3', ip="10.0.0.3", position='30,20,0')
    # h4 = net.addHost('h4', ip="10.0.0.4", position='40,20,0')
    # h5 = net.addHost('h5', ip="10.0.0.5", position='50,20,0')
    h6 = net.addHost('h6', ip="10.0.0.6", position='60,20,0')
    BS = net.addHost('BS', ip="10.0.0.7", position='30,40,0')
    c0 = net.addController('c0')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Adding Link\n")
    net.addLink(ap1, ap2, cls=_4address)  # ap1=ap, ap2=client
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
    ap2.start([c0])

    # info("*** first cycle BS collect the info of UE\n")
    # try:
    #     thread.start_new_thread(command,(BS,"python RInfo.py 10.0.0.7 BS-eth0"))
    #     thread.start_new_thread(command,(h1,"python SInfo.py 10.0.0.1 h1-eth0 10.0.0.7"))
    #     thread.start_new_thread(command,(h2,"python SInfo.py 10.0.0.2 h2-eth0 10.0.0.7"))
    #     thread.start_new_thread(command,(h3,"python SInfo.py 10.0.0.3 h3-eth0 10.0.0.7"))

    # except:
    #     print("first cycle error")
    # time.sleep(22) #wait for collect UE info
    # print("first cycle finish")

    # # the BS start to create the UE's info
    # BSLog={
    #     "h1":{},
    #     "h2":{},
    #     "h3":{}
    #     # "h4":{},
    #     # "h5":{},
    #     # "h6":{}
    # }
    # BSLog["h1"]["flag"]=False
    # BSLog["h2"]["flag"]=False
    # BSLog["h3"]["flag"]=False
    # filename1 = "/home/shlled/mininet-wifi/Log/BSLog.json"
    # with open(filename1,'r') as f1:
    #     buffer=f1.readlines()
    #     lenth=len(buffer)
    #     print(lenth)
    #     while lenth>0:
    #         temp=buffer[lenth-1]

    #         temp=json.loads(temp)
    #         print(temp,"\n")
    #         if temp[0]["UEIP"] == "10.0.0.1" and BSLog["h1"]["flag"] == False:
    #             BSLog["h1"]["flag"] = True
    #             BSLog["h1"]["IP"] = temp[0]["UEIP"]
    #             BSLog["h1"]["POWER"] = temp[0]["UEPOWER"]
    #             BSLog["h1"]["PRICE"] = temp[0]["UEPRICE"]
    #             BSLog["h1"]["LOSS"] = temp[0]["UELOSS"]
    #             BSLog["h1"]["MAX"] = temp[0]["UEMAX"]
    #         elif temp[0]["UEIP"] == "10.0.0.2" and BSLog["h2"]["flag"] == False:
    #             BSLog["h2"]["flag"] = True
    #             BSLog["h2"]["IP"] = temp[0]["UEIP"]
    #             BSLog["h2"]["POWER"] = temp[0]["UEPOWER"]
    #             BSLog["h2"]["PRICE"] = temp[0]["UEPRICE"]
    #             BSLog["h2"]["LOSS"] = temp[0]["UELOSS"]
    #             BSLog["h2"]["MAX"] = temp[0]["UEMAX"]
    #         elif temp[0]["UEIP"] == "10.0.0.3" and BSLog["h3"]["flag"] == False:
    #             BSLog["h3"]["flag"] = True
    #             BSLog["h3"]["IP"] = temp[0]["UEIP"]
    #             BSLog["h3"]["POWER"] = temp[0]["UEPOWER"]
    #             BSLog["h3"]["PRICE"] = temp[0]["UEPRICE"]
    #             BSLog["h3"]["LOSS"] = temp[0]["UELOSS"]
    #             BSLog["h3"]["MAX"] = temp[0]["UEMAX"]
    #         lenth-=1
    #         if BSLog["h1"]["flag"] == True and BSLog["h2"]["flag"] == True and BSLog["h3"]["flag"]==True:
    #            break

    # "BS use UE info to decide which UE send which packet"

    info("*** Start sending information\n")
    "BS should not control the behavior of UE,what UE has send isn't full"
    thread_list = []
    t1 = MyThread(command, args=(h2, "python receive.py 10.0.0.2 h2-eth0"))
    # t1 = threading.Thread(target=command,args=(h2,"python receive.py 10.0.0.2 h2-eth0"))
    thread_list.append(t1)
    distance = getDistance(h1, h2)
    t2 = MyThread(command, args=(h1, "python send.py  10.0.0.1 h1-eth0 10.0.0.2 %s msg.txt" % distance))
    # t2 = threading.Thread(target=command,args=(h1,"python send.py  10.0.0.1 h1-eth0 10.0.0.2 0.15 msg.txt"))
    thread_list.append(t2)
    t1.start()
    t2.start()
    for t in thread_list:
        t.join()
    #miss_pkt = thread_list[0].get_result()

    info("*** Start sending the miss pkg\n")
    #filename4 = '/home/shlled/mininet-project-fc/Stackelberg/Log/miss.txt'
    filename4 = '/media/psf/Home/Documents/GitHub/mininet-project/Stackelberg/Log/miss.txt'
    while True:
        with open(filename4, 'r+') as f4:
            buffer = f4.readlines()
            lenth = len(buffer)
            miss_pkt = buffer[lenth - 1]
        info('miss:', miss_pkt)
        if miss_pkt == 'None\n':
            print("finish collet")
            break
        t3 = threading.Thread(target=command, args=(h2, "python receive.py 10.0.0.2 h2-eth0"))
        thread_list.append(t3)
        t4 = threading.Thread(target=command,
                              args=(h1, "python send.py 10.0.0.1 h1-eth0 10.0.0.2 %s msg.txt False '%s'" % (distance, miss_pkt)))
        thread_list.append(t4)
        t3.start()
        t4.start()
        for t in thread_list:
            t.join()

    # index=0
    # num = 0 #packge number
    # "find the size of the data"
    # filename2 = "/home/shlled/mininet-wifi/Log/msg.txt"
    # f2 = open(filename2,'r')
    # buffer2= f2.readlines()
    # lenth = len(buffer2)
    # f2.close()
    # while index<lenth:
    #     flag = True
    #     while flag:
    #         try:
    #             thread.start_new_thread(command,(h2,"python receive.py 10.0.0.2 h2-eth0 0.15"))
    #             thread.start_new_thread(command,(h1,"python send.py 10.0.0.1 h1-eth0 10.0.0.2 msg.txt %d" % num))
    #         except:
    #             print("send error")
    #         time.sleep(18) # wait thread finish
    #         print("send finish")
    #         filename3 = "/home/shlled/mininet-wifi/Log/final.txt"
    #         f3 = open(filename3,'r')
    #         buffer3 = f3.readlines()
    #         temp = len(buffer3)
    #         f3.close()
    #         if temp == index + 10 or temp >= lenth:
    #             flag = False
    #     index += 10
    #     num += 1
    info("*** Running CLI\n")
    CLI_wifi(net)

    # h2.cmd("python receive.py 10.0.0.2 h2-eth0")
    # h1.cmd("python send.py 10.0.0.1 h1-eth0 10.0.0.2")

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()