#!/usr/bin/env python3

from multipliers.karatsuba import Karatsuba, BaseMultiplier
from multipliers.booth import Booth

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

    def reduce(self, a):
        return a % self.p

    def ff_mul(self, a, b):
        # alert if a or b is negative
        if a < 0 or b < 0:
            print("WARNING: negative value in field multiplication")
        return self.reduce(self.mul(a, b))

    def ff_add(self, a, b):
        return self.reduce(self.add(a, b))

    def __str__(self):
        return f"Field({self.p}) [mul={self.multiplications}, add={self.additions}]"