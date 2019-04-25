# -*- coding: utf8 -*-
import random
import numpy as np
#from sympy import *
from math import log
'''
a_i :the price of per unit rate
R_k :the rate from k-th UE to Client that can be realized
b_k :the price that k-th UE demands
P_k :the Pow that BS buy from k-th UE device 
P_k_max: input params 
'''
def game(beta_k):
    P_k = 0
    b_k = 0
    P_k_max = 10.0 # use for test
    P_k_min = 0 # the min POW that guarantee the QOS of D2D

    "原本 D32， 现在D1000"
    
    D = 1000 # the improtance of every packet

    W = 15000000.0  # 15 Mhz BandWidth
    a = 0.000000001 #10e-9 
    #R_k = 6.0 #mbps
    # beta_k = 1.0
    G_k = 10.0
    c = 0.4
    P_c = 24
    G_c = 1.0
    sigma_qua= 1
    alpha = a * W / log(2)

    # print('alpha:',alpha)

    g_k = (P_c * G_c + sigma_qua) / G_k

    # print('g_k:',g_k)
    b_k_min = alpha * D / (g_k + P_k_max)
    b_k_max = alpha * D / (g_k + P_k_min)

    # print('squr:',alpha * c * D / ( beta_k * g_k ))
    b_k_star =  ( alpha * c * D / ( beta_k * g_k ) ) ** 0.5

    P_k_star = ( alpha * D * beta_k * g_k / c) ** 0.5 -g_k

    A_k = (alpha * D * beta_k /c) ** 0.5
    # print('A_k:',A_k)

    # print('A_k **2 - 4*P_k_max:',A_k **2 - 4*P_k_max)


    if A_k ** 2 >= 4 * P_k_max:
        x1 = ( (A_k + (A_k **2 - 4*P_k_max ) **0.5 )/ 2)  ** 2
        x2 = ( (A_k - (A_k **2 - 4*P_k_max ) **0.5 )/ 2)  ** 2
        x3 = ( (A_k - (A_k **2 - 4*P_k_min ) **0.5 )/ 2)  ** 2
        x4 = ( (A_k + (A_k **2 - 4*P_k_min ) **0.5 )/ 2)  ** 2
        # print("x1 x2 x3 x4",x1,x2,x3,x4)
        if g_k <= x3 or g_k >= x4:
            P_k = P_k_min
            b_k = b_k_max
        elif (g_k > x3 and g_k < x2) or (g_k > x1 and g_k < x4):
            b_k = b_k_star
            P_k = P_k_star
        else:
            P_k = P_k_max
            b_k = b_k_min
    elif A_k **2 > 4 * P_k_min:
        x3 = ( (A_k + (A_k **2 - 4*P_k_min ) **0.5 )/ 2)  ** 2
        x4 = ( (A_k + (A_k **2 - 4*P_k_min ) **0.5 )/ 2)  ** 2
        if g_k <= x3 or g_k >= x4:
            P_k = P_k_min
            b_k = b_k_max
        else:
            b_k = b_k_star
            P_k = P_k_star
    else:
        b_k = b_k_star
        P_k = P_k_star
    result = []
    result.append(P_k)
    result.append(b_k)
    # print('a * w * d:',a * W * D)
    # print('lognum:',P_k * G_k / (P_c * G_c + sigma_qua))
    # print('log:',log(1 + P_k * G_k / (P_c * G_c + sigma_qua),2))
    U_BS = a * W * D * log((1 + P_k * G_k / (P_c * G_c + sigma_qua)),2) - b_k * P_k
    # print(U_BS)
    result.append(U_BS)
    U_UE = (beta_k * b_k - c) * P_k
    result.append(U_UE)
    # print(result)
    return result
if __name__ == '__main__':
    game(0.9)