import sys
import math
import random

x_total = []
datafile=sys.argv[1]
dFile = open(datafile,'r')
for line in dFile:
    row = line.split()
    rVec = [float(item) for item in row]
    x_total.append(rVec)
dFile.close()

trainlabelfile=sys.argv[2]
lFile = open(trainlabelfile,'r')
x_train_label = {}
for line in lFile:
    row = line.split()
    x_train_label[int(row[1])] = int(row[0])

lFile.close()

num_x_total = len(x_total)

def matrixMultiply(c, d):
    result = []
    for i in range(len(c)):
        vec = []
        for j in range(len(d[0])):
            elem = 0
            for k in range(len(d)):
                elem += c[i][k] * d[k][j]
            vec.append(elem)
        result.append(vec)
    return result

def matrixTranspose(e):
    return [[e[i][j] for i in range(len(e))]for j in range(len(e[0]))]    

def vectorAddition(vector1, vector2):
    n1 = len(vector1)
    n2 = len(vector2)

    assert(n1 == n2)\
    , "Vectors addition error: Additon of two different size vectors!"

    retVector = [[0] for i in range(n1)]

    for i in range(n1):
        retVector[i][0] = vector1[i][0] + vector2[i][0]

    return retVector

def vectorSubtraction(vector1, vector2):
    n1 = len(vector1)
    n2 = len(vector2)

    assert(n1 == n2)\
    , "Vectors subtraction error: Subtraction of two different size vectors!"

    retVector = [[0] for i in range(n1)]

    for i in range(n1):
        retVector[i][0] = vector1[i][0] - vector2[i][0]

    return retVector






X = []
for key in x_train_label:
    X.append(x_total[key])
for i in range(len(X)):
    X[i].insert(0,1.0)

n = len(X)

m = len(X[0]) - 1

y = [[x_train_label[key]] for key in x_train_label]

w = [[(0.02*random.uniform(0,1)-0.01)]for i in range(m + 1)]

eta = 0.0001

theta = 0.0001

prevError = sys.maxsize

count = 0

print("\nPlease wait for 30 seconds\n")

while True:
    count += 1

    d = vectorSubtraction(y, matrixMultiply(X,w))

    E = 1 / 2 * matrixMultiply(matrixTranspose(d),d)[0][0]

    if prevError - E <= theta:
        break

    partial_E = matrixMultiply(matrixTranspose(d),X)
    partial_E = matrixTranspose(partial_E)

    delta_w = [[eta*i[0]] for i in partial_E]

    w = vectorAddition(w, delta_w)

    prevError = E

x_test = []
for i in range(num_x_total):
    if i not in x_train_label:
        x_test.append(i)
    
    # Print the result

for i in x_test:
    sample = [[element] for element in x_total[i]]
    sample.insert(0, [1.])
        
    # prediction is a scalar
    prediction = matrixMultiply(matrixTranspose(w), sample)[0][0]
    print(0, i) if prediction < 0.5 else print(1, i)

# Print w'
print("\nw' = [w1, w2, ..., wd] is as follows:\n")
w_ = w[:]
w0 = w_.pop(0)[0]
print(w_)

# Calculate the distance
distance = abs(w0 / matrixMultiply(matrixTranspose(w_), w_)[0][0] ** 0.5)
print("\nHyperplane's distance from origin is", distance)