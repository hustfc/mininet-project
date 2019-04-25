from numpy import random
import math
from mininet.log import info
# from mn_wifi import propagationModels
# from random import gauss



def energy(sta, ap, time):
    staPosition = sta.params['position'][0:2]
    apPosition = ap.params['position'][0:2]
    distance = math.sqrt((staPosition[0] - apPosition[0]) ** 2 + (staPosition[1] - apPosition[1]) ** 2)
    info('distance : %.2fm\n' % distance)
    txpower = float(ap.params['txpower'][0])
    info('txpower: %.3fdbm\n' % txpower)
    transmitPower = 10 ** (txpower / 10) / 1000
    info('transmitPower: %fW\n' % transmitPower)
    alpha = 2.0
    t, receiveEnergy = 0, 0
    interval = 0.0001
    while t <= time:
        h = random.normal(0, 1)
        receivePower = transmitPower * (distance ** (-alpha)) * (h ** 2)
        receiveEnergy += receivePower * interval
        t += interval
    info('after %ds receive energy : %fJ\n' % (time, receiveEnergy))