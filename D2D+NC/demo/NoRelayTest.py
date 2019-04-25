import random
packs = list(range(0, 32))
print(packs)
lossRU = 0.3
lossDU = 0.1
times = 10000
success, loss = 0, 0
for t in range(times):
    packRU = []
    packDU = []
    for i in range(len(packs)):
        randRU = random.randint(1, 101)
        topRU = 100 * (1 - lossRU)
        if randRU in range(1, int(topRU) + 1):
            packRU.append(packs[i])
        randDU = random.randint(1, 101)
        topDU = 100 * (1 - lossDU)
        if randDU in range(1, int(topDU) + 1):
            packDU.append(packs[i])
    print("RU", packRU)
    print("DU", packDU)
    for i in range(len(packDU)):
        randDU = random.randint(1, 101)
        topDU = 100 * (1 - lossDU)
        if randDU in range(1, int(topDU) + 1):
            packRU.append(packDU[i])
    print("DU-RU", packRU)
    setAP = set(packs)
    setRu = set(packRU)
    if setAP == setRu:
        success += 1
    else:
        loss += 1
print(success)
print(loss)
print(float(success / times))