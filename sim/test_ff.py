from field_arithmetic.barrett import BarrettReduction


def test_barrett_reduction():
    field = BarrettReduction(65521, 16)
    a = 64111
    b = 11195
    assert field.ff_mul(a, b) == a * b % field.s

if __name__ == "__main__":
    test_barrett_reduction()