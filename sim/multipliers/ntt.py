from base import BaseMultiplier


class NTT(BaseMultiplier):
    def __init__(self):
        super().__init__()

    def mul(self, a, b):
        return self.ntt(a, b)

    def ntt(self, a, b):
        """
        Number theoretic transform integer multiplication
        """
        pass


        

    def __str__(self):
        return f"NTT Multiplier"