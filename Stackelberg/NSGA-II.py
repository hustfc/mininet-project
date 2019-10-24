# -*- coding:utf-8 -*-
#Importing required modules
import math
import random
import matplotlib.pyplot as plt
import json
import os
#
'''
采用多轮的思路是每次计算出最优解之后从其中选出增加其gains,但是其丢包率是不变的，能量也没有改变，
在多轮之后根据fairness变化的情况
'''
class UserEqu:
    Count = 0
    def __init__(self, name, ip, link_e, gains, F_BS, F_UE, N1, b):
        self.name = name
        self.ip = ip 
        self.link_e = link_e
        self.gains = gains
        self.F_BS = F_BS
        self.F_UE = F_UE
        self.N1 = N1
        self.b = b
        self.rank = 0
        UserEqu.Count += 1
#中继设备初始化
UE1 = UserEqu('UE1', '10.0.0.1', 0.10, 0.1, 195.43396778377053 , 78.65153714963657, 28, 5.808983469629878)
UE2 = UserEqu('UE2', '10.0.0.2', 0.15, 0.1, 225.13105279816864 , 100.58333991774799, 26, 6.868589996836461)
UE3 = UserEqu('UE3', '10.0.0.3', 0.20, 0.1, 247.54588421179346, 114.93967520628291, 24, 7.789153133595121)
UE4 = UserEqu('UE4', '10.0.0.4', 0.25, 0.1, 263.82627716639126, 125.27621813097173, 22, 8.694373551407805)
UE5 = UserEqu('UE5', '10.0.0.5', 0.30, 0.1, 281.2885847713523, 133.2092290621777, 21, 9.343296622008463)
UE6 = UserEqu('UE6', '10.0.0.6', 0.35, 0.1, 295.65261736458785, 139.53538286618212, 20, 9.976769143309106)
UE7 = UserEqu('UE7', '10.0.0.7', 0.40, 0.1, 307.3441330874717, 144.74137184593536, 19, 10.617966939259755)
UE8 = UserEqu('UE8', '10.0.0.8', 0.45, 0.1, 316.6832853264184, 149.12205673189075, 18, 11.284558707327264)
UE9 = UserEqu('UE9', '10.0.0.9', 0.50, 0.1, 323.907429967555, 152.86335767704668, 17, 11.991962216296864)

UE10 = UserEqu('UE10', '10.0.0.10', 0.52, 0.1, 329.8844332053065, 154.24242304735702, 17, 12.07308370866806)
UE11 = UserEqu('UE11', '10.0.0.11', 0.54, 0.1, 335.7181156256853 , 155.5376096652692, 17, 12.149271156780541)
UE12 = UserEqu('UE12', '10.0.0.12', 0.56, 0.1, 341.41466557149556 , 156.7563442953185, 17, 12.220961429136382)
UE13 = UserEqu('UE13', '10.0.0.13', 0.58, 0.1, 346.97993469709525, 157.90520206630933, 17, 12.288541298018195)
UE14 = UserEqu('UE14', '10.0.0.14', 0.60, 0.1, 342.7357413827916, 159.03272265564206, 16, 12.939545165977629)
UE15 = UserEqu('UE15', '10.0.0.15', 0.62, 0.1, 347.94883457954006, 160.1011383304499, 16, 13.00632114565312)
UE16 = UserEqu('UE16', '10.0.0.16', 0.64, 0.1, 353.05137533349597, 161.11368913337236, 16, 13.069605570835773)
UE17 = UserEqu('UE17', '10.0.0.17', 0.66, 0.1, 358.0476844677814, 162.074644990923, 16, 13.129665311932687)
UE18 = UserEqu('UE18', '10.0.0.18', 0.68, 0.1, 352.41945368621595, 162.99002514186787, 15, 13.866001676124526)
UE19 = UserEqu('UE19', '10.0.0.19', 0.70, 0.1, 357.1187768684793, 163.89821349547668, 15, 13.926547566365112)
UE20 = UserEqu('UE20', '10.0.0.20', 0.72, 0.1, 361.72767429801195, 164.76383052001006, 15, 13.984255368000671)

