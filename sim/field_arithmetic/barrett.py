from ffmath import Field


class BarrettReduction(Field):
    def __init__(self, p, n):
        super().__init__(p)
        self.s = p
        self.n = n # bit length of inputs
        self.m = int(2**(2*self.n) / self.s)

    def ff_mul(self, a, b):
        # Author: Yuval Domb, Ingoyama
        ab = self.mul(a, b)

        # a*b full mult
        ab_msb = ab >> self.n
        ab_lsb = ab & ((1 << self.n + 2) - 1)

        # ab*m msb mult (attempt)
        abm = self.mul(ab_msb, self.m)
        l1 = abm >> self.n

        # l1*s lsb mult
        l1s = self.mul(l1, self.s)
        l1s_lsb = l1s & ((1 << (self.n + 2)) - 1)

        # ab-l1s fixed width adder
        r_plus = self.add (ab_lsb, ~l1s_lsb + 1) & ((1 << (self.n + 2)) - 1)

        while r_plus >= self.s:
            r_plus = r_plus - self.s
        
        return r_plus








        
        