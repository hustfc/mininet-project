a = list(range(10))
for i in range(len(a)):
    print("i", i)
    del a[len(a) - 1 - i]
    print(a[i])

