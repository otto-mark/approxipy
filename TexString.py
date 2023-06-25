from Generic import *

class TexString(Generic):

    class ConstOps(Generic.ConstOps):
        def value(self, i):
            match i:
                case E(i):
                    return "e"
                case Pi(i):
                    return "\\pi"
                case Const(i):
                    return str(i)
                case _:
                    raise ValueError(f"{i} is not a constant")

    class MathOps(Generic.MathOps):
            def exp(self, v):
                return f"\\exp\\left( {v} \\right)"
            def plus(self, l, r):
                return f"{l} + {r}"
            def minus(self, l, r):
                return f"{l} - {r}"
            def mul(self, l, r):
                return f"{l} \cdot {r}"
            def div(self, l, r):
                return f"\\frac{{ {l} }} {{ {r} }}"
            def log(self, l, b):
                if b == "e":
                    return f"\\ln\\left( {l} \\right)"
                return f"\\log_{{ {b} }} \\left( {l} \\right)"
            def pow(self, b, x):
                return f"{b}^{{{x}}}"