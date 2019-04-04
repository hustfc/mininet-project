import math

def getDistance(h1, h2):
    #获取两个节点的距离
    position1 = h1.params['position'][0:2]
    position2 = h2.params['position'][0:2]
    distance = math.sqrt((position1[0] - position2[0]) ** 2 + (position1[1] - position2[1]) ** 2)
    return distance