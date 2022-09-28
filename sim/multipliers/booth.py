import math
from base import BaseMultiplier
from bitstring import BitArray
import random

class BaseAdder:
    def __init__(self):
        self.calls = 0

    def add(self, a, b):
        self.calls += 1
        return a + b

    def __str__(self):
        return f"Base Adder [calls={self.calls}]"

class Booth(BaseMultiplier):
    def __init__(self):
        super().__init__()
        self.adder = BaseAdder()

    def mul(self, a, b):
        return self.booth(a, b)

    def booth(self, m, r):
        # http://philosophyforprogrammers.blogspot.com/2011/05/booths-multiplication-algorithm-in.html
        # Initialize
        x = max(math.ceil(math.log2(r)), math.ceil(math.log2(m))) + 1
        y = x
        totalLength = x + y + 1
        mA = BitArray(int = m, length = totalLength)
        rA = BitArray(int = r, length = totalLength)
        A = mA << (y+1)
        S = BitArray(int = -m, length = totalLength)  << (y+1)
        P = BitArray(int = r, length = y)
        P.prepend(BitArray(int = 0, length = x))
        P = P << 1
        print ("Initial values")
        print ("A", A.bin)
        print ("S", S.bin)
        print ("P", P.bin)
        print ("Starting calculation")
        for _ in range(1,y+1):
            if P[-2:] == '0b01':
                P = BitArray(int = self.adder.add(P.int, A.int), length = totalLength)
                print ("P +  A:", P.bin)
            elif P[-2:] == '0b10':
                P = BitArray(int = self.adder.add(P.int, S.int), length = totalLength)
                print ("P +  S:", P.bin)
            P = BitArray(int=P.int // 2, length=totalLength) # Arithmetic shift right
            print ("P >> 1:", P.bin)
        P = BitArray(int=P.int // 2, length=totalLength) # Arithmetic shift right
        print ("P >> 1:", P.bin)
        return P.int


    def __str__(self):
        return f"Booth Multiplier"

def test_booth():
    k = Booth()
    a = random.randint(2**127, 2**128)
    b = random.randint(2**127, 2**128)
    result = k.mul(a, b)
    print(result)
    print(k.adder)
    assert result == a*b
    # assert k.mul(12345, 6789) == 83810205
    # print(k.multiplier)

if __name__ == "__main__":
    test_booth()