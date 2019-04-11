from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

import threading

def command(host, arg):
    result = host.cmd(arg)
    return result

def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    AP1 = net.addAccessPoint('AP1', ssid="ap-ssid", mode="g", channel="1", position='5,10,0', range=100)

    RU = net.addStation('RU', wlans=2, position='30,5,0', ip='10.0.0.1/8,10.0.0.2/8', mac='00:00:00:00:00:01,00:00:00:00:00:02')

    DU = net.addStation('DU', wlans=2, position='15,15,0', ip='10.0.0.3/8,10.0.0.4/8', mac='00:00:00:00:00:03,00:00:00:00:00:04')

    c1 = net.addController('c1')

    net.setPropagationModel(model="logDistance", exp=5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    net.plotGraph(max_x=40, max_y=40)
    AP1.setIP('10.0.0.10', intf='AP1-wlan1')

    info("*** Creating links\n")
    net.addLink(AP1, RU)
    net.addLink(AP1, DU)
    net.addLink(RU, cls=adhoc, ssid='adhocNet', mode='g', channel=5, ht_cap='HT40+')
    net.addLink(DU, cls=adhoc, ssid='adhocNet', mode='g', channel=5, ht_cap='HT40+')

    info("*** Starting network\n")
    net.build()
    c1.start()
    AP1.start([c1])

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()