E1 = UserEqu('UE1', '10.0.0.1', 0.10, 0.1, 195.43396778377053 , 78.65153714963657, 28, 5.808983469629878)
E2 = UserEqu('UE2', '10.0.0.2', 0.15, 0.1, 225.13105279816864 , 100.58333991774799, 26, 6.868589996836461)
E3 = UserEqu('UE3', '10.0.0.3', 0.20, 0.1, 247.54588421179346, 114.93967520628291, 24, 7.789153133595121)
E4 = UserEqu('UE4', '10.0.0.4', 0.25, 0.1, 263.82627716639126, 125.27621813097173, 22, 8.694373551407805)
E5 = UserEqu('UE5', '10.0.0.5', 0.30, 0.1, 281.2885847713523, 133.2092290621777, 21, 9.343296622008463)
E6 = UserEqu('UE6', '10.0.0.6', 0.35, 0.1, 295.65261736458785, 139.53538286618212, 20, 9.976769143309106)
E7 = UserEqu('UE7', '10.0.0.7', 0.40, 0.1, 307.3441330874717, 144.74137184593536, 19, 10.617966939259755)
E8 = UserEqu('UE8', '10.0.0.8', 0.45, 0.1, 316.6832853264184, 149.12205673189075, 18, 11.284558707327264)
E9 = UserEqu('UE9', '10.0.0.9', 0.50, 0.1, 323.907429967555, 152.86335767704668, 17, 11.991962216296864)

E10 = UserEqu('UE10', '10.0.0.10', 0.52, 0.1, 329.8844332053065, 154.24242304735702, 17, 12.07308370866806)
E11 = UserEqu('UE11', '10.0.0.11', 0.54, 0.1, 335.7181156256853 , 155.5376096652692, 17, 12.149271156780541)
E12 = UserEqu('UE12', '10.0.0.12', 0.56, 0.1, 341.41466557149556 , 156.7563442953185, 17, 12.220961429136382)
E13 = UserEqu('UE13', '10.0.0.13', 0.58, 0.1, 346.97993469709525, 157.90520206630933, 17, 12.288541298018195)
E14 = UserEqu('UE14', '10.0.0.14', 0.60, 0.1, 342.7357413827916, 159.03272265564206, 16, 12.939545165977629)
E15 = UserEqu('UE15', '10.0.0.15', 0.62, 0.1, 347.94883457954006, 160.1011383304499, 16, 13.00632114565312)
E16 = UserEqu('UE16', '10.0.0.16', 0.64, 0.1, 353.05137533349597, 161.11368913337236, 16, 13.069605570835773)
E17 = UserEqu('UE17', '10.0.0.17', 0.66, 0.1, 358.0476844677814, 162.074644990923, 16, 13.129665311932687)
E18 = UserEqu('UE18', '10.0.0.18', 0.68, 0.1, 352.41945368621595, 162.99002514186787, 15, 13.866001676124526)
E19 = UserEqu('UE19', '10.0.0.19', 0.70, 0.1, 357.1187768684793, 163.89821349547668, 15, 13.926547566365112)
E20 = UserEqu('UE20', '10.0.0.20', 0.72, 0.1, 361.72767429801195, 164.76383052001006, 15, 13.984255368000671)



UES = [UE1,UE2,UE3,UE4,UE5,UE6,UE7,UE8,UE9,UE10,UE11,UE12,UE13,UE14,UE15,UE16,UE17,UE18,UE19,UE20]
UES2 = [E1,E2,E3,E4,E5,E6,E7,E8,E9,E10,E11,E12,E13,E14,E15,E16,E17,E18,E19,E20]
#第一个函数计算采用某一个中继设备之后的Fairness的变化情况
def Fairness(x): #x表示的是传入设备的编号，也即染色体
    #传入的x是浮点数，要转化成整数
    x = round(x)
    U_total = 0
    U_link_s = 0     
    for i in range(0,len(UES)):
        U_total += UES[i].gains
        U_link_s += (1-UES[i].link_e)
    #加上采用第i个中继设备时的收益来计算fairness
    U_total += UES[x].F_UE
    X=[]
    for i in range(0,len(UES)):
        Ui_overline = ((1-UES[i].link_e)/U_link_s)*U_total
        if UES[i].name == UES[x].name:
            if (UES[i].gains+UES[x].F_UE)<=Ui_overline:
                X.append(UES[i].gains/Ui_overline)
            else:
                X.append(1.0)
        elif UES[i].gains<=Ui_overline:
            X.append(UES[i].gains/Ui_overline)
        else:
            X.append(1.0)
    sum_of_xi = 0
    for i in range(0,len(X)):
        sum_of_xi += X[i]

    sum_of_xi2 = 0
    for i in range(0,len(X)):
        sum_of_xi2 += X[i]**2

    fairness = (sum_of_xi)**2/(len(X)*sum_of_xi2)
    UES[x].fairness = fairness
    return fairness

#Second function to optimize,BS的效益
def Utility(x):
    x= round(x)
    value = UES[x].F_BS
    return value

