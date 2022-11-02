from ffmath import Field

# class BarrettReducer:
    
# 	modulus: int
# 	shift: int
# 	factor: int
    
    
# 	def __init__(self, mod: int):
# 		if mod <= 0:
# 			raise ValueError("Modulus must be positive")
# 		if mod & (mod - 1) == 0:
# 			raise ValueError("Modulus must not be a power of 2")
# 		self.modulus = mod
# 		self.shift = mod.bit_length() * 2
# 		self.factor = (1 << self.shift) // mod
    
    
# 	# For x in [0, mod^2), this returns x % mod.
# 	def reduce(self, x: int) -> int:
# 		mod = self.modulus
# 		assert 0 <= x < mod**2
# 		t = (x - ((x * self.factor) >> self.shift) * mod)
# 		return t if (t < mod) else (t - mod)
class BarrettReduction(Field):
    
    def __init__(self, p: int, n: int=None):
        super().__init__(p)
        if p <= 0:
            raise ValueError("Modulus must be positive")
        if p & (p - 1) == 0:
            raise ValueError("Modulus must not be a power of 2")
        self.modulus = p
        self.shift = n * 2 if n else p.bit_length() * 2
        self.factor = (1 << self.shift) // p
        print(f"Mask: {hex((1 << self.shift))}")
        print(f"p: {hex(p)}")
        print(f"Factor: {hex(self.factor)}")

    # https://www.nayuki.io/res/barrett-reduction-algorithm/barrett-reducer.py
    def reduce(self, x):
        mod = self.modulus
        assert 0 <= x < mod**2
        
        # t = (x - ((x * self.factor) >> self.shift) * mod)
        # return t if (t < mod) else (t - mod)
        # The above algorithm in single operation steps:
        t1 = x * self.factor
        print(f"t1: {hex(t1)}")
        t2 = t1 >> self.shift
        print(f"t2: {hex(t2)}")
        t3 = t2 * mod
        print(f"t3: {hex(t3)}")
        t4 = x - t3
        print(f"t4: {hex(t4)}")
        r = t4 if (t4 < mod) else (t4 - mod)
        return r

    def ff_mul(self, a, b):
        ab = self.mul(a, b) # 0 <= x <= p^2
        return self.reduce(ab)
        








        
        