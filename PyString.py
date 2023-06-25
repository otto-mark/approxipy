from Generic import *

class PyString(Generic):

    class ConstOps(Generic.ConstOps):
        def value(self, i):
            match i:
                case E(i):
                    return "math.e"
                case Pi(i):
                    return "math.pi"
                case Const(i):
                    return str(i)
                case _:
                    raise ValueError(f"{i} is not a constant")

    class MathOps(Generic.MathOps):
            def exp(self, v):
                return f"math.e ** {v}"
            def plus(self, l, r):
                return f"({l} + {r})"
            def minus(self, l, r):
                return f"({l} - {r})"
            def mul(self, l, r):
                return f"({l} * {r})"
            def div(self, l, r):
                return f"({l} / {r})"
            def log(self, l, b):
                return f"math.log({l}, {b})"
            def pow(self, b, x):
                return f"{b} ** {x}"