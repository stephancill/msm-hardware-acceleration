#!/usr/bin/env python3

import math
import ecc
import random
import os

def test_ec_add_projective():
    p = 37
    a = 0
    b = 7

    x1 = 6
    y1 = 1
    z1 = 1

    x2 = 8
    y2 = 1
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
    y1 = 1

    x2 = 8
    y2 = 1

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
    y1 = 1

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
    y1 = 1
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
    
def test_ec_double_projective():
    p = 37
    a = 0
    b = 7

    x1 = 17
    y1 = 6
    z1 = 1

    # x1 = 0
    # y1 = 1
    # z1 = 0

    x3, y3, z3 = ecc.ec_dbl_projective(x1, y1, z1, a, b, p)

    x3_affine, y3_affine = ecc.homogeneous_to_affine(x3, y3, z3, p)

    assert x3_affine == 13
    assert y3_affine == 24

def test_ec_mul_projective2():
    p = 37
    a = 0
    b = 7

    # (x, y, z, k, xr, yr)
    test_cases = [
        (6, 1, 1, 2, 18, 17),
        (6, 1, 1, 5, 24, 17),
        (6, 1, 1, 20, 32, 20),
    ]

    for case in test_cases:
        x1, y1, z1, k, xr, yr = case

        x3, y3, z3 = ecc.ec_mul_projective(x1, y1, z1, k, a, b, p)

        x3_affine, y3_affine = ecc.homogeneous_to_affine(x3, y3, z3, p)

        assert x3_affine == xr
        assert y3_affine == yr

def test_ec_mul_large():
    p = 0x01ae3a4617c510eac63b05c06ca1493b1a22d9f300f5138f1ef3622fba094800170b5d44300000008508c00000000001
    a = 0
    b = 0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001

    x1, y1 = (0x68d47cdde45290475f6de06909adb1336c1a6fa610aacf1c08eb866f704ccf99ec1760dc33c3abfeda830424010071, 0x1878642962b30a42009f8eaa7ac79091784ac903c2f2144cc6234df9af6dee01be0c4ecda79e6fea85640e16b90f33e)
    k = 0x5
    xr, yr = (0x17052d4e3eb642d32ef4989af253cc2a30ad376ce8f0b23c92b987e95cc718d02072bb78d37c09fd76f7014eecf797, 0x16c206be738bf4644faff10bb82b19f6f07779903a6ad2524809ce29f94683be32bbdd072ec0be66ae0ed0d8781f277)

    x3_affine, y3_affine = ecc.ec_mul_affine(x1, y1, k, a, b, p)

    # x3_affine, y3_affine = ecc.homogeneous_to_affine(x3, y3, z3, p)

    print(f"R = ({hex(x3_affine)}, {hex(y3_affine)})")

    assert x3_affine == xr
    assert y3_affine == yr

def generate_point_add_test_case():
    p = 0x01ae3a4617c510eac63b05c06ca1493b1a22d9f300f5138f1ef3622fba094800170b5d44300000008508c00000000001
    a = 0
    b = 0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001

    Gx = 0x008848defe740a67c8fc6225bf87ff5485951e2caa9d41bb188282c8bd37cb5cd5481512ffcd394eeab9b16eb21be9ef
    Gy = 0x01914a69c5102eff1f674f5d30afeec4bd7fb348ca3e52d96d182ad44fb82305c2fe3d3634a9591afd82de55559c8ea6

    k = random.randint(1, p - 1)
    xp, yp, zp = ecc.ec_mul_projective2(Gx, Gy, 1, k, a, b, p)
    X1, Y1 = ecc.homogeneous_to_affine(xp, yp, zp, p)

    k = random.randint(1, p - 1)
    xp, yp, zp = ecc.ec_mul_projective2(Gx, Gy, 1, k, a, b, p)
    X2, Y2 = ecc.homogeneous_to_affine(xp, yp, zp, p)

    # Add the two points
    xp, yp, zp = ecc.ec_add_projective(X1, Y1, 1, X2, Y2, 1, a, b, p)
    X3, Y3 = ecc.homogeneous_to_affine(xp, yp, zp, p)

    # Print out the test case
    print(f"P1 = ({hex(X1)}, {hex(Y1)})")
    print(f"P2 = ({hex(X2)}, {hex(Y2)})")
    print(f"P1 + P2 = ({hex(X3)}, {hex(Y3)})")

