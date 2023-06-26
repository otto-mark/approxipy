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
                    case (_, Const(0)):
                        return ls
                    case (Const(0), _):
                        return rs
                    
                    case (Mul(a, b), c) | (c, Mul(a, b)) :
                        if a == c:
                            return Mul(a, Plus(b, Const(1)).simplify())
                        if b == c:
                            return Mul(b, Plus(a, Const(1)).simplify())


                    case (Const(a), Const(b)):
                        if ls not in [E(), Pi()] and rs not in [E(), Pi()]:
                            return Const(a+b)
                    case (li, Plus(lii, b)) | (li, Plus(b, lii)):
                        if li == lii:
                            return Plus(Mul(Const(2), li), b.simplify()).simplify()
                    case (a, Minus(c, b)):
                        if a == c:
                            return Minus(Const(2)*a, b)
                        else:
                            return Minus(Plus(a,c).simplify(), b)
                return Plus(ls, rs)
            case Minus(l, r):
                ls = l.simplify()
                rs = r.simplify()
                if ls == rs:
                    return Const(0)
                match (ls, rs):
                    case (Const(a), Const(b)):
                        if ls not in [E(), Pi()] and rs not in [E(), Pi()]:
                            return Const(a-b)
                return Minus(ls, rs)
            case Mul(l, r):
                ls = l.simplify()
                rs = r.simplify()
                if ls == rs:
                    return Pow(ls, Const(2))
                
                match (ls, rs):
                    case (Const(a), Const(b)):
                        if ls not in [E(), Pi()] and rs not in [E(), Pi()]:
                            return Const(a*b)
                return Mul(ls, rs)
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
                return Div(ls, rs)
            case Log(l, r): # r = base
                ls = l.simplify()
                rs = r.simplify()
                if ls == rs:
                    return Const(1)
                if rs == Const(1):
                    return Const(0)
                return Log(ls, rs)
            case Pow(l, r): # l = base
                ls = l.simplify()
                rs = r.simplify()
                match ls:
                    case Pow(b, e):
                        Pow(b, Mul(rs, e))
                return Pow(ls, rs)

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

    def __mul__(self, oth):
        return Const(self.i * oth.i)

    def __rmul__(self, oth):
        return self * oth
    
class E(Const):
    i = math.e
    def __init__(self, i=math.e):
        pass
    
    def __mul__(self, oth):
        match oth:
            case AppVar():
                return Mul(oth, self)
            case _:
                return Mul(Const(oth), self)
            
            
    def __rmul__(self, oth):
        return self * oth


class Pi(Const):
    i = math.pi

    def __init__(self, i=math.pi):
        pass

    def __mul__(self, oth):
        match oth:
            case AppVar():
                return Mul(oth, self)
            case _:
                return Mul(Const(oth), self)
            
    def __rmul__(self, oth):
        return self * oth



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

    


