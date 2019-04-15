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
            row_vector.append(vector_mul(a[i], [b[m][j] for m in range(b_row)]))
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
    #print('data_matrix', data_matrix)
    coe_matrix = [([0] * count) for i in range(size)]    # size * count
    for i in range(size):
        for j in range(count):
            coe_matrix[i][j] = random.randint(1, 2 ** w - 1)
    encode_matrix = matrix_mul(coe_matrix, data_matrix)
    # print('coe', coe_matrix)
    # print('data', data_matrix)
    # print('encode', encode_matrix)
    return coe_matrix, encode_matrix

#Unit test
# pkts = {0: True, 1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True, 8: True, 9: True, 10: True, 11: True, 12: True, 13: True, 14: True, 15: True, 16: True, 17: True, 18: True, 19: True, 20: True, 21: True, 22: True, 23: True, 24: True, 25: True, 26: True, 27: True, 28: True, 29: True, 30: True, 31: True}
# datas = {0: [' ', 'e', 'b', ' ', '.', 'l', 't', 'e', ' ', 'u', 'y', 's', 'o', 'o', ' ', 'e', 'e', 'b', 'h', 'g', ' ', 'c', 'a', 'o', 'h', 'i', ' ', 'a', 'o', 's', 'o', ' '], 1: [' ', ' ', 'u', 's', ' ', 'p', 'o', 'r', 't', 'l', ',', 'e', 'n', 'n', 'f', 'n', 'y', 'e', 'e', ' ', 'w', 'c', 'g', 'l', 'a', 's', 't', 'l', 'p', '.', 'r', 'i'], 2: ['W', 'e', 's', 'o', 'L', 's', 'm', 's', 'h', 't', ' ', ' ', 'o', 'e', 'o', ' ', ' ', 'c', ' ', 'C', 'h', 'e', 'e', 'd', 'n', ' ', 'h', 's', 'l', ' ', 'y', 's'], 3: ['i', 'c', 'i', ' ', 'e', ' ', 'e', ' ', 'e', ' ', 't', 'l', 'u', 's', 'r', 't', 'c', 'a', 's', 'h', 'i', 'n', ' ', ' ', ' ', 'b', 'e', 'o', 'e', 'W', ' ', ' '], 4: ['t', 'o', 'n', 'a', 'a', 't', 'r', 's', 'y', 'l', 'h', 'a', 'n', ' ', 'e', 'h', 'a', 'u', 'a', 'i', 'c', 't', 'i', 'p', 'f', 'i', ' ', ' ', ',', 'e', 'b', 't'], 5: ['h', 'n', 'e', 's', 'r', 'h', 's', 't', ' ', 'a', 'e', 'n', 'c', 'h', 'i', 'e', 'n', 's', 'm', 'n', 'h', '.', 's', 'o', 'i', 'g', 's', 'd', ' ', ' ', 'y', 'h'], 6: [' ', 'o', 's', ' ', 'n', 'e', ',', 'a', 'f', 'n', 'r', 'g', 'e', 'a', 'g', 'y', ' ', 'e', 'e', 'e', ' ', '\n', ' ', 'e', 'v', ' ', 'a', 'i', 'l', 'c', ' ', 'e'], 7: ['t', 'm', 's', 't', 'i', 'm', ' ', 'r', 'i', 'g', 'e', 'u', ' ', 's', 'n', ' ', 'f', ' ', '.', 's', 'm', ' ', 'p', 'm', 'e', 'c', 'm', 'f', 'e', 'a', 's', ' '], 8: ['h', 'y', ' ', 'o', 'n', ' ', 's', 't', 'n', 'u', ' ', 'a', 'f', ' ', ' ', 'h', 'i', 't', ' ', 'e', 'a', ' ', 'r', 's', ' ', 'o', 'e', 'f', 't', 'n', 't', 'n'], 9: ['e', ',', 'c', ' ', 'g', 't', 'o', ' ', 'd', 'a', 'a', 'g', 'o', 't', 'p', 'e', 'g', 'h', 'S', ' ', 'k', 'S', 'o', '.', 't', 'u', ' ', 'i', ' ', ' ', 'u', 'e'], 10: [' ', ' ', 'o', 'w', ' ', 'o', ' ', 't', ' ', 'g', 'r', 'e', 'r', 'h', 'e', 'a', 'u', 'e', 'o', 'j', 'e', 'e', 'f', ' ', 'h', 'n', 't', 'c', 'a', 'k', 'd', 'c'], 11: ['d', 't', 'o', 'i', 't', ' ', 'm', 'o', 'i', 'e', 'e', ',', ' ', 'e', 'o', 'r', 'r', ' ', ' ', 'u', 's', 'c', 'o', 'T', 'o', 't', 'i', 'u', 'l', 'e', 'y', 'e'], 12: ['e', 'h', 'p', 'n', 'h', 'w', 'o', ' ', 't', ' ', ' ', ' ', 't', ' ', 'p', ' ', 'e', 'w', 'm', 's', ' ', 'o', 'u', 'h', 'u', 'r', 'm', 'l', 'o', 'e', 'i', 's'], 13: ['v', 'e', 'e', ' ', 'e', 'i', 'r', 'l', ' ', 't', 'f', 'w', 'h', 'd', 'l', 'd', ' ', 'o', 'o', 't', 't', 'n', 'n', 'e', 's', 'y', 'e', 't', 'n', 'p', 'n', 's'], 14: ['e', ' ', 'r', 't', ' ', 'n', 'e', 'e', 'i', 'o', 'o', 'h', 'e', 'i', 'e', 'i', 'o', 'r', 's', ' ', 'h', 'd', 'd', ' ', 'a', ' ', ',', 'y', 'e', ' ', 'g', 'a'], 15: ['l', 'w', 'a', 'h', 'l', ' ', ' ', 'a', 's', ' ', 'u', 'i', 'm', 'f', ' ', 'f', 'u', 'd', 't', 'i', 'e', 'l', ',', 'h', 'n', 'f', ' ', ' ', ' ', 't', ' ', 'r'], 16: ['o', 'o', 't', 'e', 'o', 'm', 'a', 'r', ' ', 'm', 'r', 'c', '.', 'f', 'f', 'f', 't', 's', ' ', 'g', 'm', 'y', ' ', 'i', 'd', 'u', 't', 'f', 't', 'r', 't', 'y'], 17: ['p', 'r', 'i', ' ', 'c', 'o', 'n', 'n', 't', 'a', ' ', 'h', ' ', 'e', 'e', 'e', ' ', ' ', 'o', 'n', ' ', ',', 'e', 's', ' ', 'l', 'h', 'o', 'o', 'a', 'h', ' '], 18: ['m', 'l', 'o', 'b', 'a', 'r', 'd', ' ', 'h', 's', 't', ' ', 'A', 'r', 'e', 'r', 't', 's', 'f', 'o', 'h', ' ', 's', 't', 'y', 'l', 'e', 'r', ' ', 'c', 'e', 'p'], 19: ['e', 'd', 'n', 'o', 'l', 'e', ' ', 'm', 'e', 't', 'o', 'i', 's', 'e', 'l', 'e', 'h', 'o', ' ', 'r', 'a', 'C', 'p', 'o', 'e', ' ', ' ', ' ', 't', 'e', ' ', 'a'], 20: ['n', ' ', ' ', 'o', ' ', ' ', 'm', 'a', ' ', 'e', 'n', 's', ' ', 'n', ' ', 'n', 'e', 'u', 't', 'e', 'v', 'h', 'e', 'r', 'a', 'o', 'o', 't', 'h', ' ', 'p', 'r'], 21: ['t', 'i', 'w', 'm', 'l', 'C', 'o', 'n', 'm', 'r', 'e', ' ', 'd', 't', 'c', 't', ' ', 'n', 'h', ' ', 'e', 'i', 'c', 'y', 'r', 'f', 'l', 'h', 'e', 'o', 'o', 't'], 22: [' ', 's', 'i', 'i', 'a', 'h', 'r', 'd', 'o', '.', 's', 'h', 'i', ' ', 'o', ' ', 'm', 'd', 'e', 't', ' ', 'n', 'i', ' ', 's', ' ', 'd', 'e', ' ', 'f', 'e', ' '], 23: ['o', ' ', 't', 'n', 'n', 'i', 'e', 'a', 's', '\n', ' ', 'a', 'f', 'm', 'n', 't', 'e', ' ', 'm', 'h', 's', 'e', 'a', 'o', ' ', 'c', ' ', ' ', 'f', ' ', 'm', 'l'], 24: ['f', 's', 'h', 'g', 'g', 'n', ' ', 'r', 't', ' ', 'i', 'r', 'f', 'e', 'f', 'o', 'a', 'a', ' ', 'e', 'p', 's', 'l', 'f', 'm', 'h', 'p', 'l', 'o', 't', 's', 'e'], 25: [' ', 'e', ' ', ' ', 'u', 'e', 'f', 'i', ' ', ' ', 'n', 'd', 'e', 'a', 'u', 'n', 'n', 'l', 's', ' ', 'e', 'e', 'l', ' ', 'a', 'a', 'o', 'o', 'r', 'h', '.', 'a'], 26: ['C', 'e', 'C', 'm', 'a', 's', 'o', 'n', 'd', 'F', ' ', ' ', 'r', 'n', 's', 'e', 'i', 'm', 'p', 't', 'c', ' ', 'y', 'm', 'k', 'r', 'e', 'c', 'e', 'e', ' ', 'r'], 27: ['h', 'k', 'h', 'a', 'g', 'e', 'r', ',', 'i', 'i', 'C', 't', 'e', 'i', 'e', 's', 'n', 'o', 'e', 'o', 'i', 'l', ' ', 'o', 'e', 'm', 'm', 'a', 'i', ' ', 'S', 'n'], 28: ['i', 'i', 'i', 'r', 'e', ' ', 'e', ' ', 'f', 'r', 'h', 'o', 'n', 'n', 'd', ',', 'g', 's', 'a', 'n', 'a', 'a', 't', 'r', 's', '.', ' ', 'l', 'g', 'h', 'o', 'i'], 29: ['n', 'n', 'n', 'k', ' ', 'c', 'i', 'b', 'f', 's', 'i', ' ', 't', 'g', ' ', ' ', 's', 't', 'k', 'e', 'l', 'n', 'h', 'e', ' ', ' ', 'i', ' ', 'n', 'i', ' ', 'n'], 30: ['e', 'g', 'a', 'e', 'h', 'u', 'g', 'u', 'i', 't', 'n', 'p', ' ', 's', 'w', 't', ',', ' ', 'i', 's', ' ', 'g', 'e', ' ', 't', 'A', 's', 'p', 'e', 's', 'i', 'g'], 31: ['s', ' ', ',', 't', 'e', 's', 'n', 't', 'c', 'l', 'e', 'r', 't', ',', 'h', 'h', ' ', 't', 'n', ',', 'a', 'u', ' ', 't', 'h', 't', ' ', 'e', 'r', 't', 't', ' ']}
# DU_Encode(pkts, datas, 32)
