import math
from Generic import *

class Concrete(Generic):


    class ConstOps(Generic.ConstOps):
        def value(self, i):
            match i:
                case Const(i):
                    return i
                case _:
                    raise ValueError(f"{i} is not a constant")
        

    class MathOps(Generic.MathOps):
        def exp(self, v):
            if v is None:
                return None
            try:
                return math.e ** v
            except OverflowError:
                return None
        def plus(self, l, r):
            if l is None or r is None:
                return None
            return l + r
        def minus(self, l, r):
            if l is None or r is None:
                return None
            return l - r
        def mul(self, l, r):
            if l is None or r is None:
                return None
            return l * r
        def div(self, l, r):
            if l is None or r is None or r == 0:
                return None
            return l / r
        def log(self, l, b):
            if l is None or b is None or b <= 1:
                return None
            return math.log(l, b)
        def pow(self, b, x):
            if b is None or x is None:
                return None
            try:
                return b ** x
            except OverflowError:
                return None

