import sys
import math
import numpy as np

from kernel import gaussianKernel 
def KSIR(K, y):	
	B = 1
	#y = np.array(y)
	# K must be numpy
	n,p = [len(K), len(K[0])]

	label = np.unique(y)
	sorty = np.array(sorted(y))
	index = np.sort(np.argsort(y)[0])
	#print "index:\n", index
	K = K[index, :]

	Kmean = np.mean(K,0)
	#for classification
	numOfSlice = len(label)
	smean_c = np.zeros([numOfSlice, p])
	
	#print Kmean
	for k in range(numOfSlice):	
		#print np.sqrt(sum((sorty == label[k])[0]) / float(n))
		smean_c[k,:] = (np.mean(K[np.where(sorty == label[k])[1],:],0) - Kmean) * np.sqrt(sum((sorty == label[k])[0]) / float(n))
		#smean_c(k,:)=(mean(K(Sorty==class(k),:))-Kmean)*sqrt(sum(Sorty==class(k))/n);
	#print smean_c[2]
	'''
	#for regression
	sizeOfSlice = int(n / NumOfSlice)
	m = n % NumOfSlice
	base = np.zeros([2,1])
	smean_c = np.zeros([NumOfSlice, p])
	for k in range(NumOfSlice):
		count = sizeOfSlice + (k<m+1)
		base[1] = base[1] + count

		#print len((np.mean(K[base[0]+1:base[1],:], 0) - Kmean))
		smean_c[k,:] = (np.mean(K[base[0]+1:base[1],:], 0) - Kmean) * (math.sqrt((base[1] - base[0]) / n))
		#smean_c(k,:) =(mean(K(base(1)+1:base(2),:),1)-Kmean)*sqrt((base(2)-base(1))/n);
		base[0] = base[1]
	'''
	#print len(Kmean.T)
	Kmean = np.array([Kmean])
	#print "test", len(np.dot(Kmean.T , Kmean)), len(np.dot(Kmean.T , Kmean)[0])
	Cov_K = ((np.dot(K.T, K))/n) - np.dot(Kmean.T , Kmean)
	#print Cov_K[2]
	#print (Cov_K+np.spacing(1)*np.eye(p))[0]
	#print "test:", len((Cov_K+np.spacing(1)*np.eye(p))), len((Cov_K+np.spacing(1)*np.eye(p))[0])
	Temp = np.linalg.lstsq((Cov_K+np.spacing(1)*np.eye(p)), smean_c.T)[0]
	print  smean_c.shape
	#print smean_c[0]
	#test = np.dot(np.linalg.inv(Cov_K+np.spacing(1)*np.eye(p)), smean_c.T)
	#print (Cov_K+np.spacing(1)*np.eye(p)).shape, smean_c.T.shape
	
	
	#print np.linalg.lstsq((Cov_K+np.spacing(1)*np.eye(p))[0:3], smean_c[:,0:3].transpose())
	U,D,s = np.linalg.svd(np.dot(smean_c, Temp))
	d = np.zeros([len(D), len(D)])
	
	for i in range(len(D)):
		d[i][i] = D[i] 
	D = d
	
	D,Index = [sorted(np.diag(D), reverse = True), np.argsort(np.diag(D))]
	D = D[:-1]
	U = U[:,Index[:-1]]
	#print D
	#print np.diag(1./np.sqrt(D))
	Ksir_dir = np.dot(B*(np.dot(Temp, U)), np.diag(1./np.sqrt(D)))
	return Ksir_dir


if __name__=="__main__":
	if len(sys.argv) < 2:
		print "Usage: <Data>"
		exit(-1)
	#out = open('k_sir.csv','w')	
	filename = sys.argv[1]
	irisData = np.genfromtxt(filename, delimiter = ',')
	irisData = irisData[:,:-1]

	Label = np.genfromtxt(filename, delimiter = ',', dtype = str)
	irisLabel = []
	a = [0]*50
	b = [1]*50
	c = [2]*50
	irisLabel.append(a)
	irisLabel.append(b)
	irisLabel.append(c)
	
	irisLabel = np.array(irisLabel)
	irisLabel = irisLabel.reshape(1,150)
	#print len(irisLabel)

	Kiris = gaussianKernel(0.001, irisData)

	reduce_idx = np.array([1,2,4,23, 56,79,91, 121, 137, 146])
	Kiris_reduce = Kiris[reduce_idx]
	
	irisLabel_reduce = (irisLabel[0][reduce_idx]).reshape(1,10)
	#print irisLabel_reduce.shape
	K_sir = KSIR(Kiris_reduce, irisLabel_reduce)
	np.savetxt("k_sir_sir.csv", K_sir, delimiter=",")
	result = np.dot(Kiris,K_sir)
	print Kiris.shape
	np.savetxt("k_sir.csv", result, delimiter=",")



