#!/usr/bin/env python3

from multipliers.karatsuba import Karatsuba, BaseMultiplier

class Field:
    def __init__(self, p):
        self.p = p
        self.additions = 0
        self.multiplications = 0
        self.multiplier = BaseMultiplier()

    def add(self, a, b):
        self.additions += 1
        return a + b

    def mul(self, a, b):
        self.multiplications += 1
        return self.multiplier.mul(a, b)

    def mod(self, a):
        v = a
        while v > self.p:
            v = self.add(v, -self.p)
        return v

    def ff_mul(self, a, b):
        return self.mod(self.mul(a, b))

    def ff_add(self, a, b):
        return self.mod(self.add(a, b))

    def __str__(self):
        return f"Field({self.p}) [mul={self.multiplications}, add={self.additions}]"