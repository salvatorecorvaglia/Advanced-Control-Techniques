import ast


def ret_data(n):
    f = open('/Users/simonemiglietta/Desktop/dataset/data.txt')
    points = []

    for line in f:
        w = line.split()
        # strx=line[:i]
        points.append(ast.literal_eval(w[n]))

    f.close()
    print(points[0])
    return points
