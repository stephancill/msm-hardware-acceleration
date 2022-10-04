import ecc

class BaseMSM:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def msm(self, points, scalars):
        """
        Multiplies a list of points by a list of scalars and adds together the results.
        """

        assert len(points) == len(scalars)

        rx = 0
        ry = 1
        rz = 0

        for point, scalar in zip(points, scalars):
            x, y, z = ecc.ec_mul_projective2(point[0], point[1], 1, scalar, self.a, self.b, self.p)
            rx, ry, rz = ecc.ec_add_projective(rx, ry, rz, x, y, z, self.a, self.b, self.p)

        # Convert to affine coordinates
        rx, ry = ecc.homogeneous_to_affine(rx, ry, rz, self.p)

        return rx, ry

    def __str__(self):
        return f"BaseMSM"


