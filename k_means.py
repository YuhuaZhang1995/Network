import numpy as np
import math
from scipy.optimize import minimize
import sys
import random
from functools import reduce
import csv

k_deg={} #store the node id and the total edge counts
toss=np.random.uniform(0,1,1)[0]
#center1=random.randrange(1660555)
centers={}
k_mean=[]#store the centers
filename=sys.argv[1]
with open(filename) as infile:
	count=0 #count the degree of vertex
	tmp_node=-99.9
	remove_header=0
	Flag=0 #flag for center1
	for line in infile:
		remove_header=remove_header+1
		curr_node=line.strip().split("\t")[0]
		curr_rec_node=line.strip().split("\t")[1]
		freq=line.strip().split("\t")[2]
		#if change the sender, restart the loop
		if tmp_node!=curr_node or line=='':
			#check the header was not counted
			if remove_header>2:
				k_deg[int(tmp_node)]=np.sqrt(count) #store the norm of the vector
				#reinitialize the values
				if int(curr_node)/1660555>toss:
					Flag+=1
					if Flag==1:
						centers[int(curr_rec_node)]=int(freq)
						k_mean.append(int(curr_node))
					if Flag==2:
						centers={k: v/np.sqrt(count) for k,v in centers.items()}
				count=int(freq)*int(freq)
			tmp_node=curr_node

		#if not change the sender
		else:
			#print(tmp_node)
			count+=int(freq)*int(freq)
			if Flag==1:
				centers[int(curr_rec_node)]=int(freq)
infile.close()
#print(k_deg)

#calculate the distance psi(X)
distance={} #store the distance of current to the random selected center
dist_sum=0 #total sum of the distance
with open(filename) as infile2:
	tmp_node=-99.9
	remove_header=0
	norm=1
	array1=[] #vector of current node
	array2=[] #vector of the centered node
	tmp_deg={} #store the current node receivers
	for line in infile2:
		remove_header=remove_header+1
		curr_node=line.strip().split("\t")[0]
		curr_rec_node=line.strip().split("\t")[1]
		freq=line.strip().split("\t")[2]
		#change the node, calculate the norm
		if tmp_node!=curr_node or line=='':
			if remove_header>2:
				norm=k_deg[int(tmp_node)]#vector norm
				tmp_deg={k: v/norm for k,v in tmp_deg.items()}
				alldict=[tmp_deg,centers]
				allkey = list(reduce(set.union, map(set, map(dict.keys, alldict))))#the union of all keys(receivers)
				for i in allkey:
					if (int(i) in tmp_deg.keys()) and (int(i) in centers.keys()):
						array1.append(tmp_deg[int(i)])
						array2.append(centers[int(i)])
					elif (int(i) in tmp_deg.keys()) and (not int(i) in centers.keys()):
						array1.append(tmp_deg[int(i)])
						array2.append(0)
					elif (not int(i) in tmp_deg.keys()) and (int(i) in centers.keys()):
						array1.append(0)
						array2.append(centers[int(i)])
					else:
						array1.append(0)
						array2.append(0)
				arr1=np.array(array1)
				arr2=np.array(array2)
				dist_sum+=(np.linalg.norm(arr1-arr2))**2#the distance of current node with the random selected center
				distance[int(tmp_node)]=(np.linalg.norm(arr1-arr2))**2
				#reinitialization
				tmp_deg={}
				tmp_deg[int(curr_rec_node)]=int(freq)
				array1=[]
				array2=[]
			tmp_node=curr_node
		#not change the node, update info
		else:
			tmp_deg[int(curr_rec_node)]=int(freq)
infile2.close()
#print(distance)

#sample the new centers, we have distance, k_deg, and dist_sum
l=1 #oversampling factor
distance={k: v/dist_sum for k,v in distance.items()}#normalize the distence
for i in range(int(math.log(dist_sum))):
	index=np.random.choice(len(list(distance.keys())),l,p=list(distance.values()),replace=False)
	k_mean.extend(list(np.array(list(distance.keys()))[index]))
k_mean=list(sorted(set(k_mean)))
#print(k_mean)
#get the vectors for the sampled centers
k_centers={}
with open(filename) as infile3:
	remove_header=0
	tmp_node=-99.9
	tmp_dict={}
	count=0
	for line in infile3:
		remove_header=remove_header+1
		curr_node=line.strip().split("\t")[0]
		curr_rec_node=line.strip().split("\t")[1]
		freq=line.strip().split("\t")[2]
		if tmp_node!=curr_node or line=='':
			if remove_header>2:
				#check if curr_node is the centers
				if int(tmp_node) in k_mean:
					count=np.sqrt(count)
					tmp_dict={k: v/count for k,v in tmp_dict.items()}
					k_centers[int(tmp_node)]=tmp_dict
				tmp_dict={}
				tmp_dict[int(curr_rec_node)]=int(freq)
				count=int(freq)*int(freq)
			tmp_node=curr_node
		else:
			tmp_dict[int(curr_rec_node)]=int(freq)
			count+=int(freq)*int(freq)
infile3.close()
#print(k_centers)

#cluster the resting nodes given the centers
cluster={} #store the information of the cluster
with open(filename) as infile4:
	tmp_node=-99.9
	remove_header=0
	norm=1
	array1=[] #vector of current node
	array2=[] #vector of the centered node
	tmp_deg={} #store the current node receivers
	tmp_len=99.9
	#tmp_deg2={} #store the tmp dictionary of the centers
	for line in infile4:
		remove_header=remove_header+1
		curr_node=line.strip().split("\t")[0]
		curr_rec_node=line.strip().split("\t")[1]
		freq=line.strip().split("\t")[2]
		#change the node, calculate the norm
		if tmp_node!=curr_node or line=='':
			if remove_header>2:
				norm=k_deg[int(tmp_node)]#vector norm
				tmp_deg={k: v/norm for k,v in tmp_deg.items()}
				#loop over k centers
				for j in k_centers.keys():
					alldict=[tmp_deg,k_centers[j]]
					allkey = list(reduce(set.union, map(set, map(dict.keys, alldict))))#the union of all keys(receivers)
					for i in allkey:
						if (int(i) in tmp_deg.keys()) and (int(i) in k_centers[j].keys()):
							array1.append(tmp_deg[int(i)])
							array2.append(k_centers[j][int(i)])
						elif (int(i) in tmp_deg.keys()) and (not int(i) in k_centers[j].keys()):
							array1.append(tmp_deg[int(i)])
							array2.append(0)
						elif (not int(i) in tmp_deg.keys()) and (int(i) in k_centers[j].keys()):
							array1.append(0)
							array2.append(k_centers[j][int(i)])
						else:
							array1.append(0)
							array2.append(0)
					arr1=np.array(array1)
					arr2=np.array(array2)
					if tmp_len>(np.linalg.norm(arr1-arr2))**2:
						cluster[int(tmp_node)]=j
						tmp_len=(np.linalg.norm(arr1-arr2))**2
					array1=[]
					array2=[]
				#reinitialization
				tmp_deg={}
				tmp_deg[int(curr_rec_node)]=int(freq)
				tmp_len=99.9
			tmp_node=curr_node
		#not change the node, update info
		else:
			tmp_deg[int(curr_rec_node)]=int(freq)
infile4.close()
#print(cluster)

w = csv.writer(open("KR_cluster.txt", "w+"))
for key, val in cluster.items():
    w.writerow([key, val])