def index_of(a,list):
    for i in range(0,len(list)):
        if list[i] == a:
            return i
    return -1

#按照function的值来排序
#list1的含义
def sort_by_values(list1, values):
    sorted_list = []
    while(len(sorted_list)!=len(list1)):
        if index_of(min(values),values) in list1: #values中最小值的下标
            sorted_list.append(index_of(min(values),values))
        values[index_of(min(values),values)] = math.inf
    return sorted_list

#NSGA-II's fast non dominated sort,基于帕雷托最优解来计算支配解集
def fast_non_dominated_sort(values1, values2):
    S=[[] for i in range(0,len(values1))]
    front = [[]]
    n=[0 for i in range(0,len(values1))]
    rank = [0 for i in range(0, len(values1))]
    #先计算出第一次的前沿面
    for p in range(0,len(values1)):
        S[p]=[] #p的支配集合
        n[p]=0  #p的支配个数
        for q in range(0, len(values1)):
            if (values1[p] > values1[q] and values2[p] > values2[q]) or (values1[p] >= values1[q] and values2[p] > values2[q]) or (values1[p] > values1[q] and values2[p] >= values2[q]):
                if q not in S[p]:
                    S[p].append(q)
            elif (values1[q] > values1[p] and values2[q] > values2[p]) or (values1[q] >= values1[p] and values2[q] > values2[p]) or (values1[q] > values1[p] and values2[q] >= values2[p]):
                n[p] = n[p] + 1
        if n[p]==0:
            rank[p] = 0
            if p not in front[0]:
                front[0].append(p)
    i = 0
    while(front[i] != []):
        Q=[]
        for p in front[i]:
            for q in S[p]:
                n[q] = n[q] - 1
                if( n[q]==0 ):
                    rank[q]=i+1
                    if q not in Q:
                        Q.append(q)
        i = i+1
        front.append(Q)
    del front[len(front)-1]
    return front

#Function to calculate crowding distance

#采用解的距离有问题，不采用归一化两个目标之间距离差值太大，采用标准化，不能从初始值0开始
def crowding_distance(values1, values2, front):
    distance = [0 for i in range(0,len(front))]
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    distance[0] = 4444444444444444
    distance[len(front) - 1] = 4444444444444444
    #距离计算公式，换种定义
    for k in range(1,len(front)-1):
        distance[k] = distance[k]+ (values1[sorted1[k+1]] - values1[sorted1[k-1]])/(max(values1)-min(values1)) #统一标准化
    for k in range(1,len(front)-1):
        distance[k] = distance[k]+ (values2[sorted2[k+1]] - values2[sorted2[k-1]])/(max(values2)-min(values2))
    return distance

#交叉
def crossover(a,b):
    r=random.random()
    if r>0.5:
        return mutation((a+b)/2)
    else:
        return mutation((a-b)/2)

#突变
def mutation(solution):
    mutation_prob = random.random()
    if mutation_prob <1:
        solution = min_x+(max_x-min_x)*random.random()
    return solution


