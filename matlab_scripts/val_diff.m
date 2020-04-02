 function ret= val_diff(fx,point1,point2)
syms x y a z
z=fx;
a=diff(z,x);
ret=subs(a,[x, y], [point1,point2]);
 end
 