def generate_point_add_test_case_multiple():
    # Ensure test/padd directory exists
    test_path = os.path.join("test", "padd")
    if not os.path.exists(test_path):
        os.mkdir(test_path)
    else:
        # Clear test directory
        for file in os.listdir(test_path):
            os.remove(os.path.join(test_path, file))

    p = 0x01ae3a4617c510eac63b05c06ca1493b1a22d9f300f5138f1ef3622fba094800170b5d44300000008508c00000000001
    a = 0
    b = 0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001

    Gx = 0x008848defe740a67c8fc6225bf87ff5485951e2caa9d41bb188282c8bd37cb5cd5481512ffcd394eeab9b16eb21be9ef
    Gy = 0x01914a69c5102eff1f674f5d30afeec4bd7fb348ca3e52d96d182ad44fb82305c2fe3d3634a9591afd82de55559c8ea6

    length = 100

    test_cases = []

    for _ in range(length):
        k = random.randint(1, p - 1)
        xp, yp, zp = ecc.ec_mul_projective2(Gx, Gy, 1, k, a, b, p)
        X1, Y1 = ecc.homogeneous_to_affine(xp, yp, zp, p)

        k = random.randint(1, p - 1)
        xp, yp, zp = ecc.ec_mul_projective2(Gx, Gy, 1, k, a, b, p)
        X2, Y2 = ecc.homogeneous_to_affine(xp, yp, zp, p)

        # Add the two points
        xp, yp, zp = ecc.ec_add_projective(X1, Y1, 1, X2, Y2, 1, a, b, p)
        X3, Y3 = ecc.homogeneous_to_affine(xp, yp, zp, p)

        test_cases.append((X1, Y1, X2, Y2, X3, Y3))

        # Print out the test case
        # print(f"P1 = ({hex(X1)}, {hex(Y1)})")
        # print(f"P2 = ({hex(X2)}, {hex(Y2)})")
        # print(f"P1 + P2 = ({hex(X3)}, {hex(Y3)})")

    # Write test cases to files: X1 -> test_Px.txt, Y1 -> test_Py.txt, X2 -> test_Qx.txt, Y2 -> test_Qy.txt, X3 -> test_Rx.txt, Y3 -> test_Ry.txt
    file_mapping = ["test_Px.txt", "test_Py.txt", "test_Qx.txt", "test_Qy.txt", "test_Rx.txt", "test_Ry.txt"]
    files = [open(os.path.join(test_path, file), "w") for file in file_mapping]
    for test_case in test_cases:
        for n, file in zip(test_case, files):
            file.write(f"{hex(n)[2:]}\n")
    
    # Close files
    for file in files:
        file.close()
        


def generate_point_multiplication_test_case():
    p = 0x01ae3a4617c510eac63b05c06ca1493b1a22d9f300f5138f1ef3622fba094800170b5d44300000008508c00000000001
    a = 0
    b = 0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001

    Gx = 0x008848defe740a67c8fc6225bf87ff5485951e2caa9d41bb188282c8bd37cb5cd5481512ffcd394eeab9b16eb21be9ef
    Gy = 0x01914a69c5102eff1f674f5d30afeec4bd7fb348ca3e52d96d182ad44fb82305c2fe3d3634a9591afd82de55559c8ea6

    # a = random.randint(1, p - 1)
    # xp, yp, zp = ecc.ec_mul_projective2(Gx, Gy, 1, a, a, b, p)
    # X, Y = ecc.homogeneous_to_affine(xp, yp, zp, p)
    X = Gx
    Y = Gy

    # k = random.randint(2**253, 2**254-1)
    k = 0x3b90f1f8dc6b19b59ca39e6aa82bcd0d53376d493c6ac111fe6686d14192f6d6

    # Multiply the point by k
    xp, yp, zp = ecc.ec_mul_projective2(Gx, Gy, 1, k, a, b, p)
    kX, kY = ecc.homogeneous_to_affine(xp, yp, zp, p)

    # Verify that the point is on the curve
    assert (kY ** 2 - kX ** 3 - a * kX - b) % p == 0

    # Print out the test case
    print(f"P = ({hex(X)}, {hex(Y)})")
    print(f"k = {hex(k)}")
    print(f"kP = ({hex(kX)}, {hex(kY)})")

def test_point_double():
    p = 0x01ae3a4617c510eac63b05c06ca1493b1a22d9f300f5138f1ef3622fba094800170b5d44300000008508c00000000001
    a = 0
    b = 0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001

    Px = 0x116a2c0f839d9608121202ed49d41a2fb23252aa7ae75c60ad61d9cf807e53ff10ba3ff99bf43ff6c8bfbbc6528a33b
    Py = 0x10bd644104333b1a8dbdf058a5136c194b1ff7e9731969156a8c4dfd46446cd5d93a2de3130da01999d9072585ff593

    xp, yp, zp = ecc.ec_add_projective(Px, Py, 1, Px, Py, 1, a, b, p)
    X, Y = ecc.homogeneous_to_affine(xp, yp, zp, p)

    print(f"P = ({hex(X)}, {hex(Y)})")

def test_adding_edge_case():
    p = 37
    a = 0
    b = 7

    Px, Py = (24, 20)
    Qx, Qy = (24, 17)

    xp, yp, zp = ecc.ec_add_projective(Px, Py, 1, Qx, Qy, 1, a, b, p)
    X, Y = ecc.homogeneous_to_affine(xp, yp, zp, p)

    print(f"P = ({hex(X)}, {hex(Y)})")

if __name__ == "__main__":
    # test_ec_add_affine()
    # test_ec_add_projective()
    # test_ec_mul_affine()
    # test_ec_mul_projective()
    # test_ec_double_projective()
    # test_ec_mul_projective2()
    # generate_point_add_test_case()
    # generate_point_multiplication_test_case()
    # generate_point_add_test_case_multiple()
    # test_point_double()
    test_adding_edge_case()