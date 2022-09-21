#!/usr/bin/env python3

from ffmath import Field
import libnum

def ec_add_affine(x1, y1, x2, y2, a, b, p):
    """
    Add two points on an elliptic curve in affine coordinates.
    """
    if x1 == x2 and y1 == y2:
        # Double
        s = (3*x1**2 + a) * libnum.invmod(2*y1, p)
    else:
        s = (y2 - y1) * libnum.invmod(x2 - x1, p)
    x3 = (s**2 - x1 - x2) % p
    y3 = (s*(x1 - x3) - y1) % p
    return x3, y3
    
def ec_mul_affine(x1, y1, k, a, b, p):
    """
    Multiply a point on an elliptic curve in affine coordinates.
    """
    x = x1
    y = y1
    for _ in range(k-1):
        x, y = ec_add_affine(x, y, x1, y1, a, b, p)
    return x, y

def ec_add_projective(x1, y1, z1, x2, y2, z2, a, b, p):
    """
    Add two points on an elliptic curve in homogeneous coordinates.
    """

    # Source: https://eprint.iacr.org/2015/1060.pdf

    b3 = 3 * b

    field = Field(p)

    t0 = field.ff_mul(x1, x2)
    t1 = field.ff_mul(y1, y2)
    t3 = field.ff_add(x2, y2)
    t4 = field.ff_add(x1, y1)
    t3 = field.ff_mul(t3, t4)
    t4 = field.ff_add(t0, t1)
    t3 = field.ff_add(t3, -t4)
    t4 = field.ff_mul(x2, z1)
    t4 = field.ff_add(t4, x1)
    t5 = field.ff_mul(y2, z1)
    t5 = field.ff_add(t5, y1)
    z3 = field.ff_mul(a, t4)
    x3 = field.ff_mul(b3, z1)
    z3 = field.ff_add(x3, z3)
    x3 = field.ff_add(t1, -z3)
    z3 = field.ff_add(t1, z3)
    y3 = field.ff_mul(x3, z3)
    t1 = field.ff_add(t0, t0)
    t1 = field.ff_add(t1, t0)
    t2 = field.ff_mul(a, z1)
    t4 = field.ff_mul(b3, t4)
    t1 = field.ff_add(t1, t2)
    t2 = field.ff_add(t0, -t2)
    t2 = field.ff_mul(a, t2)
    t4 = field.ff_add(t4, t2)
    t0 = field.ff_mul(t1, t4)
    y3 = field.ff_add(y3, t0)
    t0 = field.ff_mul(t5, t4)
    x3 = field.ff_mul(t3, x3)
    x3 = field.ff_add(x3, -t0)
    t0 = field.ff_mul(t3, t1)
    z3 = field.ff_mul(t5, z3)
    z3 = field.ff_add(z3, t0)

    print(field)

    return x3, y3, z3

def ec_mul_projective(x1, y1, z1, k, a, b, p):
    """
    Multiply a point on an elliptic curve in homogeneous projective coordinates.
    """

    x = x1
    y = y1
    z = z1
    for _ in range(k-1):
        x, y, z = ec_add_projective(x, y, z, x1, y1, z1, a, b, p)
    
    return x, y, z

def homogeneous_to_affine(x, y, z, p):
    """
    Convert a point on an elliptic curve in homogeneous coordinates to affine coordinates.
    """
    z_inv = libnum.invmod(z, p)
    x = (x * z_inv) % p
    y = (y * z_inv) % p
    
    return x, y


    
    

