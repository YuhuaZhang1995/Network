import numpy as np
import math
from scipy.optimize import minimize
import sys

def llk(num_vertex,total_deg,k_deg,x):
	"""k_deg=a disctionary with key=degree, value=count of vertex"""
	"""num_vertex= number of vertex"""
	"""total_degree=total degree, 2*nrow"""
	"""x=[alpha,theta]"""
	alpha=x[0]
	theta=x[1]
	keys=np.array(list(dict.keys(k_deg)))
	values=np.array(list(dict.values(k_deg)))
	tmp=np.array(list(map(math.lgamma,(keys-alpha))))-math.lgamma(1-alpha)
	llk_=num_vertex*math.log(alpha)+math.lgamma(theta/alpha+num_vertex)-math.lgamma(theta/alpha)-math.lgamma(theta+total_deg)+math.lgamma(theta)+sum(np.multiply(values,tmp))
	return 0-llk_

def llk_der(num_vertex,total_deg,k_deg,x):
	"""The Jacobian required by L-BFGS-B algorithm"""
	alpha=x[0]
	theta=x[1]
	der=np.zeros_like(x)
	f1=lambda x: (-theta/alpha**2)/(theta/alpha+x)
	f2=lambda x: 1/(1-alpha+x)
	keys=np.array(list(dict.keys(k_deg)))
	values=np.array(list(dict.values(k_deg)))
	f3=lambda key: sum(f2(x) for x in range(key))
	tmp=np.array(list(map(f3,keys-1)))
	der[0]=0-(num_vertex/alpha+sum(f1(x) for x in range(num_vertex))-sum(np.multiply(values,tmp)))
	f4=lambda x: (1/alpha)/(theta/alpha+x)
	f5=lambda x: 1/(theta+x)
	der[1]=0-(sum(f4(x) for x in range(num_vertex))-sum(f5(x) for x in range(total_deg)))
	return der

def get_llkoptim(num_vertex,total_deg,k_deg,max_iter,x0):
	"""Get the minimal of llk"""
	"""Using L-BFGS-B algorithm"""
	f=lambda x: llk(num_vertex,total_deg,k_deg,x)
	f2=lambda x: llk_der(num_vertex,total_deg,k_deg,x)
	result=minimize(f,x0,method='L-BFGS-B',jac=f2,options={'maxiter':max_iter,'ftol':1e-5},bounds=((0.001,0.999),(0.001,100)))
	return result
	
k_deg={}
num_vertex=0
total_deg=0
x0=[0.5,1]
filename=sys.argv[1]
with open(filename) as infile:
	tmp_node=-99.9
	count=0
	header=0
	for line in infile:
		header=header+1
		curr_node=line.strip().split("\t")[0]
		freq=line.strip().split("\t")[3]
		if tmp_node!=curr_node:
			tmp_node=curr_node
			if header!=1:
				num_vertex=num_vertex+1
				if count in k_deg:
					k_deg[count]+=1
				else:
					if count!=1:
						k_deg[count]=1
				count=int(freq)
		else:
			count=count+int(freq)
		if header!=1:
			total_deg=total_deg+int(freq)

print(get_llkoptim(num_vertex,total_deg,k_deg,100,x0))



