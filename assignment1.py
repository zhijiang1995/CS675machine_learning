import sys

datafile = sys.argv[1]
file = open(datafile, 'r')
data = []
raw1 = file.readlines()
for i in range(len(raw1)):
    temp1 = raw1[i].split()
    temp2 = []
    for j in range(0,len(temp1)):
        temp2.append(float(temp1[j]))
    data.append(temp2)
rows = len(data)
cols = len(data[0])
file.close()

trainlabelfile=sys.argv[2]
file=open(trainlabelfile, 'r')
trainlabels = {}
n0 = 0
n1 = 0
raw2 = file.readlines()
for i in range(len(raw2)):
    temp3 = raw2[i].split()
    trainlabels[int(temp3[1])] = int(temp3[0])
for i in range(len(raw1)):
    if(trainlabels.get(i) != None and trainlabels[i] == 0):
        n0 += 1
    if(trainlabels.get(i) != None and trainlabels[i] == 1):
        n1 += 1
file.close()
m0 = []
for j in range(0,cols):
    m0.append(0.1)
m1 = []
for j in range(0,cols):
    m1.append(0.1)
for i in range(0,rows):
    if(trainlabels.get(i) != None and trainlabels[i] == 0):
        for j in range(0,cols):
            m0[j] = m0[j] + data[i][j]
    if(trainlabels.get(i) != None and trainlabels[i] == 1):
        for j in range(0,cols):
            m1[j] = m1[j] + data[i][j]
for j in range(0,cols):
    m0[j] = m0[j]/n0
    m1[j] = m1[j]/n1 
s0 = []
for j in range(0,cols):
    s0.append(0)
s1 = []
for j in range(0,cols):
    s1.append(0.1)
for i in range(0,rows):
    if(trainlabels.get(i) != None and trainlabels[i] == 0):
        for j in range(0,cols):
            s0[j] = s0[j] + (data[i][j] - m0[j])**2
    if(trainlabels.get(i) != None and trainlabels[i] == 1):
        for j in range(0,cols):
            s1[j] = s1[j] + (data[i][j] - m1[j])**2
for j in range(0,cols):
    s0[j] = (s0[j]/n0)**0.5
    s1[j] = (s1[j]/n1)**0.5
for i in range(0,rows):
    if(trainlabels.get(i) == None):
        d0 = 0
        d1 = 0
        for j in range(0,cols):
            d0 = d0 + ((m0[j] -data[i][j])/s0[j])**2
            d1 = d1 + ((m1[j] -data[i][j])/s1[j])**2
        if(d0<d1):
            print("0 ",i)
        else:
            print("1 ",i)
	
