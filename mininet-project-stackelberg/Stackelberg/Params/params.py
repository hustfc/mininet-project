import math
from mininet.log import info

def getDistance(h1, h2):
    # position1 = h1.params['position'].replace(' ', '').split(',')
    # position2 = h2.params['position'].replace(' ', '').split(',')
    # distance = math.sqrt((int(position1[0]) - int(position2[0])) ** 2 + (int(position1[1]) - int(position2[1])) ** 2)
    distance = math.sqrt((int(h1.params['position'][0]) - int(h2.params['position'][0])) ** 2 + (int(h1.params['position'][1]) - int(h2.params['position'][1])) ** 2)
    return distance