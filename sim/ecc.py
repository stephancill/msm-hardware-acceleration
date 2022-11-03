#!/usr/bin/env python3

from ffmath import Field
# from field_arithmetic.barrett import BarrettReduction as Field
# from field_arithmetic.montgomery import MontgomeryReduction as Field
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
    Source: https://eprint.iacr.org/2015/1060 (alg 1)
    """

    b3 = 3 * b

    field = Field(p)

    t0 = field.ff_mul(x1, x2) #1
    t1 = field.ff_mul(y1, y2) #2
    t2 = field.ff_mul(z1, z2) #3
    t3 = field.ff_add(x1, y1) #4
    t4 = field.ff_add(x2, y2) #5
    t3 = field.ff_mul(t3, t4) #6
    t4 = field.ff_add(t0, t1) #7
    t3 = field.ff_add(t3, -t4) #8
    t4 = field.ff_add(x1, z1) #9
    t5 = field.ff_add(x2, z2) #10
    #11
    t4 = field.ff_mul(t4, t5)
    #12
    t5 = field.ff_add(t0, t2)
    #13
    t4 = field.ff_add(t4, -t5)
    #14
    t5 = field.ff_add(y1, z1)
    #15
    x3 = field.ff_add(y2, z2)
    #16
    t5 = field.ff_mul(t5, x3)
    #17
    x3 = field.ff_add(t1, t2)
    #18
    t5 = field.ff_add(t5, -x3)
    #19
    z3 = field.ff_mul(a, t4)
    #20
    x3 = field.ff_mul(b3, t2)
    #21
    z3 = field.ff_add(x3, z3)
    #22
    x3 = field.ff_add(t1, -z3)
    #23
    z3 = field.ff_add(t1, z3)
    #24
    y3 = field.ff_mul(x3, z3)
    #25
    t1 = field.ff_add(t0, t0)
    #26
    t1 = field.ff_add(t1, t0)
    #27
    t2 = field.ff_mul(a, t2)
    #28
    t4 = field.ff_mul(b3, t4)
    #29
    t1 = field.ff_add(t1, t2)
    #30
    t2 = field.ff_add(t0, -t2)
    #31
    t2 = field.ff_mul(a, t2)
    #32
    t4 = field.ff_add(t4, t2)
    #33
    t0 = field.ff_mul(t1, t4)
    #34
    y3 = field.ff_add(y3, t0)
    #35
    t0 = field.ff_mul(t5, t4)
    #36
    x3 = field.ff_mul(t3, x3)
    #37
    x3 = field.ff_add(x3, -t0)
    #38
    t0 = field.ff_mul(t3, t1)
    #39
    z3 = field.ff_mul(t5, z3)
    #40
    z3 = field.ff_add(z3, t0)

    return x3, y3, z3



def ec_dbl_projective(x, y, z, a, b, p):
    """
    Double a point on an elliptic curve in homogeneous projective coordinates. 
    Source: https://eprint.iacr.org/2015/1060 (alg 3)
    """
    b3 = 3 * b
    field = Field(p)
    
    t0 = field.ff_mul(x, x)         # 1
    t1 = field.ff_mul(y, y)         # 2
    t2 = field.ff_mul(z, z)         # 3
    t3 = field.ff_mul(x, y)         # 4
    t3 = field.ff_add(t3, t3)       # 5
    z3 = field.ff_mul(x, z)         # 6
    z3 = field.ff_add(z3, z3)       # 7
    x3 = field.ff_mul(a, z3)        # 8
    y3 = field.ff_mul(b3, t2)       # 9
    y3 = field.ff_add(x3, y3)       # 10
    x3 = field.ff_add(t1, -y3)      # 11
    y3 = field.ff_add(t1, y3)       # 12
    y3 = field.ff_mul(x3, y3)       # 13
    x3 = field.ff_mul(t3, x3)       # 14
    z3 = field.ff_mul(b3, z3)       # 15
    t2 = field.ff_mul(a, t2)        # 16
    t3 = field.ff_add(t0, -t2)      # 17
    t3 = field.ff_mul(a, t3)        # 18
    t3 = field.ff_add(t3, z3)       # 19
    z3 = field.ff_add(t0, t0)       # 20
    t0 = field.ff_add(z3, t0)       # 21
    t0 = field.ff_add(t0, t2)       # 22
    t0 = field.ff_mul(t0, t3)       # 23
    y3 = field.ff_add(y3, t0)       # 24
    t2 = field.ff_mul(y, z)         # 25
    t2 = field.ff_add(t2, t2)       # 26
    t0 = field.ff_mul(t2, t3)       # 27
    x3 = field.ff_add(x3, -t0)      # 28
    z3 = field.ff_mul(t2, t1)       # 29
    z3 = field.ff_add(z3, z3)       # 30
    z3 = field.ff_add(z3, z3)       # 31

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

def ec_mul_projective2(x1, y1, z1, k, a, b, p):
    """
    Multiply a point on an elliptic curve in homogeneous projective coordinates using double-and-add method.
    """

    xt = x1
    yt = y1
    zt = z1

    x = 0
    y = 1
    z = 0
    
    for i in range(k.bit_length()):
        if k & (1 << i):
            x, y, z = ec_add_projective(x, y, z, xt, yt, zt, a, b, p)
            # xa, ya = homogeneous_to_affine(x, y, z, p)
            # print(f"i={i} ({hex(xa), hex(ya)})")
        xt, yt, zt = ec_dbl_projective(xt, yt, zt, a, b, p)
        # xa, ya = homogeneous_to_affine(xt, yt, zt, p)
        # print(f"J: i={i} ({hex(xa), hex(ya)})")
        
        # xta, yta = homogeneous_to_affine(xt, yt, zt, p)
        # print(f"i={i}, k={k}, x={xa}, y={ya} xt={xta}, yt={yta}")
    
    return x, y, z

def homogeneous_to_affine(x, y, z, p):
    """
    Convert a point on an elliptic curve in homogeneous coordinates to affine coordinates.
    """
    if x == 0 and y == 1 and z == 0:
        return 0, 0

    z_inv = libnum.invmod(z, p)
    x = (x * z_inv) % p
    y = (y * z_inv) % p
    
    return x, y


    
    

