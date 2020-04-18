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
		s1=1
	else:
		p=interctions[C_s1]/sum(interactions[C_s1])
		s1=sample(interactions[C_s1],p)
		if !s1 in interactions[C_s1]:
			interactions[C_s1].extend(s1:1) #change from interactions to tmp interactions
		else:
			interactions[C_s1][s1]+=1
	if (interactions[C_s2].len()==0):
		s2=1
	else:
		p=interctions[C_s2]/sum(interactions[C_s2])
		s2=sample((interactions[C_s2],interaction[C_s2]+1),p)
		if !s2 in interactions[C_s2]:
			interactions[C_s2].extend(s2:1)
		else:
			interactions[C_s2][s2]+=1
	
	#Given the cluster and the sender, decide whether to keep the sender in the file
	Flag=sample from Bernoulli(C_s1*B*C_s2)
	if Flag==1:
		if s1 in interactions:
			interactions[C_s1][s1]+=1
		else:
			interactions[C_s1].extend(s1)
		if s2 in interactions:
			interactions[C_s2][s2]+=1
		else:
			interactions[C_s2].extend(s2)



