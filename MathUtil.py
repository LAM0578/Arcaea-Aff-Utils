
import math


class MathUtil:
    # Try parse input to int. If fail, return input self.
    def IntTryParse(x):
        try:
            return int(x)
        except:
            return x

    # Try parse input to float. If fail, return input self.
    def FloatTryParse(x):
        try:
            return float(x)
        except:
            return x

    # Compare two values check they are similar.
    def Approximately(a:float,b:float,size=float(0.000001)):
        return math.fabs(a - b) <= size
