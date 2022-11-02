from field_arithmetic.barrett import BarrettReduction
from field_arithmetic.montgomery import MontgomeryReduction
import random

def test_barrett_reduction():
    p = 0x01ae3a4617c510eac63b05c06ca1493b1a22d9f300f5138f1ef3622fba094800170b5d44300000008508c00000000001
    n = 377
    field = BarrettReduction(p, n)
    a = 0x1cf6b5e190d19cd0998015b5af31af5eb6b64eb9163b7745a666cbc3efd3103e56bcb2b10f509cc06844791bec4acbfb03104d3e1103e1bf02436591df74f1fd9323cedccac5de4a2693789bd485f98a3a58d9e0371fdae1675ee5c546e12
    r = field.reduce(a)
    print(hex(r))
    print(hex(a % p))
    
    assert r == a % p

    a = random.randint(2**(n-1), p)
    print(f"a: {hex(a)}")
    b = random.randint(2**(n-1), p)
    print(f"b: {hex(b)}")
    r = field.ff_mul(a, b)
    print(f"r: {hex(r)}")
    assert r == a * b % p

def test_montgomery_reduction():
    field = MontgomeryReduction(65521)
    a = 64111
    b = 11195
    assert field.ff_mul(a, b) == a * b % field.s

if __name__ == "__main__":
    test_barrett_reduction()