filename1 = '/Users/fanc/Documents/GitHub/mininet-project/D2D+NC/Log/DU_coe.txt'
size = 32
with open(filename1, 'r') as f:
    buffer = f.readlines()
    start = len(buffer) - (size + 1)
    print(buffer[start])

