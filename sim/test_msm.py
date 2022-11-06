from msm.base import BaseMSM
from msm.pippenger import PippengerMSM
import random
import ecc
import time
import sys
import os
from tqdm import tqdm

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

    points = [(6, 1), (17, 6), (5, 13)]
    scalars = [18, 80, 17] # (24, 17), (13, 24), (19, 24)

    x, y = msm.msm(points, scalars)

    print(x, y)

    assert x == 35
    assert y == 6

    points = [(6, 1), (5, 13)]
    scalars = [18, 80] # (24, 17), (16, 25)

    x, y = msm.msm(points, scalars)

    print(x, y)

    assert x == 35
    assert y == 31

def benchmark_msm_pippenger():
    # Ensure test directory exists
    if not os.path.exists("test"):
        os.mkdir("test")
    else:
        # Clear test directory
        for file in os.listdir("test"):
            remove_path = os.path.join("test", file)
            # Check if path is a file
            if os.path.isfile(remove_path):
                os.remove(remove_path)

    # ----- Large test -----
    # p = 0x01ae3a4617c510eac63b05c06ca1493b1a22d9f300f5138f1ef3622fba094800170b5d44300000008508c00000000001
    # a = 0
    # b = 0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
    # Gx = 0x008848defe740a67c8fc6225bf87ff5485951e2caa9d41bb188282c8bd37cb5cd5481512ffcd394eeab9b16eb21be9ef
    # Gy = 0x01914a69c5102eff1f674f5d30afeec4bd7fb348ca3e52d96d182ad44fb82305c2fe3d3634a9591afd82de55559c8ea6

    # ----- Medium test -----
    # p = 4294967291
    # a = 0
    # b = 1
    # Gx, Gy = (3,752522715)

    # ----- Small test -----
    p = 37
    a = 0
    b = 7
    Gx, Gy = (6, 1)

    # Verify that G is on the curve
    assert (Gy * Gy - (Gx * Gx * Gx + a * Gx + b)) % p == 0

    print("Generator is on the curve!")

    msm_length = 1000

    # # Generate random points and scalars
    points, scalars = generate_random_msm_data(p, a, b, Gx, Gy, msm_length)

    # Write points and scalars to file
    with open("test/test_Gx.txt", "w") as Gx_file:
        with open("test/test_Gy.txt", "w") as Gy_file:
            with open("test/test_x.txt", "w") as scalars_file:
                for point, scalar in zip(points, scalars):
                    Gx_file.write(f"{hex(point[0])[2:]}\n")
                    Gy_file.write(f"{hex(point[1])[2:]}\n")
                    scalars_file.write(f"{hex(scalar)[2:]}\n")
    
    # Compute the result using the naive algorithm
    msm = BaseMSM(a, b, p)

    # Start timer
    start = time.time()

    x, y = msm.msm(points, scalars)

    # Stop timer
    end = time.time()

    # Verify that the result is on the curve
    assert (y * y - (x * x * x + a * x + b)) % p == 0

    print(f"X: {x}, Y: {y}")

    print("Result is on the curve!")
    print(f"Naive algorithm took {end - start} seconds")

    naive_x = x
    naive_y = y

    gs_start = start
    gs_end = end

    # Compute the result using Pippenger's algorithm
    msm = PippengerMSM(max(p.bit_length(), 16), 2, a, b, p)

    # Start timer
    start = time.time()

    x, y = msm.msm(points, scalars)

    # Stop timer
    end = time.time()

    # Verify that the result is on the curve
    assert (y * y - (x * x * x + a * x + b)) % p == 0

    print(f"X: {x}, Y: {y}")
    # Verify that the result is the same as the naive algorithm
    assert x == naive_x
    assert y == naive_y

    with open("test/test_Rx.txt", "w") as Rx_file:
        Rx_file.write(f"{hex(x)[2:]}\n")
    
    with open("test/test_Ry.txt", "w") as Ry_file:
        Ry_file.write(f"{hex(y)[2:]}\n")

    print("Result is on the curve!")
    print(f"Pippenger's algorithm took {end - start} seconds")
    print(f"Speedup: {(gs_end - gs_start) / (end - start)}")

