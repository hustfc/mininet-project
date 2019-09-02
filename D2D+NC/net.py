# -*- coding: utf-8 -*-
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

import threading
from NC.FileToM import *


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

def command(host, arg):
    result = host.cmd(arg)
    return result


def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    #AP1 = net.addAccessPoint('AP1', ssid="ap-ssid", mode="g", channel="1", position='5,10,0', range=100)
    AP = net.addStation('AP', position='5,10,0', ip='10.0.0.1', mac='00:00:00:00:00:01')

    RU = net.addStation('RU', position='30,5,0', ip='10.0.0.2', mac='00:00:00:00:00:02')

    DU = net.addStation('DU', position='15,15,0', ip='10.0.0.3', mac='00:00:00:00:00:03')

    c1 = net.addController('c1')

    net.setPropagationModel(model="logDistance", exp=5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    net.plotGraph(max_x=40, max_y=40)
    #AP1.setIP('10.0.0.10', intf='AP1-wlan1')

    info("*** Creating links\n")
    net.addLink(AP, cls=adhoc, ssid='adhocNet', mode='g', channel=5, ht_cap='HT40+')
    net.addLink(RU, cls=adhoc, ssid='adhocNet', mode='g', channel=5, ht_cap='HT40+')
    net.addLink(DU, cls=adhoc, ssid='adhocNet', mode='g', channel=5, ht_cap='HT40+')

    info("*** Starting network\n")
    net.build()
    c1.start()
    #AP1.start([c1])

    info("*** Starting Send information\n")
    #获得总包的个数
    for index in range(30):
        file = '/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log'
        filename1 = '%s/msg.txt' % file
        results = FToMatrix(filename1)
        nums = len(results)
        for i in range(nums):
            info("round ", i, "\n")
            info("AP to DU and RU\n")
            t1 = MyThread(command, args=(DU, "python DU_receive.py 10.0.0.3 DU-wlan0"))
            t2 = MyThread(command, args=(RU, "python RU_receive_AP.py 10.0.0.2 RU-wlan0"))
            t3 = MyThread(command, args=(AP, "python APSend.py 10.0.0.1 AP-wlan0 10.0.0.2 10.0.0.3 %s False" % i))
            t1.start()
            t2.start()
            t3.start()
            t1.join()
            t2.join()
            t3.join()
            info("DU send encoded packets to RU\n")
            t4 = MyThread(command, args=(DU, "python DU_send.py 10.0.0.3 DU-wlan0 10.0.0.2"))
            t5 = MyThread(command, args=(RU, "python RU_receive_DU.py 10.0.0.2 RU-wlan0"))
            t4.start()
            t5.start()
            t4.join()
            t5.join()
            info("AP reSend to RU\n")
            t6 = MyThread(command, args=(DU, "python APSend.py 10.0.0.1 AP-wlan0 10.0.0.2 10.0.0.3 %s True" % i))
            t7 = MyThread(command, args=(RU, "python RU_receive_AP.py 10.0.0.2 RU-wlan0 True"))
            t6.start()
            t7.start()
            t6.join()
            t7.join()
            info("ACK %d\n" % i)

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()