import math

class MathUtil:
    # Compare two values check they are similar.
    def Approximately(a:float,b:float,size=float(0.000001)):
        return math.fabs(a - b) <= size
