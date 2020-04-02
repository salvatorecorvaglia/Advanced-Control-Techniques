import numpy
from sympy import *

def degree_MTX(Adj,size,control):
    NN = size
    I_NN = numpy.eye(NN, dtype=numpy.int)
    colsum = Adj.sum(axis=0)
    DEGREE = colsum
    if control==0:
      Diag_deg = numpy.diag(DEGREE)
      Lapl = Diag_deg - Adj
      WW = I_NN - 0.05 * Lapl
    else:
      #the lazy metropolis WW
      grad=[0]*size
      WW=zeros(size,size)
      for i in range(0,size):
            grad[i]=0
            for j in range(0,size):
                if Adj[i,j]==1:
                    grad[i] = max(grad[i],DEGREE[j])
      for i in range(0,size):

             for j in range(0,size):
                 if(i!=j):
                    if Adj[i,j]==1:
                        WW[i, j] = 1 / (2 * (grad[i]))
                 if (i==j):
                     WW[i, j] = 1 - (1 / (2 * (grad[i])) * (DEGREE[i] - 1))

    print('WW is \n',WW)


    return WW
