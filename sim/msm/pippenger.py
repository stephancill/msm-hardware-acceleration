import ecc
from .base import BaseMSM
import math

class PippengerMSM(BaseMSM):
    def __init__(self, scalar_size, bucket_size, a, b, p, mul_algorithm=ecc.ec_mul_projective2):
        super().__init__(a, b, p, mul_algorithm)
        self.scalar_size = scalar_size # b
        self.c = bucket_size # number of bits in the partitioned scalars

    def msm(self, points, scalars):
        """
        Multiplies a list of points by a list of scalars and adds together the results
        using the Pippenger algorithm.
        """

        assert len(points) == len(scalars)

        K = math.ceil(self.scalar_size/self.c) # number of buckets

        # print(f"K = {K}")

        l_indexes = [x-1 for x in range(0, 2**self.c)]
        B_l_k = [[(0, 1, 0) for k in range(K)] for l in range(1, 2**self.c)]

        # print(f"B_l_k.shape = {len(B_l_k)}, {len(B_l_k[0])}")

        for n in range(len(points)):
            for k in range(K):
                # Kth partition of scalars[n], l
                l = (scalars[n] >> (k*self.c)) & ((1 << self.c) - 1)
                # print(f"Binary l = {bin(l)}")
                if l == 0:
                    continue
                bx, by, bz = B_l_k[l_indexes[l]][k]
                B_l_k[l_indexes[l]][k] = ecc.ec_add_projective(bx, by, bz, points[n][0], points[n][1], 1, self.a, self.b, self.p)
        
        S_k = [(0, 1, 0) for k in range(K)]
        G_k = [(0, 1, 0) for k in range(K)]
        for l in range(2**self.c-1, 0, -1):
            # print(f"l = {l}")
            for k in range(K):
                bx, by, bz = B_l_k[l_indexes[l]][k]
                S_k[k] = ecc.ec_add_projective(S_k[k][0], S_k[k][1], S_k[k][2], bx, by, bz, self.a, self.b, self.p)
                G_k[k] = ecc.ec_add_projective(G_k[k][0], G_k[k][1], G_k[k][2], S_k[k][0], S_k[k][1], S_k[k][2], self.a, self.b, self.p)

        G = (0, 1, 0)
        for k in range(K-1, -1, -1):
            # print(f"k = {k}")
            # Caclulate 2^c * G
            G_temp = ecc.ec_mul_projective2(G[0], G[1], G[2], 1 << self.c, self.a, self.b, self.p)
            
            # Add to G_k and assign to G
            G = ecc.ec_add_projective(G_k[k][0], G_k[k][1], G_k[k][2], G_temp[0], G_temp[1], G_temp[2], self.a, self.b, self.p)

        # Convert to affine coordinates
        # print(f"G = {G}")
        G = ecc.homogeneous_to_affine(G[0], G[1], G[2], self.p)

        return G

    def __str__(self):
        return f"PippengerMSM(scalar_size={self.scalar_size}, bucket_size={self.c})"