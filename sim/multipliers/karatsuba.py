import math
from .base import BaseMultiplier
import random

class Karatsuba(BaseMultiplier):
    def __init__(self):
        super().__init__()
        self.multiplier = BaseMultiplier()

    def mul(self, a, b):
        return self.karatsuba(a, b)

    def karatsuba(self, a, b):
        if (a < 10) or (b < 10):
            return self.multiplier.mul(a, b) #/* fall back to traditional multiplication */
        
        #/* Calculates the size of the numbers. */
        m = min ( math.log10(a), math.log10(b))
        m2 = math.ceil (m / 2) 
        #/* m2 = ceil (m / 2) will also work */
        
        #/* Split the digit sequences in the middle. */
        k = 10**m2
        high1 = a // k
        low1 = a % k
        high2 = b // k
        low2 = b % k

        # print(f"a={a}, b={b}, high1={high1}, low1={low1}, high2={high2}, low2={low2}")
        
        #/* 3 recursive calls made to numbers approximately half the size. */
        z0 = self.karatsuba (low1, low2)
        z1 = self.karatsuba (low1 + high1, low2 + high2)
        z2 = self.karatsuba (high1, high2)
        
        return (z2 * 10 ** (m2 * 2)) + ((z1 - z2 - z0) * 10 ** m2) + z0

    def __str__(self):
        return f"Karatsuba Multiplier"

def test_karatsuba():
    k = Karatsuba()
    a = random.randint(2**127, 2**128)
    b = random.randint(2**127, 2**128)
    assert k.mul(a, b) == a * b
    print(k.multiplier)

if __name__ == "__main__":
    test_karatsuba()