def benchmark_msm_multiplication():

    # ----- Large test -----
    p = 0x01ae3a4617c510eac63b05c06ca1493b1a22d9f300f5138f1ef3622fba094800170b5d44300000008508c00000000001
    a = 0
    b = 0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
    Gx = 0x008848defe740a67c8fc6225bf87ff5485951e2caa9d41bb188282c8bd37cb5cd5481512ffcd394eeab9b16eb21be9ef
    Gy = 0x01914a69c5102eff1f674f5d30afeec4bd7fb348ca3e52d96d182ad44fb82305c2fe3d3634a9591afd82de55559c8ea6

    # ----- Medium test -----
    # p = 4294967291
    # a = 0
    # b = 1
    # Gx, Gy = (3,752522715)

    # ----- Small test -----
    # p = 37
    # a = 0
    # b = 7
    # Gx, Gy = (6, 1)

    # Verify that G is on the curve
    assert (Gy * Gy - (Gx * Gx * Gx + a * Gx + b)) % p == 0

    print("Generator is on the curve!")

    msm_length = 1000

    speedups = []

    for _ in tqdm(range(1)):
        # # Generate random points and scalars
        points, scalars = generate_random_msm_data(p, a, b, Gx, Gy, msm_length)

        # Compute the result using the naive algorithm
        # msm = PippengerMSM(max(p.bit_length(), 16), 2, a, b, p, mul_algorithm=ecc.ec_mul_projective2)
        msm = BaseMSM(a, b, p, mul_algorithm=ecc.ec_mul_projective2)


        # Start timer
        start = time.time()

        x, y = msm.msm(points, scalars)

        # Stop timer
        end = time.time()

        # Verify that the result is on the curve
        assert (y * y - (x * x * x + a * x + b)) % p == 0

        print(f"X: {hex(x)}, Y: {hex(y)}")

        print("Result is on the curve!")
        print(f"Double and add algorithm took {end - start} seconds")

        naive_x = x
        naive_y = y

        gs_start = start
        gs_end = end

        # Compute the result using Pippenger's algorithm
        # msm = PippengerMSM(max(p.bit_length(), 16), 4, a, b, p, mul_algorithm=ecc.ec_mul_projective3)
        msm = BaseMSM(a, b, p, mul_algorithm=ecc.ec_mul_projective3)

        # Start timer
        start = time.time()

        x, y = msm.msm(points, scalars)

        # Stop timer
        end = time.time()

        # Verify that the result is on the curve
        assert (y * y - (x * x * x + a * x + b)) % p == 0

        print(f"X: {x}, Y: {y}")
        # Verify that the result is the same as the naive algorithm
        assert x == naive_x
        assert y == naive_y

        speedups.append((gs_end - gs_start) / (end - start))

    print("Result is on the curve!")
    print(f"Sliding window took {end - start} seconds")
    # Print average of speedups
    print(f"Average speedup: {sum(speedups) / len(speedups)}")

def generate_random_msm_data(p, a, b, Gx, Gy, msm_length):
    # Generate random points and scalars
    print("Generating random points and scalars...")
    bit_length = p.bit_length()
    points = []
    scalars = []
    for _ in tqdm(range(msm_length)):
        X = 0
        Y = 0
        k = 0
        while X == 0 or Y == 0:
            k = random.randint(2**(bit_length-1), 2**bit_length-1)
            xp, yp, zp = ecc.ec_mul_projective2(Gx, Gy, 1, k, a, b, p)
            X, Y = ecc.homogeneous_to_affine(xp, yp, zp, p)
        
        points.append((X, Y))
        scalars.append(k)
    
    print("Done generating random points and scalars")

    return points, scalars

# def test_parallel_msm():
#     # ----- Large test -----
#     p = 0x01ae3a4617c510eac63b05c06ca1493b1a22d9f300f5138f1ef3622fba094800170b5d44300000008508c00000000001
#     a = 0
#     b = 0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
#     Gx = 0x008848defe740a67c8fc6225bf87ff5485951e2caa9d41bb188282c8bd37cb5cd5481512ffcd394eeab9b16eb21be9ef
#     Gy = 0x01914a69c5102eff1f674f5d30afeec4bd7fb348ca3e52d96d182ad44fb82305c2fe3d3634a9591afd82de55559c8ea6

#     msm_length = 100

#     points, scalars = generate_random_msm_data(p, a, b, Gx, Gy, msm_length)

#     # Compute the result using the naive algorithm
#     # msm = PippengerMSM(max(p.bit_length(), 16), 2, a, b, p, mul_algorithm=ecc.ec_mul_projective2)
#     msm = BaseMSM(a, b, p)
#     x_ref, y_ref = msm.msm(points, scalars)

#     # Break up the points and scalars into chunks
#     chunk_size = 10
#     points_chunks = [points[i:i+chunk_size] for i in range(0, len(points), chunk_size)]
#     scalars_chunks = [scalars[i:i+chunk_size] for i in range(0, len(scalars), chunk_size)]

#     # Compute partial results using msm
#     partial_results = []
#     for points_chunk, scalars_chunk in zip(points_chunks, scalars_chunks):
#         partial_results.append(msm.msm(points_chunk, scalars_chunk))
    
#     # Add the partial results together
#     x, y = partial_results[0]
#     for i in range(1, len(partial_results)):
#         x, y = ecc.ec_add_affine(x, y, partial_results[i][0], partial_results[i][1], a, b, p)
    
#     # Verify that the result is the same as the naive algorithm
#     assert x == x_ref
#     assert y == y_ref




if __name__ == "__main__":
    # test_msm()
    # test_msm_pippenger()
    benchmark_msm_pippenger()
    # benchmark_msm_multiplication()
    # test_parallel_msm()