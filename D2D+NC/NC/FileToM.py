def FileToS(filename):
    with open(filename, 'r') as f:
        strings = f.read()
        return strings

def SToFile(strings, filename):
    with open(filename, 'w') as f:
        f.write(strings)

def StringToM(subString, size):
    # string to matix
    if len(subString) != size * size:
        raise Exception('size error')
    matrix = [(['0'] * size) for i in range(size)]
    k = 0
    for j in range(size):
        for i in range(size):
            matrix[i][j] = subString[k]
            k += 1
    return matrix

def FToMatrix(filename):
    #file to matrix
    strings = FileToS(filename)
    results = []
    size = 32
    total = size * size
    j = 0
    for i in range(len(strings)):
        if (i + 1) % total == 0:
            subString = strings[j:i+1]
            j = i + 1
            results.append(StringToM(subString, size))
    if len(strings) > j:
        subString = strings[j:len(strings)] + ' ' * (total - (len(strings) - j))
    results.append(StringToM(subString, size))
    return results


# filename1 = '/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/msg.txt'
# filename2 = '/media/psf/Home/Documents/GitHub/mininet-project/D2D+NC/Log/RU.txt'
# result = FToMatrix(filename1)
# for item in result:
#     print(item)