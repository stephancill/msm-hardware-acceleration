from msm.base import BaseMSM
from msm.pippenger import PippengerMSM
import random
import ecc
import time
import sys

def test_msm():
    p = 37
    a = 0
    b = 7

    msm = BaseMSM(a, b, p)

    points = [(6, 1), (17, 6), (5, 13)]
    scalars = [18, 80, 17] # (24, 17), (13, 24), (19, 24)

    x, y = msm.msm(points, scalars)

    print(x, y)

    assert x == 35
    assert y == 6

    points = [(6, 1), (5, 13)]
    scalars = [18, 80] # (24, 17), (16, 25)

    x, y = msm.msm(points, scalars)

    assert x == 35
    assert y == 31

def test_msm_pippenger():
    p = 37
    a = 0
    b = 7

    msm = PippengerMSM(16, 2, a, b, p)

    print(f"msm: {msm}")

    points = [(6, 1), (17, 6)]
    scalars = [18, 80] # (24, 17), (13, 24)

    x, y = msm.msm(points, scalars)

    print(x, y)

    assert x == 16
    assert y == 25

    points = [(6, 1), (5, 13)]
    scalars = [18, 80] # (24, 17), (16, 25)

    x, y = msm.msm(points, scalars)

    print(x, y)

    assert x == 35
    assert y == 31

def test_msm_large():
    p = 0x01ae3a4617c510eac63b05c06ca1493b1a22d9f300f5138f1ef3622fba094800170b5d44300000008508c00000000001
    a = 0
    b = 0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001

    Gx = 0x008848defe740a67c8fc6225bf87ff5485951e2caa9d41bb188282c8bd37cb5cd5481512ffcd394eeab9b16eb21be9ef
    Gy = 0x01914a69c5102eff1f674f5d30afeec4bd7fb348ca3e52d96d182ad44fb82305c2fe3d3634a9591afd82de55559c8ea6

    # Verify that G is on the curve
    assert (Gy * Gy - (Gx * Gx * Gx + a * Gx + b)) % p == 0

    print("Generator is on the curve!")

    msm_length = 100

    # Generate random points and scalars
    points, scalars = generate_random_msm_data(p, a, b, Gx, Gy, msm_length)

    # Write points and scalars to file
    with open("points.txt", "w") as f:
        lines = []
        for point, scalar in zip(points, scalars):
            lines.append(f"{hex(scalar)} {hex(point[0])} {hex(point[1])}\n")
        f.writelines(lines)
    
    # Compute the result using the naive algorithm
    msm = BaseMSM(a, b, p)

    # Start timer
    start = time.time()

    x, y = msm.msm(points, scalars)

    # Stop timer
    end = time.time()

    # Verify that the result is on the curve
    assert (y * y - (x * x * x + a * x + b)) % p == 0

    print("Result is on the curve!")
    print(f"Naive algorithm took {end - start} seconds")

    naive_x = x
    naive_y = y

    # Compute the result using Pippenger's algorithm
    msm = PippengerMSM(p.bit_length(), 2, a, b, p)

    # Start timer
    start = time.time()

    x, y = msm.msm(points, scalars)

    # Stop timer
    end = time.time()

    # Verify that the result is on the curve
    assert (y * y - (x * x * x + a * x + b)) % p == 0

    # Verify that the result is the same as the naive algorithm
    assert x == naive_x
    assert y == naive_y

    print("Result is on the curve!")
    print(f"Pippenger's algorithm took {end - start} seconds")

def generate_random_msm_data(p, a, b, Gx, Gy, msm_length):
    # Generate random points and scalars
    points = []
    scalars = []
    for _ in range(msm_length):
        k = random.randint(1, p - 1)
        xp, yp, zp = ecc.ec_mul_projective2(Gx, Gy, 1, k, a, b, p)
        X, Y = ecc.homogeneous_to_affine(xp, yp, zp, p)
        points.append((X, Y))

        scalars.append(random.randint(2**253, 2**254-1))

    return points, scalars

if __name__ == "__main__":
    # test_msm()
    # test_msm_pippenger()
    test_msm_large()