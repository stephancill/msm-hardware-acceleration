import ecc

class BaseMSM:
    def __init__(self, a, b, p, mul_algorithm=ecc.ec_mul_projective2):
        self.a = a
        self.b = b
        self.p = p
        self.mul_algorithm = mul_algorithm

    def msm(self, points, scalars):
        """
        Multiplies a list of points by a list of scalars and adds together the results.
        """

        assert len(points) == len(scalars)

        rx = 0
        ry = 1
        rz = 0

        for point, scalar in zip(points, scalars):
            x, y, z = self.mul_algorithm(point[0], point[1], 1, scalar, self.a, self.b, self.p)

            # __x, __y = ecc.homogeneous_to_affine(rx, ry, rz, self.p)
            # __x2, __y2 = ecc.homogeneous_to_affine(x, y, z, self.p)
            

            rx, ry, rz = ecc.ec_add_projective(rx, ry, rz, x, y, z, self.a, self.b, self.p)
            # __x3, __y3 = ecc.homogeneous_to_affine(rx, ry, rz, self.p)
            # print(f"Mul Result = ({__x2}, {__y2}) + P = ({__x}, {__y}) = ({__x3}, {__y3})" )

        # Convert to affine coordinates
        rx, ry = ecc.homogeneous_to_affine(rx, ry, rz, self.p)

        return rx, ry

    # Affine implementation
    # def msm(self, points, scalars):
    #     assert len(points) == len(scalars)

    #     rx = 0
    #     ry = 0

    #     for point, scalar in zip(points, scalars):
    #         x, y = ecc.ec_mul_affine(point[0], point[1], scalar, self.a, self.b, self.p)

    #         # __x, __y = ecc.homogeneous_to_affine(rx, ry, rz, self.p)
    #         # __x2, __y2 = ecc.homogeneous_to_affine(x, y, z, self.p)
            

    #         rx, ry = ecc.ec_add_affine(rx, ry, x, y, self.a, self.b, self.p)
    #         # __x3, __y3 = ecc.homogeneous_to_affine(rx, ry, rz, self.p)
    #         # print(f"Mul Result = ({__x2}, {__y2}) + P = ({__x}, {__y}) = ({__x3}, {__y3})" )


        return rx, ry

    def __str__(self):
        return f"BaseMSM"


