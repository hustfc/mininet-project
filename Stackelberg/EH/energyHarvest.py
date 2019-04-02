from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from energy import energy

def topology():
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', position='5,5,0', ip='10.0.0.1', mac='00:00:00:00:00:01', range=5)
    sta2 = net.addStation('sta2', position='15,5,0', ip='10.0.0.2', mac='00:00:00:00:00:02', range=5)
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1', position='10,10,0', range=40)

    c1 = net.addController('c1')

    net.setPropagationModel(model="logDistance", exp=2)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    net.plotGraph(max_x=20, max_y=20)
    ap1.setIP('10.0.0.3',intf='ap1-wlan1')

    info("*** Creating links\n")
    net.addLink(ap1, sta1)
    net.addLink(ap1, sta2)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])

    info('*** Energy Harvest\n')
    energy(sta1, ap1, 10)
    info('***\n')

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()