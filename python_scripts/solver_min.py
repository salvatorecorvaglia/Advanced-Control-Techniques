from asyncore import dispatcher

from sympy import *
import math
import numpy
import matplotlib.pyplot as plt
from dataNodes import dataNodes
from ResPoints import ResPoints
from degree_MTX import degree_MTX
from ret_data import ret_data
import pylab
def val_diff2(fxy, point1, point2):
    a = Symbol('a')
    b = Symbol('b')

    x = Symbol('x')
    y = Symbol('y')
    z = fxy
    vec=[]
    a = diff(z, x)
    b = diff(z, y)
    vec.append(a.subs([(x, point1), (y, point2)]))
    vec.append(b.subs([(x, point1), (y, point2)]))

    return vec

def val_diff(fx, point1, point2, control):
    a = Symbol('a')
    x = Symbol('x')
    y = Symbol('y')
    a1 = 0
    if control == 0:
        a = diff(fx, x)
        a1 = a.subs([(x, point1), (y, point2)])
    else:
        if control == 1:
            a = diff(fx, y)
            a1 = a.subs([(x, point1), (y, point2)])
    return a1







if __name__ == '__main__':

     x = Symbol('x')
     y = Symbol('y')
     grad = []




     func=[]
     adj_values = [0, 1]
     NN = 1

     #func = dataNodes(NN)

     while True:
         Adj = numpy.random.choice(adj_values, [NN, NN], p=[0.8, 0.2])
         v = ones(1, NN - 1)
         Adj = (Adj | numpy.transpose(Adj))
         # FN=float(NN)
         I_NN = numpy.eye(NN, dtype=numpy.int)
         Adj = (Adj | (I_NN))
         testAdj = numpy.linalg.matrix_power((I_NN + Adj), NN)
         print("test adj is \n" + str(testAdj))
         if (numpy.all(numpy.all(testAdj))):
             print('\nthe graph is connected.\n')
             print("Adj is \n" + str(Adj))
             break
         else:

             print('\nthe graph is disconnected.\n')
     while True:
         # calcola la degree matrix
         fun_in=[]
         function=[]
         selector= input(' Would you like to compute last square line? type y/n \n')

         if selector =='y' or selector == 'yes':
             component= 2
             function= dataNodes(NN)
             if NN > 2:
                 step = 0.0005 + (0.0002 * (NN - 2))
             else:
                 step = 0.0005
             array = []
             array.append(symbols('x0:%d' % component))
             break


         component = int(input('insert number of components: \n '))
         array = []
         array.append(symbols('x0:%d' % component))
         #symbols_dict = dict(('x%d' % k, symbols('x%d' % k)) for k in range(component))
         #print('simone vale=', x)
         #locals().update(symbols_dict)
         test=int(input('how many functions would you like to insert?\n'))

         for i in range (0,test):

              fun_in.append(expand(input('insert function '+ str(i+1)+':\n')))



         if test==1:
           for i in range(0,NN):
              function.append(fun_in[0])
         else:
           function = fun_in
         step = 0.01
         break


     print(function)

     WW = degree_MTX(Adj,NN,1)

     print("Double stoc \n" + str(WW))

     # Adj, WW risultano calcolate e verificate

     MAX_ITERS =1000
     # if NN > 3:
     #     step = 0.0006 + (0.0002 * (NN - 3))
     # else:
     #     step = 0.0006

     XX = numpy.empty([NN, MAX_ITERS,component])
     for i in range(0,component):
         X0 = 10 * numpy.random.rand(NN)
         XX[:,0,i] = X0
     # set initial condition

     flag = 1
     tt = 0
     U_i2 = zeros(component)
     U_i = zeros(component)
     s = numpy.empty([NN, MAX_ITERS, component])
     # CONVERGENCE
     for tt in range(0, MAX_ITERS - 1):
         if (numpy.mod(tt, 10) == 0):
             print('\nIteration  ' + str(tt) + '/' + str(MAX_ITERS) + '\n')



         for ii in range(0, NN):

             N_ii = numpy.where((Adj[ii, :] == 1))
             #print('ss',N_ii)
             N_ii = numpy.asarray(N_ii)
             N_ii=N_ii.tolist()
             N_ii=N_ii[0]

             # print('neighb '+ st# r(N_ii))
             U_i2= zeros(component)
             U_i = zeros(component)

             #print('neighb \n', N_ii )

             for jj in N_ii:
                 if (flag == 1):
                     array = numpy.asarray(array)
                     array = array.tolist()
                     array = array[0]
                     for kk in range(0, NN ):
                         for c in range(0,component):


                             grad=(diff(function[kk],array[c]))


                             s[kk, 0, c] = grad.subs([(array[n], XX[kk, 0, n]) for n in range(component)])



                         print('status iniziale', XX[kk, 0, :])
                         #print('grad is ', grad)


                         #print('der', s[kk, 0, :])
                     flag = 0



                 for c in range (0,component):

                     U_i[c] = U_i[c] + WW[ii, jj] * XX[jj, tt, c]

                     U_i2[c] = U_i2[c] + WW[ii, jj] * s[jj, tt, c]




             for c in range(0,component):
                 XX[ii, tt+1, c]= U_i[c] - step * (s[ii, tt, c])

             for c in range (0,component):
                 grad = (diff(function[ii], array[c]))

                 s[ii, tt+1, c ] = U_i2[c] + grad.subs([(array[n], XX[ii, tt+1, n]) for n in range(component)])-grad.subs([(array[n], XX[ii, tt, n]) for n in range(component)])

             U_i=[]
             U_i2=[]


     for c  in range(0, component) :
       print('final states\n', XX[:,tt,c])
       for i in range (0,NN):
        plt.plot(range(0, len(XX[0])), XX[i,:,c], label='agent ' + str(i))

       pylab.legend(loc='upper right')
       plt.title('Consensus achievement')
       plt.ylabel('X' + str(c) + '(t) of each agent')
       plt.xlabel('t (iterations)')
       plt.grid(True)
       plt.show()

     sum=0
     flag=true
     for i in range (0, NN):
         sum = sum + function[i].subs([(array[n], XX[i, tt, n]) for n in range(component)])

     for c in range (0, component):
         if abs(s[0, tt, c])*step > 0.1:
                 flag = false
                 print(abs(s[0, tt, c]))
     if flag == true:
         minV=sum/NN
         print('min Value = ', minV)
         print('function is', function)
     else:
         print('min not found')

     #plt.show()
     #print(' x is \n' + str(XC[:, tt]), 'y is \n', X2[:, tt])
     # ris=0
     # for i in range(0,NN):
     #
     #   ris=ris +func[i].subs([(x, X1[i, tt]), (y, X2[i, tt])])
     #
     # #ris=ris/NN
     # print('the average min is ',ris)
     #
     # plt.plot(ret_data(0), ret_data(1) ,'ro',markersize=4)
     # x = numpy.linspace(-1, 15, 300)
     #
     # plt.plot(x, X1[0, tt] * x + X2[0, tt], linestyle='-')
     # plt.show()
     #
     #
