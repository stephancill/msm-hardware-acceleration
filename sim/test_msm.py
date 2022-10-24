from msm.base import BaseMSM
from msm.pippenger import PippengerMSM
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

if __name__ == "__main__":
    test_msm()
    # test_msm_pippenger()