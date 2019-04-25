primitive_polynomial_dict = {4: 0b10011,  # x**4  + x  + 1
                             8: (1 << 8) + 0b11101,  # x**8  + x**4  + x**3 + x**2 + 1
                             16: (1 << 16) + (1 << 12) + 0b1011,  # x**16 + x**12 + x**3 + x + 1
                             32: (1 << 32) + (1 << 22) + 0b111,  # x**32 + x**22 + x**2 + x + 1
                             64: (1 << 64) + 0b11011  # x**64 + x**4 + x**3 + x + 1
                             }
class GF:
    def __init__(self, w):
        self.w = w
        self.total = (1 << self.w) - 1
        self.gflog = []
        self.gfilog = [1] # g(0) = 1
        self.make_gf_dict(self.w, self.gflog, self.gfilog)

    def make_gf_dict(self, w, gflog, gfilog):
        gf_element_total_number = 1 << w
        primitive_polynomial = primitive_polynomial_dict[w]
        for i in range(1, gf_element_total_number - 1):
            temp = gfilog[i - 1] << 1  # g(i) = g(i-1) * 2
            if temp & gf_element_total_number:  # overflow
                temp ^= primitive_polynomial  # xor primitive
            gfilog.append(temp)

        assert (gfilog[gf_element_total_number - 2] << 1) ^ primitive_polynomial
        gfilog.append(None)

        for i in range(gf_element_total_number):
            gflog.append(None)

        for i in range(0, gf_element_total_number - 1):
            gflog[gfilog[i]] = i
        # print(gflog)
        # print(gfilog)

    def add(self, a, b):
        return a ^ b

    def sub(self, a, b):
        return a ^ b

    def mul(self, a, b):
        if a == 0 or b == 0:
            return 0
        return self.gfilog[(self.gflog[a] + self.gflog[b]) % self.total]

    def div(self, a, b):
        if a == 0:
            return 0
        return self.gfilog[(self.gflog[a] - self.gflog[b]) % self.total]



import random
t = 0
w = 16
gf = GF(w)
while t <= 20:
    a = random.randint(1, 2 ** w - 1)
    b = random.randint(1, 2 ** w - 1)
    c = gf.add(a, b)
    d = gf.mul(a, b)
    print('%d + %d = %d' % (a, b, c))
    print('%d - %d = %d' % (c, a, gf.sub(c, a)))
    print('%d * %d = %d' % (a, b, d))
    print('%d / %d = %d' % (d, a, gf.div(d, a)))
    print()
    t += 1

#Unit test
# gf = GF(8)
# a = gf.mul(118, 97)
# b = gf.mul(233, 109)
# print(gf.add(a, b))