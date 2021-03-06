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

def vectorMultiplication(vector1, vector2):
    n1 = len(vector1)
    n2 = len(vector2)

    assert(n1 == n2)\
    , "Vectors subtraction error: Subtraction of two different size vectors!"

    retVector = [[0] for i in range(n1)]

    for i in range(n1):
        retVector[i][0] = vector1[i][0] * vector2[i][0]

    return retVector

def getMax(vector):
    n = len(vector)

    retVector = [[0] for i in range(n)]

    for i in range(n):
        if vector[i][0] > 0:
            retVector[i][0] = vector[i][0]
        else:
            retVector[i][0] = 0.

    return retVector

def sumVector(vector):
    n = len(vector)

    retScalar = 0

    for i in range(n):
        retScalar += vector[i][0]

    return retScalar

def main():
    eta_list = [1, .1, .01, .001, .0001, .00001, .000001, .0000001, .00000001, .000000001, .0000000001, .00000000001]

    # Get the file names from the command line
    featureFile = sys.argv[1]
    labelFile = sys.argv[2]

    x_total = getFeatureData(featureFile)
    x_train_label = getLabelData(labelFile)

    for i in range(len(x_total)):
        x_total[i].insert(0, 1.)

    # Convert all 0's into -1's of labels
    for i in x_train_label:
        if x_train_label[i] == 0:
            x_train_label[i] = -1
    
    num_x_total = len(x_total)
    
    X = []
    for key in x_train_label:
        X.append(x_total[key])

    # n: number of samples
    n = len(X)

    # m: number of features
    m = len(X[0]) - 1

    y = [[x_train_label[key]] for key in x_train_label]


    w = [[(random.random() - 0.5) * 0.02] for i in range(m + 1)]

    theta = 0.001

    prevE = sys.maxsize

    count = 0
    
    while True:
        bestobj = 1000000000000

        yHat = matrixMultiply(X, w)

        y_times_yHat = vectorMultiplication(y, yHat)

        wi = [[0] for i in range(n)]
        for i in range(n):
            if y_times_yHat[i][0] < 1:
                wi[i] = y[i]

        partial_E = matrixMultiply(matrixTranspose(X), wi)

        for k in range(0, len(eta_list), 1):
            eta = eta_list[k]

            delta_w = [[eta * i[0]] for i in partial_E]
            
            w = vectorAddition(w, delta_w)
                   
            yHat = matrixMultiply(X, w)

            y_times_yHat = vectorMultiplication(y, yHat)

            ones = [[1] for i in range(n)]
            one_minus_y_times_yHat = vectorSubtraction(ones, y_times_yHat)

            E_vector = getMax(one_minus_y_times_yHat)

            E = sumVector(E_vector)

            obj = E
            
            if (obj < bestobj):
                bestobj = obj
                best_eta = eta

            w = vectorSubtraction(w, delta_w)

        eta = best_eta

        # Delta w: delta_w, shape = (m+1) * 1
        delta_w = [[eta * i[0]] for i in partial_E]
        
        # Update vector w
        w = vectorAddition(w, delta_w)
        
        # Calculate yHat
        yHat = matrixMultiply(X, w)

        # Calculate yi * yHati
        y_times_yHat = vectorMultiplication(y, yHat)

        # Calculate 1 - yi * yHati
        ones = [[1] for i in range(n)]
        one_minus_y_times_yHat = vectorSubtraction(ones, y_times_yHat)

        # Calculate E_vector
        E_vector = getMax(one_minus_y_times_yHat)

        # Error: E, scalar
        E = sumVector(E_vector)
        
        # Check stop condition
        if abs(prevE - E) < theta:
            break

        # Updata the current error
        prevE = E

    x_test = []
    for i in range(num_x_total):
        if i not in x_train_label:
            x_test.append(i)
    
    # Print the result
    for i in x_test:
        sample = [[element] for element in x_total[i]]
        
        prediction = matrixMultiply(matrixTranspose(w), sample)[0][0]
        print(0, i) if prediction < 0 else print(1, i)

main()
