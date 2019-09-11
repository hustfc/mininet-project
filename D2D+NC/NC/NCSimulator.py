def stringToList(s):
    if s == '':
        return []
    s = s[1:len(s) - 2]
    s = s.replace(' ', '')
    return [int(i) for i in s.split(',')]


total = 0
count = 0
counts = []
filename = "/Users/fanc/Documents/GitHub/mininet-project/D2D+NC/Log/miss.txt"
with open(filename, 'r') as f:
    buffer = f.readlines()
    print(len(buffer))
for i in range(len(buffer)):
    context = buffer[i]
    if context[0] == 'A':
        counts.append(32)
    else:
        missList = stringToList(context)
        print(missList)
        counts.append(32-len(missList))
print(counts)

for j in range(len(counts)):
    count += counts[j]
count = count / len(counts)
print("cout", count)
print("throutput", (count/32)*1024)