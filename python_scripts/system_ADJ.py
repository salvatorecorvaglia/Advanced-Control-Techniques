from sympy import *
import numpy


def system_ADJ(size):



    adj_values = [0, 1]
    NN = size
    # NN=float(NN)

    while True:
        Adj = numpy.random.choice(adj_values, [NN, NN], p=[0.8, 0.2])
        v = ones(1, NN - 1)
        Adj = (Adj | numpy.transpose(Adj))
        # FN=float(NN)
        I_NN = numpy.eye(NN, dtype=numpy.int)
        Adj = (Adj | (I_NN))
        #testAdj = (I_NN + Adj)**NN
        testAdj= numpy.linalg.matrix_power((I_NN + Adj),NN)
        #print("test adj is \n" + str(testAdj))
        if (numpy.all(numpy.all(testAdj))):
            print('\nthe graph is connected.\n')
            print("Adj is \n" + str(Adj))

            break
        else:

           print('\nthe graph is disconnected.\n')
    return Adj