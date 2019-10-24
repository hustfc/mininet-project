import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
from sympy import  *
from math import log
def game(S):
    C = 3 #RU对包的基本支付单价
    C_DU = 2 #DU传输一个包的成本
    C_BS = 1    #BS传输一个包的成本
    N = 32 #总包数
    a = 2  #满足因子
    # e = 0.1  #丢包率
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
    filename = 'Ulity20.txt'
    with open(filename,'a+') as f:
        f.write(str(result))
        f.write('\n')
    # print(result)
    return result
'''
绘图 
'''
C = 3  # RU对包的基本支付单价
C_DU = 2  # DU传输一个包的成本
C_BS = 1  # BS传输一个包的成本
N = 32 #总包数
a = 2  # 满足因子


U_BS_ES = []
U_BS_Non = []

e = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
for i in range(0,len(e)):
    U_Non =C * N - N * C_BS
    U_BS_Non.append(U_Non)
    U_ES = game(1-e[i])[3]
    U_BS_ES.append(U_ES)


# 绘制柱状图
# name_list = ['e = 0.1', 'e = 0.2', 'e = 0.3', 'e = 0.4']
# x = list(range(len(U_BS_Non)))
# total_width, n = 0.8, 2
# width = total_width / n
# plt.bar(x, U_BS_Non, width=width, label='Non-ES', fc='r')
# for i in range(len(x)):
#     x[i] = x[i] + width
# plt.bar(x, U_BS_ES, width=width, label='ES', tick_label=name_list, fc='g')
# x= [0.1, 0.2, 0.3, 0.4]
#绘制折线图
plt.plot(e, U_BS_ES, marker = '*', color = 'teal', label = 'ES')
plt.plot(e, U_BS_Non, marker= 'o', linestyle=':', color='royalblue', label = 'Non-ES')

plt.xlabel("loss rate")
plt.xlim(0,1)
plt.ylabel("Utility of BS")
# plt.title("不采用中继（Non-ES）与采用中继博弈均衡（ES）时基站效益对比图")
plt.legend()
plt.show()