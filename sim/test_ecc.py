#!/usr/bin/env python3

import math
import ecc

def test_ec_add_projective():
    p = 37
    a = 0
    b = 7

    x1 = 6
    y1 = int(math.sqrt((x1**3 + a*x1 + b) % p))
    z1 = 1

    x2 = 8
    y2 = int(math.sqrt((x1**3 + a*x1 + b) % p))
    z2 = 1
    
    # Reference
    x3, y3, z3 = ecc.ec_add_projective(x1, y1, z1, x2, y2, z2, a, b, p)

    x3_affine, y3_affine = ecc.homogeneous_to_affine(x3, y3, z3, p)

    assert x3_affine == 23
    assert y3_affine == 36

def test_ec_add_affine():
    p = 37
    a = 0
    b = 7

    # Test addition of two points on the curve
    x1 = 6
    y1 = int(math.sqrt((x1**3 + a*x1 + b) % p))

    x2 = 8
    y2 = int(math.sqrt((x2**3 + a*x2 + b) % p))

    x3, y3 = ecc.ec_add_affine(x1, y1, x2, y2, a, b, p)

    assert x3 == 23
    assert y3 == 36

    # Test doubling of a point on the curve
    x3, y3 = ecc.ec_add_affine(x1, y1, x1, y1, a, b, p)

    assert x3 == 18
    assert y3 == 17

def test_ec_mul_affine():
    p = 37
    a = 0
    b = 7

    x1 = 6
    y1 = int(math.sqrt((x1**3 + a*x1 + b) % p))

    k = 2

    x3, y3 = ecc.ec_mul_affine(x1, y1, k, a, b, p)

    assert x3 == 18
    assert y3 == 17

    k = 5

    x3, y3 = ecc.ec_mul_affine(x1, y1, k, a, b, p)

    assert x3 == 24
    assert y3 == 17

def test_ec_mul_projective():
    p = 37
    a = 0
    b = 7

    x1 = 6
    y1 = int(math.sqrt((x1**3 + a*x1 + b) % p))
    z1 = 1

    k = 2

    x3, y3, z3 = ecc.ec_mul_projective(x1, y1, z1, k, a, b, p)

    x3_affine, y3_affine = ecc.homogeneous_to_affine(x3, y3, z3, p)

    assert x3_affine == 18
    assert y3_affine == 17

    k = 5

    x3, y3, z3 = ecc.ec_mul_projective(x1, y1, z1, k, a, b, p)

    x3_affine, y3_affine = ecc.homogeneous_to_affine(x3, y3, z3, p)

    assert x3_affine == 24
    assert y3_affine == 17
    
if __name__ == "__main__":
    test_ec_add_affine()
    test_ec_add_projective()
    test_ec_mul_affine()
    test_ec_mul_projective()