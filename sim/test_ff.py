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

    # a = random.randint(2**(n-1), p)
    # print(f"a: {hex(a)}")
    # b = random.randint(2**(n-1), p)
    # print(f"b: {hex(b)}")
    # r = field.ff_mul(a, b)
    # print(f"r: {hex(r)}")
    # assert r == a * b % p

def test_barrett_reduction_edge_case():
    p = 0x01ae3a4617c510eac63b05c06ca1493b1a22d9f300f5138f1ef3622fba094800170b5d44300000008508c00000000001
    n = 377
    field = BarrettReduction(p, n)
    a = 0x122ab2da99a50bd398418159f740ee6ed1b2aed659e6b75e1a1c2ff25b5c180f7ea86577c4a0e7583e6ad0b14a729e3fe1fb6afd654254af8507711c8c9d03c433b5ff35c001d5ef94ab52ee6e9f37c0a5758f3d122bed519562a6f3a8561
    r = field.reduce(a)
    print(hex(r))
    print(hex(a % p))
    
    assert r == a % p

def test_barrett_reduction_small():
    p = 37
    n = 8
    field = BarrettReduction(p, n)
    a = 567
    r = field.reduce(a)
    print(hex(r))
    print(hex(a % p))
    
    assert r == a % p

def test_montgomery_reduction():
    p = 0x01ae3a4617c510eac63b05c06ca1493b1a22d9f300f5138f1ef3622fba094800170b5d44300000008508c00000000001
    n = 377
    field = MontgomeryReduction(p)
    a = 0x1cf6b5e190d19cd0998015b5af31af5eb6b64eb9163b7745a666cbc3efd3103e56bcb2b10f509cc06844791bec4acbfb03104d3e1103e1bf02436591df74f1fd9323cedccac5de4a2693789bd485f98a3a58d9e0371fdae1675ee5c546e12
    r = field.reduce(a)
    print(hex(r))
    print(hex(a % p))
    
    assert r == a % p

    # a = random.randint(2**(n-1), p)
    # print(f"a: {hex(a)}")
    # b = random.randint(2**(n-1), p)
    # print(f"b: {hex(b)}")
    # r = field.ff_mul(a, b)
    # print(f"r: {hex(r)}")
    # assert r == a * b % p

if __name__ == "__main__":
    test_barrett_reduction_small()