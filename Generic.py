from abc import ABC, abstractmethod
from syntax import *


class Value(ABC):
    pass

class Generic(ABC):

    class ConstOps(ABC):
        @abstractmethod
        def value(self, i):
            pass

    class MathOps(ABC):
        @abstractmethod
        def exp(self, v):
            pass
        @abstractmethod
        def plus(self, l, r):
            pass
        @abstractmethod
        def minus(self, l, r):
            pass
        @abstractmethod
        def mul(self, l, r):
            pass
        @abstractmethod
        def div(self, l, r):
            pass

        

    def eval(self, s: AppVar) -> Value:
        match s:
            case Const(i):
                return self.ConstOps().value(s)
            case Exp(x):
                return self.MathOps().exp(self.eval(x))
            case Plus(l, r):
                return self.MathOps().plus(self.eval(l), self.eval(r))
            case Minus(l, r):
                return self.MathOps().minus(self.eval(l), self.eval(r))
            case Mul(l, r):
                return self.MathOps().mul(self.eval(l), self.eval(r))
            case Div(l, r):
                return self.MathOps().div(self.eval(l), self.eval(r))
            case Log(l, b):
                return self.MathOps().log(self.eval(l), self.eval(b))
            case Pow(b, x):
                return self.MathOps().pow(self.eval(b), self.eval(x))
