import ast

def central_min():
    f = open('/Users/simonemiglietta/Desktop/dataset/min.txt')
    for line in f:
        w = line.split()
    f.close()
    return w[0]

if __name__ == '__main__':
     w=float(central_min())
     #print(w)

