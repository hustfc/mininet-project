# -*- coding:utf-8 -*-
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
from sympy import  *
from math import log
def game(a,S):
    C = 3 #RU对包的基本支付单价
    C_DU = 2 #DU传输一个包的成本
    C_BS = 1    #BS传输一个包的成本
    N = 32 #总包数
    # a = 2  #满足因子 作为自变量
    x = Symbol('x')
    # expr1 = x*(C_BS+(C*N*S)/(log(a)*(a+S*x)))
    expr1 = C_BS + C*N*S/(log(a)*(a+S*x))+x*(-C*N*S*S)/(log(a)*(a+S*x)*(a+S*x))-C_DU
    # N1 = solve(diff(expr1,x),x)
    ans = solve(expr1,x)
    lenth = len(ans)
    N1 = ans[0]
    # print('dad', ans)
    for i in range(0,lenth):
        if ans[i]>0:
            N1 = ans[i]
    if N1>0:
        temp = int(N1)
    else:
        N1 = 0
        temp = 0
    U_L =temp * (C_BS + C*N*S/(log(a)*(a+S*temp)))-C_DU*temp #向下取整的时候的效益
    temp = temp+1
    U_H = temp * (C_BS + C*N*S/(log(a)*(a+S*temp)))-C_DU*temp #向上取整的时候的效益
    if U_L>U_H:
        N1 = temp -1
        U_DU = U_L
    else:
        N1 = temp
        U_DU = U_H
    b = C_BS + C*N*S/(log(a)*(a+S*N1))
    # print('dadad',b)
    U_BS = C*N*log(a+S*N1, a)-b*N1-(N-N1)*C_BS
    result = [N1,b,U_BS,U_DU]
    # filename = 'Ulity20.txt'
    # with open(filename,'a+') as f:
    #     f.write(str(result))
    #     f.write('\n')
    # # print(result)
    return result
'''
考虑满足因子对
'''

B_set = []
N_set = []
for a in range(2,11):
    result = game(a,0.2)
    B_set.append(result[1])
    N_set.append(result[0])
plt.xlabel('satisfaction factor',fontsize = 10)
plt.xlim(2,9)
plt.ylabel('ES',fontsize = 10)
x = [i for i in range(2,11)]
plt.plot(x,B_set,marker = 'o',linestyle = ':',color = 'goldenrod',label='b')
plt.plot(x,N_set,marker = '^',color = 'cadetblue',label='N_r')
plt.grid()
plt.legend()
plt.show()