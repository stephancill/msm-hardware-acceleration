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
    def __init__(self, p, n=None):
        super().__init__(p)
        if n is None:
            self.n = p.bit_length() * 2
        else:
            self.n = n
        self.p = p
        # self.n = n * 2 # 2x bit length of p
        self.r = (1 << self.n) // p # Precomputed factor floor(4^k / p)

    def ff_mul(self, a, b):
        ab = self.mul(a, b) # 0 <= x <= p^2
        
        # Reduction
        abr = self.mul(ab, self.r) # m1
        abr_div4_k = abr >> self.n 
        abr_div4_k_p = self.mul(abr_div4_k, self.p) # m2
        t = self.add(ab, -abr_div4_k_p)
        return t if (t < self.p) else (t - self.p)








        
        