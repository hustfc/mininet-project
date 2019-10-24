total = 500 * 2.7
a = (float)(3.7/2.7)
b = a
count = 0
for i in range(14):
    count += b
    b = b * a
print(count)
output = (500 * 2.7) / (3.7 + count)
print(output)
result = []
result.append(output)
an = output/2.7
result.append(an)
for i in range(14):
    an = an * a
    result.append(an)
print("结果:", result)
