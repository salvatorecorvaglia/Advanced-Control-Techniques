from sympy import *


def partial_sum(vecx, vecy):
    x = Symbol('x')
    y = Symbol('y')
    vecx = [float(i) for i in vecx]
    vecy = [float(i) for i in vecy]
    partial = 0


    for i in range(0, len(vecx)):

       # partial = partial + func.subs([(x, vecx[i]), (y, vecy[i])])
       partial = partial + expand((vecx[i] * x + y - vecy[i]) ** 2)



    return partial
