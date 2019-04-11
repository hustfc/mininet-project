import GF
import random

w = 8
total = 2 ** w
gf = GF.GF(w)

def vector_mul(a, b):
    res = 0
    for i in range(len(a)):
        res = gf.add(res, gf.mul(a[i], b[i]))
    return res

def matrix_mul(a, b):
    a_row = len(a)
    b_col = len(b[0])
    b_row = len(b)
    result = []
    for i in range(a_row):
        row_vector = []
        for j in range(b_col):
            row_vector.append(vector_mul(a[i], [b[i][j] for i in range(b_row)]))
        result.append(row_vector)
    return result

def CharToByte(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = ord(matrix[i][j])


def DU_Encode(pkts, datas, size):
    count = 0
    data_matrix = []
    for i in range(len(pkts)):
        if pkts[i] == True:
            count += 1
            data_matrix.append(datas[i])
    CharToByte(data_matrix)
    coe_matrix = [([0] * count) for i in range(size)]    # size * count
    for i in range(size):
        for j in range(count):
            coe_matrix[i][j] = random.randint(1, 2 ** w - 1)
    encode_matrix = matrix_mul(coe_matrix, data_matrix)
    print('coe', coe_matrix)
    print('data', data_matrix)
    print('encode', encode_matrix)
    return coe_matrix, encode_matrix

#Unit test
# pkts = {0:True, 1:True}
# datas = {0:['a','b','c','d'], 1:['m','n','p','q']}
# DU_Encode(pkts, datas, 4)
