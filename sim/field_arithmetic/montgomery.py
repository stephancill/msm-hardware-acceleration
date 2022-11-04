# https://www.nayuki.io/res/montgomery-reduction-algorithm/montgomery-reducer.py

from ffmath import Field
import math

class MontgomeryReduction(Field):
    
    def __init__(self, mod):
        super().__init__(p=mod)

        # Modulus
        if mod < 3 or mod % 2 == 0:
            raise ValueError("Modulus must be an odd number at least 3")
        self.modulus = mod
        
        # Reducer
        self.reducerbits = (mod.bit_length() // 8 + 1) * 8  # This is a multiple of 8
        
        self.reducer = 1 << self.reducerbits  # This is a power of 256
        self.mask = self.reducer - 1
        assert self.reducer > mod and math.gcd(self.reducer, mod) == 1
        
        # Other computed numbers
        self.reciprocal = MontgomeryReduction.reciprocal_mod(self.reducer % mod, mod)
        self.factor = (self.reducer * self.reciprocal - 1) // mod
        self.convertedone = self.reducer % mod
    
    # Inputs and output are in Montgomery form and in the range [0, modulus)
    def multiply(self, x, y):
        mod = self.modulus
        assert 0 <= x < mod and 0 <= y < mod
        product = x * y
        temp = ((product & self.mask) * self.factor) & self.mask
        reduced = (product + temp * mod) >> self.reducerbits
        result = reduced if (reduced < mod) else (reduced - mod)
        assert 0 <= result < mod
        return result
    
    def ff_mul(self, a, b):
        return self.multiply(a, b)

    def reduce(self, ab):
        product = self.convert_in(ab) * self.convert_in(1)
        mod = self.modulus
        temp = ((product & self.mask) * self.factor) & self.mask
        reduced = (product + temp * mod) >> self.reducerbits
        result = reduced if (reduced < mod) else (reduced - mod)
        assert 0 <= result < mod
        return self.convert_out(result)
    
    # The range of x is unlimited
    def convert_in(self, x: int) -> int:
        return (x << self.reducerbits) % self.modulus
        # Compute the above using bit shifts and multiplications
    
    # The range of x is unlimited
    def convert_out(self, x: int) -> int:
        return (x * self.reciprocal) % self.modulus
    
    # Input x (base) and output (power) are in Montgomery form and in the range [0, modulus); input y (exponent) is in standard form
    def pow(self, x, y):
        assert 0 <= x < self.modulus
        if y < 0:
            raise ValueError("Negative exponent")
        z = self.convertedone
        while y != 0:
            if y & 1 != 0:
                z = self.multiply(z, x)
            x = self.multiply(x, x)
            y >>= 1
        return z
    
    
    @staticmethod
    def reciprocal_mod(x, mod):
        # Based on a simplification of the extended Euclidean algorithm
        assert mod > 0 and 0 <= x < mod
        y = x
        x = mod
        a = 0
        b = 1
        while y != 0:
            a, b = b, a - x // y * b
            x, y = y, x % y
        if x == 1:
            return a % mod
        else:
            raise ValueError("Reciprocal does not exist")