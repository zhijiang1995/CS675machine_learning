import sys
import math
import random

def getFeatureData(featureFile):
    x=[]
    dFile = open(featureFile, 'r')
    for line in dFile:
        row = line.split()
        rVec = [float(item) for item in row]
        x.append(rVec)
    dFile.close()
    return x

def getLabelData(labelFile):
    lFile = open(labelFile, 'r')
    lDict = {}
    for line in lFile:
        row = line.split()
        lDict[int(row[1])] = int(row[0])
    lFile.close()
    return lDict


def sigmoid(y):
    if isinstance(y,list):
        return [sigmoid(item) for item in y]
    else:
        return 1.0/(1+math.exp(-y))


def dotProduct(u,v):
    sum = 0
    for i in range(len(u)):
        sum += u[i] * v[i]
    return sum


def norm(v):
    return math.sqrt(dotProduct(v,v)) 

def matrixMultiply(a,b):
    result = []
    for i in range(len(a)):
        vec = []
        for j in range(len(b[0])):
            elem = 0
            for k in range(len(b)):
                elem += a[i][k] * b[k][j]
            vec.append(elem)
        result.append(vec)
    return result

def vectorMultiply(a,v):
    result = []
    for row in a:
        result.append(dotProduct(row,v))
    return result

def matrixTranspose(a):
    return [[a[i][j] for i in range(len(a))] for j in range(len(a[0]))]


def getMatrixShape(a):
    return '(' + str(len(a)) + ", " + str(len(a[0])) + ')'


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


def main():
    eta_list = [1, .1, .01, .001, .0001, .00001, .000001, .0000001, .00000001, .000000001, .0000000001, .00000000001]

    # Get the file names from the command line
    featureFile = sys.argv[1]
    labelFile = sys.argv[2]

    x_total = getFeatureData(featureFile)
    x_train_label = getLabelData(labelFile)
    num_x_total = len(x_total)
    

    X = []
    for key in x_train_label:
        X.append(x_total[key])
    for i in range(len(X)):
        X[i].insert(0, 1.)

    # n: number of samples
    n = len(X)

    # m: number of features
    m = len(X[0]) - 1

    y = [[x_train_label[key]] for key in x_train_label]
  
    # Initialize components of w, an m+1 dimensional vector
    # wi's range is (-0.01, 0.01)
    w = [[(random.random() - 0.5) * 0.02] for i in range(m + 1)]

    # # Learning rate: eta
    # eta = 0.0001
    # Stop condition: theta
    theta = 0.001

    # Initialize the error
    prevE = sys.maxsize
    
    # Start iteration
    while True:
        # Initilize bestobj
        bestobj = 1000000000000

        # Diff vector: d, shape = n * 1 
        d = vectorSubtraction(y, matrixMultiply(X, w))

        # Partial derivative: partial_E, shape = (m+1) * 1
        partial_E = matrixMultiply(matrixTranspose(d), X) # shape = 1 * (m+1)
        partial_E = matrixTranspose(partial_E)

        for k in range(0, len(eta_list), 1):
            eta = eta_list[k]
        
            # Delta w: delta_w, shape = (m+1) * 1
            delta_w = [[eta * i[0]] for i in partial_E]
        
            # Update vector w
            w = vectorAddition(w, delta_w)

            # Diff vector: d, shape = n * 1 
            d = vectorSubtraction(y, matrixMultiply(X, w))

            # Error: E, scalar
            E = 1 / 2 * matrixMultiply(matrixTranspose(d), d)[0][0]

            obj = E
            
            ##update bestobj and best_eta
            if (obj < bestobj):
                bestobj = obj
                best_eta = eta

            ##remove the eta for the next
            w = vectorSubtraction(w, delta_w)

        eta = best_eta

        delta_w = [[eta * i[0]] for i in partial_E]

        w = vectorAddition(w, delta_w)

        E = 1 / 2 * matrixMultiply(matrixTranspose(d), d)[0][0]

        if prevE - E <= theta:
            break

        prevE = E


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



main()
