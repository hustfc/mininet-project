# -*- coding: utf-8 -*-
size = 4
pkts_AP = {0:True, 1:False, 2:True, 3:False}
datas_AP = {0:[1,2,3,4], 1:[], 2:[4,5,6,7], 3:[]}
coe_DU = [[1,2,3],[6,4,9],[5,7,2],[21,6,2]]
enc_DU = [[1,2,3,4],[5,6,4,9],[8,1,7,12],[5,8,1,3]]
Pkts = {0:False, 1:True, 2:True, 3:True}

def Decode():
    #参数：pkts_AP & datas_AP ：建立稀疏矩阵    coe_DU & enc_DU : 建立增广矩阵   Pkts ：确定填充的位置
    coe_matrix = []  #总的系数矩阵
    encoded_matrix = []  #总的编码矩阵
    for i in range(len(pkts_AP)):
        if pkts_AP[i] == True:
            coe_vector = [0] * size
            coe_vector[i] = 1
            enc_vector = datas_AP[i]
            coe_matrix.append(coe_vector)
            encoded_matrix.append(enc_vector)
    print('coe:', coe_matrix)
    print('enc:', encoded_matrix)
    #建立增广矩阵
    augment_matrix = [([0] * size) for i in range(len(coe_DU))]        #len(coe_DU) * size
    #coe_cols = GetMatrixCol(coe_DU)
    index = 0  # 指向列的指针
    for j in range(len(Pkts)):
        if Pkts[j] == True:
            for i in range(len(augment_matrix)):
                augment_matrix[i][j] = coe_DU[i][index]
            index += 1
    coe_matrix.extend(augment_matrix)
    encoded_matrix.extend(enc_DU)
    print('coe_matrix', coe_matrix)
    print('encoded_matrix', encoded_matrix)
    return coe_matrix, encoded_matrix
Decode()