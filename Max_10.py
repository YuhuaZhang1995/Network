import numpy as np
import math
import scipy.optimize as opt
import sys
import matplotlib.pyplot as plt
import powerlaw

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
        result=opt.minimize(f,x0,method='L-BFGS-B',jac=f2,options={'maxiter':max_iter,'ftol':1e-5},bounds=((0.001,0.999),(0.001,100)))
        return result


k_deg={}
num_vertex=0
total_deg=0
filename=sys.argv[1]
x0=[0.5,1]
#nodes=[1506957, 1576132, 867962, 157003, 698501, 625896, 633055, 1440320, 1635368, 194796]
nodes=[648883, 1029464, 1498074, 1361181, 620603, 68030, 1506600, 1635368, 1354241, 1345822]
MLE={'1635368':1.965,'1506600':1.294,'1498074':1.571,'1361181':0.017,'1354241':1.437,'1345822':1.324,'1029464':1.095,'648883':1.743,'620603':1.06,'68030':1.191}
with open(filename) as infile:
	#count=1 #count the degree of vertex
	tmp_node=-99.9
	rec_node=-99.9
	remove_header=0
	count={}
	count1=0
	for line in infile:
		remove_header=remove_header+1
		curr_node=line.strip().split("\t")[0]
		rec_node=line.strip().split("\t")[1]
		freq=line.strip().split("\t")[3]
		#if not change the sender
		if remove_header>1:
			if int(curr_node) in nodes:
				tmp_node=curr_node
				#k_deg[int(rec_node)]=int(freq)
				if count1 in k_deg:
					k_deg[count1]+=1
				else:
					if count1!=1:
						k_deg[count1]=1
				count1+=int(freq)
				num_vertex+=1
				total_deg+=int(freq)
		#generate plots and initialize to 0
		if total_deg!=0:
			if not int(curr_node) in nodes:
				#fit the local E2 model
				print(tmp_node)
				print(get_llkoptim(num_vertex,total_deg,k_deg,100,x0))
				'''
				#fit the MLE model
				for i in k_deg.keys():
					if k_deg[i] in count.keys():
						count[k_deg[i]]+=1
					else:
						count[k_deg[i]]=1
				keys=np.array(list(dict.keys(count)))
				values=np.array(list(dict.values(count)))
				keys_log=np.array(list(map(math.log,(keys))))
				values_log=np.array(list(map(math.log,(values))))
				
				def distribution(x, alpha, beta,x0):
					return (x+x0)**(-alpha)*np.exp(-beta*x)
				fit = opt.curve_fit(distribution, keys, values ,maxfev=5000)
				print(str(tmp_node))
				print(fit[0])
				'''
				'''
				#generate plot
				plt.scatter(keys_log,values_log)
				plt.title('Sender '+str(tmp_node))
				plt.xlabel('log of degree')
				plt.ylabel('log of freq')
				plt.savefig(str(tmp_node)+'.png')
				plt.close()
				'''
				#reinitialize the value
				count={}
				k_deg={}
				num_vertex=0
				total_deg=0
				count1=0




