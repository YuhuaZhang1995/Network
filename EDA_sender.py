import numpy as np
import math
import scipy.optimize as opt
import sys
import matplotlib.pyplot as plt
import powerlaw
import operator

k_deg={}
num_vertex=0
total_deg=0
filename=sys.argv[1]
with open(filename) as infile:
	#count=1 #count the degree of vertex
	tmp_node=-99.9
	#rec_node=-99.9
	remove_header=0
	for line in infile:
		remove_header=remove_header+1
		curr_node=line.strip().split("\t")[0]
		freq=line.strip().split("\t")[3]
		#if change the sender, restart the loop
		if tmp_node!=curr_node:
			tmp_node=curr_node
			#check the header was not counted
			if remove_header!=1:
				k_deg[int(tmp_node)]=int(freq)
				
		#if not change the sender
		else:
			k_deg[int(tmp_node)]+=int(freq)

'''
count={}
for i in k_deg.keys():
	if k_deg[i] in count.keys():
		count[k_deg[i]]+=1
	else:
		count[k_deg[i]]=1


keys=np.array(list(dict.keys(count)))
values=np.array(list(dict.values(count)))
keys_log=np.array(list(map(math.log,(keys))))
values_log=np.array(list(map(math.log,(values))))
#print(count)
plt.scatter(keys_log,values_log)
plt.title('Outdegree of Node 1')
plt.xlabel('log of degree')
plt.ylabel('log of freq')
#plt.savefig('JP_outdegree.png')


#Get the powerlaw estimates

y_data=values/sum(values)
#print(y_data)
def distribution(x, alpha, beta, x0):
	return (x + x0)**alpha * np.exp(-beta *x)
fit = opt.curve_fit(distribution, keys, y_data, maxfev=5000)
print(fit[0])
'''
'''
data = np.array(list(dict.values(k_deg))) # data can be list or numpy array
results = powerlaw.Fit(data)
print(results.power_law.alpha)
'''

#get the 10 nodes with largest outdegree
print(sorted(k_deg, key=(lambda key:k_deg[key]), reverse=True)[:10])









