import GF
import numpy as np

w = 8
total = 2 ** w

gf = GF.GF(w)


def vector_mul(a, b):
    res = 0
    for i in range(len(a)):
        res = gf.add(res, gf.mul(a[i], b[i]))
    return res


def encode(packet):
    size = len(packet)
    cols = int(size)
    coefficients_matrix = np.random.randint(0, 2 ** w - 1, size=[cols, size])
    encode_matrix = []
    for i in range(cols):
        encode_matrix.append(vector_mul(coefficients_matrix[i], packet))
    return coefficients_matrix, encode_matrix



