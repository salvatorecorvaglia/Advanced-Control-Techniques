function ret= deriv(fx,point1)
syms x y a z
z=fx;
a=diff(z,x);
ret=subs(a,x, point1);
 end
 