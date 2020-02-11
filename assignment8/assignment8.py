import sys
import random
import math

datafile = sys.argv[1]

f = open(datafile, 'r')
data = []
line = f.readline()

while (line != ''):
    temp = line.split()
    a2 = []
    for c in range(0, len(temp), 1):
        a2.append(float(temp[c]))
    data.append(a2)
    line = f.readline()
rows = len(data)
cols = len(data[0])
f.close()


k = int(sys.argv[2])
col = [0 for _ in range(0, cols, 1)]
anew = [col for _ in range(0, k, 1)]

ini_val = 0
for f in range(0, k, 1):
    ini_val = random.randrange(1, rows-1)
    anew[f] = data[ini_val]
trainlbl = {}
diff = 1
prev = [[0]*cols for g in range(k)]
mdist = [0 for _ in range(0, k, 1)]
n_size = [0.1 for _ in range(0, k, 1)]
length_dist = [0.1 for _ in range(0, k, 1)]
total = 1
centroid = []
while ((total) > 0):
    for a in range(0,rows, 1):
        length_dist =[]
        for f in range(0, k, 1):
            length_dist.append(0)
        for f in range(0, k, 1):
            for c in range(0, cols, 1):
                length_dist[f] += ((data[a][c] - anew[f][c])**2)
        for f in range(0, k, 1):
            length_dist[f] = (length_dist[f])**0.5
        mindist=0
        mindist = min(length_dist)
        for f in range(0, k, 1):
            if(length_dist[f]==mindist):
                trainlbl[a] = f
                n_size[f]+=1
                break
    anew = [[0]*cols for g in range(k)]
    col = []
    for a in range(0, rows, 1):
        for f in range(0, k, 1):
            if(trainlbl.get(a) == f):
                for c in range(0, cols, 1):
                    temp =  anew[f][c]
                    temp1 =  data[a][c]
                    anew[f][c] = temp + temp1
    for c in range(0, cols, 1):
        for a in range(0, k, 1):
            anew[a][c] = anew[a][c]/n_size[a]
    centroid = [int(g) for g in n_size]
    n_size=[0.1]*k
    mdist = []
    for f in range(0, k, 1):
        mdist.append(0)
    for f in range(0, k, 1):
        for c in range(0, cols, 1):
            mdist[f]+=float((prev[f][c]-anew[f][c])**2)

        mdist[f] = (mdist[f])**0.5
    
    prev=anew
    total = 0
    for i in range(0,len(mdist),1):
        total += mdist[i]
print("Clustered data",k,"is",centroid)
for a in range(0,rows, 1):
    print(trainlbl[a],a)