import numpy as np
import GF

gf = GF.GF(8)
#增广矩阵
def arguemented_mat(a, b):
    return np.c_[a, b]


# 第i行和第j行交换
def swap_row(a ,i, j):
    m, n = a.shape
    if i >= m or j >= m:
        print('error: out of index ...')
    else:
        a[i] = a[i] ^ a[j]
        a[j] = a[i] ^ a[j]
        a[i] = a[i] ^ a[j]
    return a


# 变成阶梯矩阵
def trape_mat(sigma):
    m, n = sigma.shape
    #保存主元所在的列数，一般来说，每行都有一个主元，除非某行全零
    main_factor = []
    main_col = 0
    while main_col < n and len(main_factor) < m:
        # 当行数多于列数的时候，出现所有的列已经处理完，结束
        if main_col == n:
            break
        # 逐列找主元,若该列全零（从第i行往下），则没有主元
        # 当前查找小矩阵首行所在原矩阵的行号
        first_row = len(main_factor)
        while main_col < n:
            new_col = sigma[first_row:, main_col]
            not_zeros = np.where(new_col > 0)[0]
            # 若该列没有非零值，则该列非主元列
            if len(not_zeros) == 0:
                main_col += 1
                break

            # 否则通过行变换找到主元
            else:
                main_factor.append(main_col)
                index = not_zeros[0]
                # 若首个元素不是主元,需要行变换
                if index != 0:
                    sigma = swap_row(sigma, first_row, first_row + index)
                # 把该主元下面的元素全部变成0
                if first_row < m - 1:
                    for k in range(first_row+1, m):
                        times = gf.div(sigma[k, main_col], sigma[first_row, main_col])
                        temp = [gf.mul(times, i) for i in sigma[first_row]]
                        for i in range(len(sigma[k])):
                            sigma[k][i] = gf.sub(sigma[k][i], temp[i])
                        # times = float(sigma[k, main_col]) / sigma[first_row, main_col]
                        # sigma[k] = sigma[k] - times * sigma[first_row]

                # 处理完当前主元列之后继续
                main_col += 1
                break
    return sigma, main_factor


# 回代求解
def back_solve(sigma, main_factor):
    #判断是否有解
    if len(main_factor) == 0:
        print('wrong main_factor ...')
        return None
    m,n = sigma.shape
    if main_factor[-1] == n-1:
        print('no answer ...')
        return None
    # 把所有的主元元素上方的元素变成0
    for i in range(len(main_factor)-1,-1,-1):
        factor = sigma[i, main_factor[i]]
        for j in range(len(sigma[i])):
            sigma[i][j] = gf.div(sigma[i][j], factor)
        #sigma[i] = sigma[i] / float(factor)
        for j in range(i):
            times = sigma[j, main_factor[i]]
            temp = [gf.mul(times, m) for m in sigma[i]]
            for n in range(len(sigma[j])):
                sigma[j][n] = gf.sub(sigma[j][n], temp[n])
            #sigma[j] = sigma[j] - float(times)*sigma[i]
    # 先看看结果对不对
    return sigma

# 结果打印
def print_result(sigma, main_factor):
    if sigma is None:
        print('no answer ...')
        return
    m,n = sigma.shape
    result = [''] * (n-1)
    main_factor = list(main_factor)
    for i in range(n-1):
        # 如果不是主元列，则为自由变量
        if i not in main_factor:
            result[i] = 'x_' + str(i+1) + '(free var)'
        # 否则是主元变量，从对应的行，将主元变量表示成非主元变量的线性组合
        else:
            # row_of_maini表示该主元所在的行
            row_of_maini = main_factor.index(i)
            result[i] = str(sigma[row_of_maini, -1])
            for j in range(i+1, n-1):
                ratio = sigma[row_of_maini, j]
                if ratio > 0:
                    result[i] = result[i] + '-' + str(ratio) + 'x_' + str(j+1)
                if ratio < 0:
                    result[i] = result[i] + '+' + str(-ratio) + 'x_' + str(j+1)
    print('方程的通解是:',)
    for i in range(n-1):
        print('x_' + str(i+1), '=', result[i])
    return result


# 得到简化的阶梯矩阵和主元列
def solve(a, b, length):
    sigma = arguemented_mat(a, b)
    print('增广矩阵为：')
    print(sigma[0:length])
    sigma, main_factor = trape_mat(sigma)
    sigma = back_solve(sigma, main_factor)
    try:
        print('方程的简化阶梯矩阵:')
        print(sigma[0:length])
    except:
        print('no answer')
    print('方程的主元列为：')
    print(main_factor[0:length])
    res = print_result(sigma, main_factor)
    return sigma, res

from encode import encode

if __name__ == '__main__':
    success, error = 0, 0
    for t in range(50):
        packets = [32, 41, 15, 21, 43, 41, 43, 54, 12, 54, 42, 23, 42, 54, 98, 123, 23, 43, 23, 43, 64, 12, 82, 43, 45, 13] * 10
        coe, encodedP = encode(packets)
        print('随机编码矩阵:')
        print(coe)
        print('伽罗华域编码之后的包:')
        print(encodedP)
        print()
        try:
            sigma, res = solve(coe, encodedP, len(packets))
            if res and int(res[0]) == packets[0]:
                success += 1
            else:
                error += 1
        except:
            error += 1
        print('*' * 20)
        print()
    print('成功:', success)
    print('失败:', error)
    print('成功率：%.3f' % (success / (success + error)))
