import math
from abc import ABC
from dataclasses import dataclass


class AppVar(ABC):

    def simplify(self):
        match self:
            case Const(x):
                return self
            case Exp(x):
                inner = x.simplify()
                match inner:
                    case Log(l, E()):
                        return l
                    case _:
                        return Exp(inner)
            case Plus(l, r):
                ls = l.simplify()
                rs = r.simplify()
                if ls == rs:
                    return Mul(Const(2), ls)
                match (ls, rs):
                    case (Const(a), Const(b)):
                        return Const(a+b)
                    case (Const(a), Plus(Const(c), b)) | (Const(a), Plus(b, Const(c))):
                        if a == c:
                            return Plus(Mul(Const(2), ls), b.simplify())
                        else:
                            return Plus(Const(a+c), b)
                    case (Const(a), Minus(Const(c), b)):
                        if a == c:
                            return b.simplify()
                        else:
                            return Minus(Const(a+c), b)
                return self
            case Minus(l, r):
                ls = l.simplify()
                rs = r.simplify()
                if ls == rs:
                    return Const(0)
                match (ls, rs):
                    case (Const(a), Const(b)):
                        return Const(a-b)
                return self
            case Mul(l, r):
                ls = l.simplify()
                rs = r.simplify()
                if ls == rs:
                    return Pow(ls, Const(2))
                
                match (ls, rs):
                    case (Const(a), Const(b)):
                        return Const(a*b)
                return self
            case Div(l, r):
                ls = l.simplify()
                rs = r.simplify()
                if ls == rs:
                    return Const(1)
                if any([x in (E(), Pi()) for x in [ls, rs]]):
                       return self
                match (ls, rs):
                    case (Const(a), Const(b)):
                        return Const(a/b)
                    case (Mul(a, b), c):
                        if a == c:
                            return b 
                        if b == c:
                            return a
                    case (c, Mul(a, b)):
                        if a == c:
                            return Div(Const(1), b)
                        if b == c:
                            return Div(Const(1), a)
                return self
            case Log(l, r): # r = base
                ls = l.simplify()
                rs = r.simplify()
                if ls == rs:
                    return Const(1)
                if rs == Const(1):
                    return Const(0)
                return self
            case Pow(l, r): # l = base
                ls = l.simplify()
                rs = r.simplify()
                match ls:
                    case Pow(b, e):
                        Pow(b, Mul(rs, e))
                return self

    def depth(self):
        match self:
            case Const(x):
                return 1
            case Exp(x):
                return 1 + x.depth()
            case Plus(l, r)|Minus(l, r)|Mul(l, r)|Div(l, r)|Log(l,r)|Pow(l,r):
                return 1 + max(l.depth(), r.depth())
            case Mt():
                return 0
    
    def length(self):
        match self:
            case Const(x):
                return 1
            case Exp(x):
                return 1 + x.length()
            case Plus(l, r)|Minus(l, r)|Mul(l, r)|Div(l, r)|Log(l,r)|Pow(l,r):
                return 1 + l.length() + r.length()
            case Mt():
                return 0
            

@dataclass
class Mt(AppVar):
    pass

@dataclass
class Const(AppVar):
    i : float

class E(Const):
    i = math.e
    def __init__(self, i=math.e):
        pass

class Pi(Const):
    i = math.pi

    def __init__(self, i=math.pi):
        pass



@dataclass
class Exp(AppVar):
    a: AppVar

@dataclass
class Plus(AppVar):
    l: AppVar
    r: AppVar

@dataclass
class Minus(AppVar):
    l: AppVar
    r: AppVar

@dataclass
class Mul(AppVar):
    l: AppVar
    r: AppVar

@dataclass
class Div(AppVar):
    l: AppVar
    r: AppVar

    
@dataclass
class Log(AppVar):
    l: AppVar
    b: AppVar
    
@dataclass
class Pow(AppVar):
    b: AppVar
    e: AppVar

    