if __name__=='__main__':
    pop_size = 20
    max_gen = 100
    #初始化
    min_x = 0
    max_x = 19
    cicle = 1
    rand_fair = [0]
    result_fair = [0]
    result_UBS = [] #最终保存 BS效益的数组
    result_URD = [] #最终保存的设备
    result_NRD = []
    while cicle <20:
    #random.random()产生一个(0,1)的随机数,此处在X范围内随机产生一个数
        solution=[min_x+(max_x-min_x)*random.random() for i in range(0,pop_size)] #产生从0到20设备编号解
        gen_no=0
        result=[]
        while(gen_no<max_gen):
            fairness_values = [Fairness(solution[i])for i in range(0,pop_size)]
            utility_values = [Utility(solution[i])for i in range(0,pop_size)]
            non_dominated_sorted_solution = fast_non_dominated_sort(fairness_values[:],utility_values[:])#快速非支配排序返回的front的集合
            print("第",gen_no, "次繁衍的帕累托最优的设备编号为")
            #保存最后一轮的结果
            result = solution
            for valuez in non_dominated_sorted_solution[0]:
                print(round(solution[valuez],3),end=" ")
            print("\n")
            crowding_distance_values=[]
            for i in range(0,len(non_dominated_sorted_solution)):
                crowding_distance_values.append(crowding_distance(fairness_values[:], utility_values[:], non_dominated_sorted_solution[i][:]))
            solution2 = solution[:]
            #产生子代
            while(len(solution2)!=2*pop_size): #新一代种群数量是原种群数量的两倍
                a1 = random.randint(0,pop_size-1) #从种群中随机选择两个个体
                b1 = random.randint(0,pop_size-1)
                solution2.append(crossover(solution[a1],solution[b1]))#从原始的两个个体中交叉产生新的个体
            fairness_values2 = [Fairness(solution2[i])for i in range(0,2*pop_size)]
            utility_values2 = [Utility(solution2[i])for i in range(0,2*pop_size)]
            non_dominated_sorted_solution2 = fast_non_dominated_sort(fairness_values2[:],utility_values2[:])
            crowding_distance_values2=[]
            for i in range(0,len(non_dominated_sorted_solution2)):
                crowding_distance_values2.append(crowding_distance(fairness_values2[:],utility_values2[:],non_dominated_sorted_solution2[i][:]))
            new_solution= []
            for i in range(0,len(non_dominated_sorted_solution2)):
                non_dominated_sorted_solution2_1 = [index_of(non_dominated_sorted_solution2[i][j],non_dominated_sorted_solution2[i]) for j in range(0,len(non_dominated_sorted_solution2[i]))]
                front22 = sort_by_values(non_dominated_sorted_solution2_1[:], crowding_distance_values2[i][:])
                front = [non_dominated_sorted_solution2[i][front22[j]] for j in range(0,len(non_dominated_sorted_solution2[i]))]
                front.reverse()
                for value in front:
                    new_solution.append(value)
                    if(len(new_solution) == pop_size):
                        break
                if (len(new_solution) == pop_size):
                    break
            solution = [solution2[i] for i in new_solution] 
            gen_no = gen_no + 1
        #图示显示每一轮的帕累托前沿面
        fairness = [i  for i in fairness_values]
        utility = [j  for j in utility_values]
        # plt.xlabel('Fairness', fontsize=15)
        # plt.ylabel('F_BS', fontsize=15)
        # plt.scatter(fairness, utility)
        # plt.show()
        #在显示完plot之后，从前沿面中选择出一个点作为解，更新其gains值
        # print(result)
        #version1先从中选取
        IntResult = []
        for i in range(0,len(result)-1):
            IntResult.append(int(round(result[i],0)))
        #从前沿面中随机选择一个点更新其，gains
        k = random.randint(0,len(IntResult)-1)
        # print(len(result))
        print("k:",k)
        print("NO.",IntResult[k])

        #随机选取设备时的fairness
        #numpy中的random模块和random中的random的范围不同，这里也包含右边界
        num = random.randint(0,19)
        UES2[num].gains += UES2[num].F_UE
        rand_fair.append(Fairness(num))
        #采用博弈策略后的fairness
        UES[IntResult[k]].gains += UES[IntResult[k]].F_UE
        # UBS += UES[IntResult[k]].F_BS
        result_fair.append(Fairness(IntResult[k]))
        result_NRD.append(IntResult[k])
        result_UBS.append(UES[IntResult[k]].F_BS)
        result_URD.append(UES[IntResult[k]].F_UE)
        # print(IntResult)
        # os.system("pause")
        cicle += 1
        # append the result to the graph
    # 绘制fairness图
    plt.xlabel('round',fontsize = 10)
    plt.xlim(0,20)
    plt.ylim(0,1)
    plt.ylabel('system fairness',fontsize = 10)
    cicle = [i for i in range(0,20)]

    game_fair = [0, 0.05, 0.1, 0.15, 0.15, 0.2, 0.2, 0.25, 0.3, 0.35, 0.4, 0.4, 0.45, 0.45,
                  0.49999725808766626, 0.5490915372696149, 0.5494345676331145, 0.5986329518439101, 0.6434627526049957, 0.6822118090289238]
    plt.plot(cicle,result_fair,marker = '*',color = 'darksalmon',label='MOO')
    plt.plot(cicle,game_fair,marker = '^',linestyle=':',color = 'slateblue',label='Game Only')
    # #绘制BS和UD的效用图
    # plt.xlabel('round ',fontsize=15)
    # plt.xlim(0,20)
    # plt.ylabel('U_BS/U_RD',fontsize=15)
    # cicle = [i for i in range(1,20)]
    # print(result_NRD)
    # print(cicle)
    # print(result_fair)
    # plt.plot(cicle, result_UBS, marker='o', label="$U_BS$")
    # plt.plot(cicle, result_URD, marker='*', label="$U_RD$")
    # for i in range(0,19):
    #     plt.annotate(result_NRD[i], (cicle[i], result_UBS[i]))
    #     plt.annotate(result_NRD[i], (cicle[i], result_URD[i]))
    labelx = range(0,21)
    plt.xticks(cicle,labelx)
    plt.grid()
    plt.legend()
    plt.show()