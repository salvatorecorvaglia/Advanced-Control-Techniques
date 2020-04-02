from sympy import *
import ast

def dataNodes(size):
    points=[]
    i=0
    sum=0
    fun=[]
    vecx=[]
    vecy=[]
    # with open("/Users/simonemiglietta/Desktop/dataset/data.txt","r") as data:
    #     substrings = data.read().split(' ')
    #     print (substrings[2])
    # while i <(len(substrings)-1):
    #  vecx.append(substrings[i])
    #  i=i+1
    #  vecy.append(substrings[i])
    #
    #  i=i+2
    f = open('/Users/simonemiglietta/Desktop/dataset/data.txt')
    points = []

    for line in f:
        w = line.split()
        # strx=line[:i]
        points.append(ast.literal_eval(w[0]))

    f.close()
    vecx=points
    f = open('/Users/simonemiglietta/Desktop/dataset/data.txt')
    points = []

    for line in f:
        w = line.split()
        # strx=line[:i]
        points.append(ast.literal_eval(w[1]))

    f.close()
    vecy=points
    #vecx=[float(i) for i in vecx]
    #vecy=[float(i) for i in vecy]
    print('vecx are', vecx, '\nvecy are',vecy)
    x0 = Symbol('x0')
    x1 = Symbol('x1')
    number=(len(vecx)//size)
    count=0
    for i in range(0,size):

       for k in range(i*number,(i+1)*number):
           sum= sum +expand((vecx[k]*x0+ x1 -vecy[k])**2)

           #print('points are',k)
       fun.append(sum)

       sum = 0
    print(fun)

    return fun


if __name__ == "__main__":
    vecx=dataNodes(5)
