import math
from base import BaseMultiplier

class Booth(BaseMultiplier):
    def __init__(self):
        super().__init__()
        self.multiplier = BaseMultiplier()

    def mul(self, a, b):
        return self.booth(a, b)

    def booth(self, a, b):
        """
        Booth multiplication
        """
        pass


    def __str__(self):
        return f"Booth Multiplier"

def test_booth():
    k = Booth()
    assert k.mul(12345, 6789) == 83810205
    print(k.multiplier)

if __name__ == "__main__":
    test_booth()