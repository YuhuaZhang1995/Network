import numpy as np
import math
import scipy.optimize as opt
import sys
import generators as gn

interactions={}
def gen_sample(alpha,theta,alpha_null,B,iter=100):
	#Cluster assignment
	pi_s=np.random.dirichlet(alpha_null)
	C_s1=np.random.multinomial(pi_s)
	C_s2=np.random.multinomial(pi_s)
	 
	#Fix the parameter based on the cluster assignment
	tmp_a1=alpha[C_s1]
	tmp_th1=theta[C_s1]
	tmp_a2=alpha[C_s2]
	tmp_th2=theta[C_s2]
	
	#generate the senders based on the DP
	if (interactions[C_s1].len()==0):
		sender