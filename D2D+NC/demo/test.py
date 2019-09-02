filename = '/Users/fanc/Documents/GitHub/mininet-project/D2D+NC/Log/miss.txt'
success = 0
loss = 0
with open(filename, 'r') as f:
    buffer = f.readlines()
    length = len(buffer)
    for i in range(length):
        if buffer[i][0] == 'A':
            success += 1
        else:
            loss += 1
print('success',success)
print('loss', loss)
print('rate', float(success / length))