import sys
import math
import random
#threshold = 0.01

datafile = sys.argv[1]
f = open(datafile)
# f=open("inputdata.data", 'r')
data = []
l = f.readline()
i = 0

#####Read data
while(l != ''):
	a = l.split()
	l2 = []
	for j in range(0, len(a), 1):
		l2.append(float(a[j]))
	l2.append(i)
	data.append(l2)
	l = f.readline()
	i = i + 1
allrows=len(data)
cols = len(data[0])-1
f.close()
#print('cols',cols)
###Read labels
labelfile=sys.argv[2]
f=open(labelfile)
# f=open("input.trainlabels.0", 'r')
trainlabels={}
l=f.readline()
while(l!=''):
	a=l.split()
	trainlabels[int(a[1])]=int(a[0])
	if (trainlabels[int(a[1])]==0):
		trainlabels[int(a[1])]=-1
	l = f.readline()
f.close()
#print('data',data)
#print('trainlabels',trainlabels)
rows = len(trainlabels)
#separate testdata
testrows=len(data)-len(trainlabels)
#print('testrows',testrows)
test_data=[]
train_data=[]
for i in range(0,allrows,1):
    if (trainlabels.__contains__(i)==0):
        test_data.append(data[i])
    else:
        train_data.append(data[i])
#print('test_data',test_data)
#print('train_data',train_data)
test_class=[]
for i in range(0,testrows,1):
    test_class.append([])
#random select colums
rcols=int(1/3*cols)
#print('rcols',rcols)
for m in range(0,100,1):
    rc=[]#random cols index array
    for i in range(0,rcols,1):
        rc.append(0)
        rc[i]=random.randint(0,cols-1)
        for j in range (0,i,1):
            if(rc[i]==rc[j]):
                rc[i]=random.randint(0,cols)
    #print('rc',rc)
    #random gernerate rows
    rrow=[]#random rows index
    for i in range(0,rows,1):
        rrow.append(0)
        rrow[i]=random.randint(0,rows-1)
    #print('rrow',rrow)
    #save random sample
    #sample two dimension list rows and rcols colums
    sample=[([0] * rcols) for i in range(rows)]
    for i in range(0,rows,1):
        for j in range(0,rcols,1):
            sample[i][j]=train_data[rrow[i]][rc[j]]
        sample[i].append(train_data[rrow[i]][-1])
    #print('sample',sample)
    
    #####gini function
    def gini_caculation (j, s):
        lp = 0.0
        rp = 0.0
        lsize = 0.0
        rsize = 0.0
        #print('ginidata',data)
        for i in range(0, rows, 1):
            if  sample[i][j]<=s:
                lsize=lsize+1
            if trainlabels[int(sample[i][rcols])]==-1:
                lp=lp+1
            if sample[i][j]>s:
                rsize=rsize+1
            if trainlabels[int(sample[i][rcols])]==-1:
                rp=rp+1
        if lsize==0:
            gini = (rsize/float(rows))*(rp/float(rsize))*(1-rp/float(rsize))
        elif rsize==0:
            gini = (lsize/float(rows))*(lp/float(lsize))*(1-lp/float(lsize))
        else:
        	 #print (lp,rp,lsize,rsize)
            gini = (lsize/float(rows))*(float(lp)/float(lsize))*(1-lp/float(lsize))+(rsize/float(rows))*(rp/float(rsize))*(1-rp/float(rsize))	
        return(gini)
    
    def gini_caculation1 (j, s):
        lp = 0.0
        rp = 0.0
        lsize = 0.0
        rsize = 0.0
        #print('gini_caculation',sample)
        for i in range(0, rows, 1):
            if sample[i][j]<s:
                lsize=lsize+1
            if trainlabels[int(sample[i][rcols])]==-1:
                lp=lp+1
            if sample[i][j]>=s:
                rsize=rsize+1
            if trainlabels[int(sample[i][rcols])]==-1:
                rp=rp+1
        if lsize==0:
            gini = (rsize/float(rows))*(rp/float(rsize))*(1-rp/float(rsize))
        elif rsize==0:
            gini = (lsize/float(rows))*(lp/float(lsize))*(1-lp/float(lsize))
        else:
    		#print (lp,rp,lsize,rsize)
            gini = (lsize/float(rows))*(float(lp)/float(lsize))*(1-lp/float(lsize))+(rsize/float(rows))*(rp/float(rsize))*(1-rp/float(rsize))	
        return(gini)
    
    ####sort data
    c =[]
    def sortdata(j):
        for i in range(0, rows, 1):
            c.append(sample[i][j])
        c.sort()
        return c
    
    ####initialize s and k
    bests =[]
    for j in range(0, rcols, 1):
    	bests.append(0)
    
    k =[]
    for j in range(0, rcols, 1):
    	k.append(0)
    
    ####split data
    for j in range(0,rcols,1):
        c=[]
        c=sortdata(j)
        s=0
        s1=0
        gini=0.0
        mini_gini=10000
        for i in range(0, rows+1, 1):
        	if (i==0):
        		s = c[0]
        		gini = gini_caculation1(j, s)
        	elif (i==rows):
        		s = c[rows-1]
        		gini = gini_caculation(j, s)
        	else:
        		s=(c[i-1]+c[i])/2
        		if (s!= c[i-1] and s!= c[i]):
        			gini = gini_caculation(j, s)
        		else:
        			continue
        	if (mini_gini > gini):
        		mini_gini = gini
        		s1 = s
        k[j] = mini_gini
        bests[j] = s1
    
    min_k = 1000
    min_s = 0
    k1 = -1
    for j in range(0, rcols, 1):
        if min_k > k[j]:
            min_k = k[j]
            min_s = bests[j]
            k1 = j
    print ("best split value is: %.6f" % (min_s))
    print ("lowest gini is: %.12f" % (k[k1]))
    k1=rc[k1]
    print ("column: %d" %(k1))
    #prediction
    
    #test_class=[([0] * 10) for i in range(rows)]
    for i in range(0,testrows,1):
        if test_data[i][k1]>min_s:
            test_class[i].append(1)
        else:
            test_class[i].append(0)
sum_class=[]
prediction=[]
for i in range(0,testrows,1):
    sum_class.append(0)
    prediction.append([])
for i in range(0,testrows,1):
    for j in range(0,100,1):
        sum_class[i]+=test_class[i][j]
    if sum_class[i]>=50:
        sum_class[i]=1
    else:
        sum_class[i]=0
    prediction[i].append(sum_class[i])
    prediction[i].append(test_data[i][-1])
#print('sum_class',sum_class)
print('The majority vote of the predictions are as follows:')
print('[class,index]')
for i in range(0,testrows,1):
    print(prediction[i])
