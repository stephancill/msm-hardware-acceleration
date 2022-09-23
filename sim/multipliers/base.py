class BaseMultiplier:
    def __init__(self):
        self.calls = 0

    def mul(self, a, b):
        self.calls += 1
        return a * b

    def __str__(self):
        return f"Base Multiplier [calls={self.calls}]"
