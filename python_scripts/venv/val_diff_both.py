from sympy import *
import numpy
class val_diff_both:
  def val_diff_both(fxy, point1, point2):
    a = Symbol('a')
    b = Symbol('b')

    x = Symbol('x')
    y = Symbol('y')
    z = fxy
    vec = []
    a = diff(z, x)
    b = diff(z, y)
    vec[0] = a.subs([(x, point1), (y, point2)])
    vec[1] = b.subs([(x, point1), (y, point2)])

    return vec