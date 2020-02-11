import sys
import random
import math

datafile=sys.argv[1]
all_data=open(datafile, 'r')
labelfile=sys.argv[2]
trainlabels_data=open(labelfile, 'r')
temp1=[line.split() for line in all_data]##split data by space
data=[[float(column) for column in row] for row in temp1]##convert data type into float
temp2=[line.split() for line in trainlabels_data]
train_label=[[int(column) for column in row] for row in temp2]# convert trainlabel type into int


for i in range(0,len(data),1):
    data[i].append(1)
rows=len(data)
cols=len(data[0])
################
### initialize w
def dot_product(l1,l2):
    sum=float(0)
    for i in range(0,len(l1),1):
        sum+=l1[i]*l2[i]
    return sum
dellf=[]#iteration results
w=[]
for j in range(0, cols, 1):

    w.append(0.00000001)
    dellf.append(0)

print("please wait for 30 seconds")

eta=0.01
error=0.1

n=0

while 1:
    J=error
    error = 0
    n+=1
    for j in range(0, cols, 1):
        dellf[j]=0  

    for i in range(0, len(train_label), 1):
        r=train_label[i][1]
        sigmoid_function=1/(1+math.exp(-dot_product (w, data [r])))
        if train_label[i][0] == 1:
            error+=-(train_label[i][0]*math.log(sigmoid_function))
            #error+=-1*math.log(dot_product(w, data[r]))
        if train_label[i][0] == 0:
            error+=-((1-train_label[i][0])*math.log(1-sigmoid_function)) 
        for j in range(0, cols, 1):
            dellf[j]+=(train_label[i][0]-sigmoid_function)*data[r][j]
    if abs(J-error)<=0.001:
        break
    
    for j in range(0,cols,1):
        w[j]+= eta*dellf[j]

a=0;
for i in range(cols-1):
    a+=w[i]**2
w1=math.sqrt(a)
distance=w[cols-1]/w1

s=[]
for i in range(0, len(train_label)):
    s.append(train_label[i][1])
s2=[]
for j in range(0, len(data)):
    s2.append(j)
test_data=[]
test_index=[]
for x in s2:
    if x not in s:
        test_data.append(data[x])
        test_index.append(x)

for i in range(0, len(test_index), 1):
    dp=0
    if test_index[i]!= None:
        dp=1/(1+math.exp(-dot_product (w, test_data [i])))
    if  dp < 0.5:
        print("0, ", test_index[i])
    else:
        print("1, ", test_index[i])