import sys
import math
import random
threshold = 0.001

datafile = sys.argv[1]
f = open(datafile)
#f=open("inputdata.data", 'r')
data = []
l = f.readline()

#####Read data
while(l != ''):
	a = l.split()
	l = []
	for j in range(0, len(a), 1):
		l.append(float(a[j]))
	data.append(l)
	l = f.readline()

rows = len(data)
cols = len(data[0])
f.close()
#print (data)

#k = input("Enter k: ")
#k = 2
k1 = sys.argv[2]
k = int(k1)
#k=3
##initial labels
w = {}
n=[0.0001]*k
for i in range(0,rows,1):
	w[i]=random.randint(0, k-1)
	n[w[i]]+=1

objective = 10000
previous = 100000 
#for a in range (0, 100, 1):
while (abs(previous - objective)> threshold):
#while(previous - objective != 0):
##initialize cluster
	previous = objective
	cluster = []
	for i in range(0, rows, 1):
		l = []
		for kk in range(0, k, 1):
			l.append(0)
		cluster.append(l)
	
#initialize means
	m = []
	for kk in range(0, k ,1):
		l = []
		for j in range (0, cols ,1):
			l.append(0)
		m.append(l)
	
##compute means
	for kk in range(0, k, 1):
		for i in range(0, rows, 1):
			if (w.get(i)==kk):
				for j in range(0, cols, 1):
					m[kk][j]=m[kk][j]+data[i][j]
	
####what if n is 0
	for kk in range(0, k, 1):
		for j in range(0, cols ,1):
			m[kk][j] = m[kk][j]/n[kk]

##compute cluster
	for kk in range(0, k, 1):
		for i in range(0, rows ,1):
			for j in range(0, cols, 1):
				cluster[i][kk]=(data[i][j]-m[kk][j])**2+cluster[i][kk]
	
	for i in range(0, rows, 1):
		for kk in range(0, k ,1):
			cluster[i][kk] = math.sqrt(cluster[i][kk])
	

## reassign,update w
	n=[0.0001]*k
	for i in range(0, rows, 1):
		min = 1000000
		k1 = -1
		for kk in range(0, k ,1):
			if (min > cluster[i][kk]):
				min = cluster[i][kk]
				k1 = kk
		w[i] = k1
		n[w[i]]+= 1 
## objective
	objective = 0
	for kk in range(0, k ,1):
		for i in range(0, rows, 1):
			for j in range(0, cols ,1):
				objective += (data[i][j]-m[kk][j])**2	

for i in range(0, rows, 1):
	print("%d %d" % (w.get(i), i))
