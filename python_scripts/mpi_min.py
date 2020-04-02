from random import random

from mpi4py import MPI
from degree_MTX import degree_MTX

import sys
from system_ADJ import system_ADJ
from partial_sum import partial_sum
import numpy
from sympy import *
from ret_data import ret_data
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt1
import pylab
from math import *
from central_min import central_min


if __name__ == "__main__":

    comm = MPI.COMM_WORLD          # definisce il communicator
    rank = comm.Get_rank()         # il rank identifica il thread
    size = comm.Get_size()
    vecx = []
    vecy = []
    vect_X = []
    vect_Y = []
    function_s = []
    result = []

    if rank == 0:
        centr_m = central_min()   # get the minimum value of f = sum( f(i)) from the Matlab centralized solver, by reading from a file
        difference = []           # note that the central solver must be updated if  f = sum( f(i)) changes

        while True:
            quad = input('Would you like to solve a least square problem? Use (y or yes) (n or no)\n')
            if quad == 'yes' or quad == 'y':
               break
            if quad == 'n' or quad == 'no':
                inputfunction = []
                positive = false
                while positive == false:
                  try:
                    component = int(input('enter number of components:\n'))     # specify domain of function
                    if component <=0:
                        print('please enter an acceptable number.')
                    else:
                        positive = true
                    array = []

                  except ValueError:
                      print('please enter an acceptable number.')


                array.append(symbols('x0:%d' % component))

                positive=false
                while positive ==false:
                  try:
                    test = int(input('how many functions would you like to insert, 1 (for all) or '+str(size)+ '?\n'))
                    #  insert one function if you want that each node gets the same function f(i) , or specify manually each f(i)


                    if test == 1 or test == size:
                        positive = true


                    else:
                        print('please enter an acceptable number.')
                  except ValueError:
                      print('please enter an acceptable number.')


                counter = 0
                while counter < test:
                    try:
                        buffer = (input('enter function ' + str(counter + 1) + ':\n'))     #  NOTE!!! the function/s must be written as symbolic function/s
                                                                                           #  according with  Python syntax and functions interpreter
                                                                                           # i.e the ' ^ ' operator becomes ' ** '
                        function_s.append(expand(buffer))

                        #inputfunction.append(buffer)


                        counter = counter +1
                    except Exception:
                        print('Syntax error, please enter the current function again')


                # for i in range(0, test):
                #     inputfunction.append(input('enter function ' +str(i+1)+':\n'))
                #     function_s.append(expand(inputfunction[i]))
                break
            else:
                print('Invalid answer. ')

        ADJ = system_ADJ(size)           # get Adj
        WW = degree_MTX(ADJ, size, 1)    # get weight matrix
        if quad=='y' or quad=='yes':     # if solving a least square problem then retrieve the dataset points
            points_X = []
            points_Y = []
            points_X = ret_data(0)
            points_Y = ret_data(1)

            portion = len(points_X) // size
            i = portion
            vect_X.append(points_X[0:portion])
            vect_Y.append(points_Y[0:portion])
            n = rank + 1
            for n in range(rank + 1, size - 1):           # divide points to each agent, if not divisible append residuals to last node
                j = i + portion
                vect_X.append(points_X[i: j])
                vect_Y.append(points_Y[i: j])

                i = j

            n = n + 1
            vect_X.append(points_X[i: len(points_X)])    #  points to the last
            vect_Y.append(points_Y[i: len(points_Y)])
            component=2


    else:
        ADJ = None
        WW = None
        test = None
        component = None
        #array = None
        myfunction = None
        quad= None

    ADJ = comm.bcast(ADJ, root=0)            # 0 send in broadcast the exential common informations
    WW = comm.bcast(WW, root=0)
    test = comm.bcast(test, root=0)

    component = comm.bcast(component, root=0)
    quad = comm.bcast(quad, root=0)

    #array = comm.bcast(array,root=0)



    if quad=='y' or quad=='yes':
        MAX_ITERS = 1000                       # if least square problem set iteration
        vecx = comm.scatter(vect_X, root=0)
        vecy = comm.scatter(vect_Y, root=0)    # scatter points to each node
        if size > 2:
            step = 0.0005 + (0.0002 * (size - 2))   # set the stepsize
        else:
            step = 0.0005
        component = 2                       # set the State dimension to 2
        partial = partial_sum(vecx, vecy)   # got the f (0)
        myfunction = partial
        print('function', myfunction)
        array = []
        array.append(symbols('x'))
        array.append(symbols('y'))
        # array = numpy.asarray(array)
        # array = array.tolist()
        # array = array[0]
        #print('array', array)



    else:                                                      # if you are not going to solve a least square problem then:
        if test == 1:
            myfunction = comm.bcast(function_s, root=0)          # if you have chosen to insert a single function then send in broadcast
            myfunction = myfunction[0]
        else:
            myfunction = comm.scatter(function_s, root=0)       # if you have specified each f(i) manually, then distribute to each node
        # print('My function is :', myfunction)
        MPI.COMM_WORLD.Barrier()
        step = 0.01
        MAX_ITERS = 600                                        # set parameter for a generic  min problem
        array = []
        array.append(symbols('x0:%d' % component))             # declare symbolic components
        array = numpy.asarray(array)
        array = array.tolist()
        array = array[0]
    # destination = []
    #
    #
    XX = numpy.empty([MAX_ITERS, component])
    all_a = numpy.empty([size, MAX_ITERS, component])

    for i in range(0, component):

        Xi = 10 * random()
        XX[0, i] = float(Xi)

    s = numpy.empty([size, MAX_ITERS, component])             # define the State matrix and the average gradient s
    States_x = numpy.empty([size, component])
    s_all = numpy.empty([size, MAX_ITERS, component])
    total_value = numpy.zeros(size)
    #print('XX is', XX[0,:], 'rank', rank)

    #States_x= numpy.empty(size,component)
    #print('function', len(myfunction))
    for tt in range(0, MAX_ITERS-1):

        local_value = myfunction.subs([(array[n], XX[tt, n]) for n in range(component)])         # 0 collect the  actual minimum value
        total_value[:] = comm.gather(local_value, root=0)
        MPI.COMM_WORLD.Barrier()
        if rank==0:
            sumT = 0
            for g in range(0, size):
                sumT = sumT + total_value[g]
            difference.append(float(sumT) - float(centr_m))                       # save the minimum estimation at tt  in a list

        # if (numpy.mod(tt, 10) == 0):
        #     local_value = myfunction.subs([(array[n], XX[tt, n]) for n in range(component)])
        #     total_value[:] = comm.allgather(local_value)
        #     MPI.COMM_WORLD.Barrier()


        if (numpy.mod(tt, 10) == 0) and rank == 0:
            # sumT=0
            # for g in range(0, size):
            #     sumT = sumT + total_value[g]
            # difference.append(float(sumT) - float(centr_m))
            print('\nIteration  ' + str(tt) + '/' + str(MAX_ITERS) + '\n')

            sys.stdout.flush()

        U_i2x = numpy.zeros(component)      # clear the input
        U_ix = numpy.zeros(component)

        if tt == 0:

            for c in range(0, component):
                gradien = diff(myfunction, array[c])          # for each component compute the symbolic derivative and subs points

                s[rank, 0, c] = gradien.subs([(array[n], XX[0, n]) for n in range(component)])

                # got the gradient


        States_x[:,:]= comm.allgather(XX[tt,:])


        if rank == 0 and tt == MAX_ITERS - 2:

           print('X is\n', States_x)

        s[:, tt, :] = comm.allgather(s[rank, tt, :])
        MPI.COMM_WORLD.Barrier()

        #contiene gli stati di tutti i nodi

        destination = ADJ[rank, :]                   # send local states to nodes

        for c in range (0, component):
          States_x[:,c] = States_x[:,c] * destination

          s[:, tt, c] = s[:, tt, c] * destination        # get the neighbors

        for jj in range(0,size):
           for c in range (0,component):
              U_ix[c] = U_ix[c] + WW[rank, jj] * States_x[jj, c]        # weight neighbors states
              U_i2x[c] = U_i2x[c] + WW[rank, jj] * s[jj, tt, c]

        for c in range(0, component):
            XX[tt+1, c] = U_ix[c] - step * s[rank, tt, c]            # update local state

        for c in range (0, component):
            gradien = diff(myfunction, array[c])                # update average gradient
            s[rank, tt +1, c] = U_i2x[c] + gradien.subs([(array[n], XX[ tt+1, n]) for n in range(component)]) - gradien.subs([(array[n], XX[tt, n]) for n in range(component)])

    all_a[:] = comm.gather(XX, root=0)
    total_value = numpy.zeros(size)
    local_value = myfunction.subs([(array[n], XX[tt, n]) for n in range(component)])    # 0 got the sum of f(i)
    total_value[:] = comm.gather(local_value, root=0)
    MPI.COMM_WORLD.Barrier()




    if rank == 0 and tt == MAX_ITERS - 2:
         if quad == 'yes ' or quad == 'y':
             plt.figure(figsize=(8, 5))
             plt.title('Least Squares Regression Line')      # plot section
             plt.grid(True)
             plt.ylabel('y')
             plt.xlabel('x')
             plt.plot(ret_data(0), ret_data(1), 'ro', markersize=4)
             x = numpy.linspace(0, 15, 300)
             plt.plot(x, XX[tt, 0] * x + XX[tt, 1], linestyle='-')
             plt.show()

         for c in range(0, component):
                plt.figure(figsize=(11, 6))

                for i in range(0, size):
                    plt.plot(range(0, tt), all_a[i, :tt, c], label='agent ' + str(i))

                pylab.legend(loc='upper right')
                plt.title('Consensus achievement')
                plt.ylabel('X' + str(c) + '(t) of each agent')
                plt.xlabel('t (iterations)')
                plt.grid(True)
                plt.show()
                sumT = 0


         flag = true
         for g in range(0, size):               # 0 sum the f(i)
             sumT = sumT + total_value[g]

         plt1.figure(figsize=(11, 6))              # plot on a file the difference from the minimum found by the central algorithm and by this one
         plt1.plot(range(1, len(difference)), difference[1:], label='agent')
         plt1.title('Comparison of minimum cost value between the MPI algorithm and the centralized one:')
         plt1.ylabel(' minimum value difference at each iteration  (dB) ')
         plt1.xlabel('t (iterations)')
         plt1.yscale('log')
         plt1.savefig('/Users/simonemiglietta/Desktop/dataset/Comparison.png')



         for c in range (0,component):     # NOTE : this is only a QUALITATIVE control on the gradient value: if we got a minimum then the gradient
                                           # of f will be 0. A gradient descent method, is very slow near the gradient 0 value, so we have to choose
                                           # a majorant of 0 small enough

             if (s[rank, tt , c]* step > 0.001):
                 flag = false

                 # the input function can be interpreted both  as the 'bigger ' function from which we want the minimum value, (see the 'average' print)
                 # or as single function f(i) that each node should have; in this case each f(i) is a partial sum of the 'bigger ' function
                 # obtained by summing all f(i), so even the minimum value must be the sum  (to get  the 'bigger' function minimum)

         if flag == true:      # the x found is the one that minimize both the sum and the average of the given function(s)
            print('minimum sum value is ', sumT)            # if you have specified a/N function/s  f(i) to distribute equally to nodes, then look here
            print('the minimum value of average is', sumT/size)    # if you have specified a 'bigger' function and want to have the corresponding minimum value, look here

         else:
             print('minimum not found')


