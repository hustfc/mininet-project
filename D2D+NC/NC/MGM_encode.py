import GF
import numpy as np
import random

w = 8
total = 2 ** w

gf = GF.GF(w)


def vector_mul(a, b):
    res = 0
    for i in range(len(a)):
        res = gf.add(res, gf.mul(a[i], b[i]))
    return res


def encode(packets):
    size = len(packets[0])
    maxGen = len(packets)
    l = 1
    encode_matrix = []
    coe_matrix = []
    gen_packets = [packets[0]]

    #预处理每一代的包
    for i in range(1, maxGen):
        packet = gen_packets[i - 1] + packets[i]
        gen_packets.append(packet)
    print('MGM包')
    print(gen_packets)

    #对每一代的包进行编码
    while l <= maxGen:
        coefficients_matrix = [([0] * (size * l)) for q in range(size * l)]
        for m in range(size * l):
            for n in range(size * l):
                coefficients_matrix[m][n] = random.randint(0, 2 ** w - 1)
        #coefficients_matrix = np.random.randint(0, 2 ** w - 1, size=[size * l, size * l])
        coe_matrix.extend(coefficients_matrix)
        matrix = []
        for i in range(size * l):
            matrix.append(vector_mul(coefficients_matrix[i], gen_packets[l - 1]))
        encode_matrix.extend(matrix)
        l += 1


    #处理系数矩阵
    maxLen = len(coe_matrix[-1])
    for i in range(len(coe_matrix)):
        length = len(coe_matrix[i])
        for j in range(maxLen - length):
            coe_matrix[i].append(0)
    print('系数矩阵')
    for item in coe_matrix:
        print(item)
    #return coefficients_matrix, matrix

    print('编码包')
    print(encode_matrix)
    return coe_matrix, encode_matrix
# packets = [[1,2],[3,4],[5,6]]
# encode(packets)
