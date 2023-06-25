
import math
import copy
from syntax import *
from Generic import *
from Concrete import *
from PyString import *
from TexString import *

upperlimit = 10
maxerror = 0.01
out_file = "app.tex"


# apps::= 4.5 -> ((upperAppVal, upper_err), (lowerAppVal, lower_err))
#
#
apps = {}


def extend(app:AppVar, maxdepth)->AppVar:
    match app:
        case Mt():
            if 1 not in apps.keys():
                apps[1] = [Pi()]
            yield Pi()
            apps[1].append(E())
            yield E()
            for el in range(1, 10):
                yield Const(el)
            if maxdepth == 1:
                return
            else:
                yield from extend(Exp(Mt()), maxdepth-1)
                yield from extend(Plus(Mt(), Mt()), maxdepth-1)
                yield from extend(Minus(Mt(), Mt()), maxdepth-1)
                yield from extend(Mul(Mt(), Mt()), maxdepth-1)
                yield from extend(Log(Mt(), Mt()), maxdepth-1)
                yield from extend(Div(Mt(), Mt()), maxdepth-1)
                powgen = extend(Pow(Mt(), Mt()), maxdepth-1)
                con = Concrete()
                for p in powgen:
                    # print(p)
                    if con.eval(p.e) != 1.0:
                        yield p
        case Exp(x):
            k = extend(x, maxdepth)
            for subres in k:
                a = Exp(subres)
                yield a
        case Plus(l, r)| Minus(l, r)| Mul(l, r)| Div(l, r):
            lg = extend(l, maxdepth)
            rg = extend(r, maxdepth)
            for le in lg:
                for re in rg:
                    if le != re:
                        app.l = le
                        app.r = re
                        yield app
        case Log(l,r):
            lg = extend(l, maxdepth)
            rg = extend(r, maxdepth)
            for le in lg:
                for re in rg:
                    if le != re:
                        app.l = le
                        app.b = re
                        yield app
        case Pow(l, r):
            lg = extend(l, maxdepth)
            rg = extend(r, maxdepth)
            for le in lg:
                for re in rg:
                    if le != re:
                        app.b = le
                        app.e = re
                        yield app

# def approx(val, depth=3):
#     gen = extend(Mt(), depth)
#     con = Concrete()
#     pys = PyString()
#     for g in gen:
#         res = con.eval(g)
#         if res is not None and abs(res) < upperlimit and abs(res - val) >= 1E-5 and abs(res-val) <= maxerror :
#             print(pys.eval(g), "=", res)

#     tex = TexString()

def approx(vals, depth=3):

    def get_closest_val(comp):
        v = min(vals, key=lambda x:abs(comp-x))
        return v, comp-v


    gen = extend(Mt(), depth)
    con = Concrete()
    pys = PyString()


    apps = {}
    for val in sorted(vals):
        apps[val] = [(Mt(), float("inf")), (Mt(), float("inf"))]

    for g in gen:
        res = con.eval(g)
        if res is not None and g.depth() > 1:
            close, diff = get_closest_val(res)
            cur = apps[close][diff > 0]
            if abs(diff) >= 1E-5 and abs(cur[1]) > abs(diff):
                apps[close][diff > 0] = (copy.deepcopy(g), diff)

    tex = TexString()

    with open(out_file, "w") as file:
        f = "\\documentclass[twocolumn]{extarticle}\n"\
            "\\usepackage{amsmath}\n"\
            "\\title{Approximations}\n"\
            "\\date{}\n"\
            "\\begin{document}\n"\
            "\\maketitle\n"\
            "{\\allowdisplaybreaks\n"\
            "\\begin{align*}\n"
        file.write(f)



        for v in vals:
            up = apps[v][0][0].simplify()
            down = apps[v][1][0].simplify()
            if up != Mt():
                file.write(f"{v} &\\geq {tex.eval(up)} &&= {round(con.eval(up), 5)}\\\\\n")
            if down != Mt():
                file.write(f"{v} &\\leq {tex.eval(down)} &&= {round(con.eval(down),5)}\\\\\n")
            # print(f"{v}:\n\t{pys.eval(up)} = {con.eval(up)}")
            # print(f"\t{pys.eval(down)} = {con.eval(down)}")
        file.write("\\end{align*}\n}\n\\end{document}")

def main():
    li =[ i/2 for i in range(1, 2*20)]
    approx(li, 5)


if __name__ == "__main__":
    main()