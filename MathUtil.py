
class MathUtil:
    # Try parse input to int. If fail, return input self.
    def int_tryparse(x):
        try:
            return int(x)
        except:
            return x

    # Try parse input to float. If fail, return input self.
    def float_tryparse(x):
        try:
            return float(x)
        except:
            return x
