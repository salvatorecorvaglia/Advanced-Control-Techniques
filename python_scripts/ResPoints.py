def ResPoints(control):
    points=[]
    i=0
    sum=0
    fun=[]
    vecx=[]
    vecy=[]
    with open("/Users/simonemiglietta/Desktop/dataset/data.txt","r") as data:
        print('data is',data)
        substrings = data.read().split(' ')
        print (substrings[2])
    while i <(len(substrings)-1):
     vecx.append(substrings[i])
     i=i+1
     vecy.append(substrings[i])

     i=i+2
    vecx=[float(i) for i in vecx]
    vecy=[float(i) for i in vecy]

    if control==0:
        return vecx
    else:
        return vecy
