import math
from base import BaseMultiplier

class Booth(BaseMultiplier):
    def __init__(self):
        super().__init__()
        self.multiplier = BaseMultiplier()

    def mul(self, a, b):
        return self.booth(a, b)

    def booth(self, m, r):
        """
        Booth multiplication
        """

        x = max(math.ceil(math.log2(r)), math.ceil(math.log2(m))) + 3
        y = x

        # x = 4
        # y = 4


        print(f"m = {bin(m)}, r = {bin(r)}, x = {x}, y = {y}")

        l = x+y+1
        mask = 2**l - 1

        print(f"-m = {bin((~m + 1) & mask)}")

        A = (m << (y+1)) & mask
        S = ((~m + 1) << (y+1)) & mask
        P = (r << 1) & mask

        print(f"A (bin): {bin(A)}")
        print(f"S (bin): {bin(S)}")
        print(f"P (bin): {bin(P)}")

        for _ in range(y):
            lsb = P & 0b11
            print(f"P (bin): {bin(P)}, lsb = {bin(lsb)}")
            v = 0
            if lsb == 0b01:
                print("v = (P + A) & mask")
                print(f"v = ({bin(P)} + {bin(A)}) & {bin(mask)}")
                v = (P + A) & mask
            elif lsb == 0b10:
                print("v = (P + S) & mask")
                print(f"v = ({bin(P)} + {bin(S)}) & {bin(mask)}")
                v = (P + S) & mask
            elif lsb == 0b00:
                print("v = P")
                v = P
            else:
                print("v = P")
                v = P
            
            P = v >> 1

        print("Pen P (bin):", bin(P))
        print("Final P (bin):", bin(P >> 1))

        return P >> 1


    def __str__(self):
        return f"Booth Multiplier"

def test_booth():
    k = Booth()
    result = k.mul(123, 456)
    print(result)
    assert result == 60
    # assert k.mul(12345, 6789) == 83810205
    # print(k.multiplier)

if __name__ == "__main__":
    test_booth()