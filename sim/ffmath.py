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

    def ff_mul(self, a, b):
        return self.mul(a, b) % self.p

    def ff_add(self, a, b):
        return self.add(a, b) % self.p

    def __str__(self):
        return f"Field({self.p}) [mul={self.multiplications}, add={self.additions}]"