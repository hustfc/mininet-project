import random

# 模拟没有NC环境下面的吞吐量
ratioAPtoRU = 0.3
ratioAPtoDU = 0.1
ratioDUtoRU = 0.1
packet = list(range(1, 32))
counts = []
count = 0
for j in range(1000):
    DU_pkt = []
    RU_pkt = []
    # AP广播
    for i in range(len(packet)):
        topDU = int(100 * (1 - ratioAPtoDU))
        topRU = int(100 * (1 - ratioAPtoRU))
        num1 = random.randint(1, 101)
        num2 = random.randint(1, 101)
        if num1 in range(1, topDU + 1):
            DU_pkt.append(packet[i])
        if num2 in range(1, topRU + 1):
            RU_pkt.append(packet[i])

    # DU转发
    for i in range(len(DU_pkt)):
        topDU_RU = int(100 * (1 - ratioDUtoRU))
        num = random.randint(1, 101)
        if num in range(1, topDU_RU + 1):
           RU_pkt.append(DU_pkt[i])
    counts.append(len(set(RU_pkt)))
    print(counts)
for j in range(len(counts)):
    count += counts[j]
count = count / len(counts)
print(count)

