#!/usr/bin/python

import math

def read_file(input_file):
	'''Reading the data from the file into data array inidicating the clusters, where the index of the array indicates the index of the daata'''
	csv_file = open(input_file, 'r')
	data = []
	for r in csv_file:
		r = r.strip()
		data.append(r.split(' ')[1])
		#data.append([float(i) for i in r.split(' ')])
	csv_file.close()
	return data

def cluster_probability(cluster):
	cluster_sum=[]
	n = float(len(cluster))
	cluster_names = list(set(cluster))
	for index,cluster_name in enumerate(cluster_names):
		cluster_sum.append(0)
		for i in cluster:
			if(cluster_name==i):
				cluster_sum[index]+=1
	cluster_prob = [i/n for i in cluster_sum]
	return cluster_prob	

def entropy(cluster):
	cluster_prob = cluster_probability(cluster)
	entropy = 0
	for i in cluster_prob:
		entropy+=i*math.log(i,2)
	return entropy*(-1)		
	
def mutual_information(cluster, truth):
	n = float(len(cluster))
	r = float(len(truth))
	pc = cluster_probability(cluster)
	pt = cluster_probability(truth)

	sc = list(set(cluster)) #name of the clusters
	st = list(set(truth)) #name of the clusters in ground truth
	
	#declare empty array to store p_ij
	p_matrix = [[0 for x in range(len(sc))] for y in range(len(st))]
 
	for i in range(len(truth)):
		p_matrix[st.index(truth[i])][sc.index(cluster[i])] += 1
	mutual_info = 0
	for i in range(len(st)):
		for j in range(len(sc)):
			joint_p = (p_matrix[i][j]/(n))
			if(joint_p != 0):
				mutual_info +=  joint_p*(math.log(joint_p/float(pc[j]*pt[i]),2))
	return mutual_info

def nmi(cluster,truth):
	hc = entropy(cluster)
	ht = entropy(truth)
	mutual_info = mutual_information(cluster,truth)
	return 2*mutual_info/(hc+ht)

def jaccard_coefficient(cluster, truth):
	n = float(len(cluster))
	r = float(len(truth))
	pc = cluster_probability(cluster)
	pt = cluster_probability(truth)

	sc = list(set(cluster)) #name of the clusters
	st = list(set(truth)) #name of the clusters in ground truth
	
	#declare empty array to store p_ij
	p_matrix = [[0 for x in range(len(sc))] for y in range(len(st))]
 
	for i in range(len(truth)):
		p_matrix[st.index(truth[i])][sc.index(cluster[i])] += 1
	mutual_info = 0
	
	#calculate tp
	tp = 0
	for i in range(len(st)):
		for j in range(len(sc)):
			n_ij = (p_matrix[i][j])
			tp += (n_ij*(n_ij - 1))/2

	#calculate fn
	pt = cluster_probability(truth)
	temp = 0
	for i in range(len(pt)):
		mi = pt[i]*n
		temp += (mi*(mi-1))/2
	fn = temp - tp

	#calculate fn
	pc = cluster_probability(cluster)
	total_positives = 0
	for i in range(len(pc)):
		mi = pc[i]*n
		total_positives += (mi*(mi-1))/2
	fp = total_positives - tp
		
	
	return tp/(tp+fn+fp)
	
truth = read_file('partitions.txt')
c1 = read_file('clustering_1.txt')
c2 = read_file('clustering_2.txt')
c3 = read_file('clustering_3.txt')
c4 = read_file('clustering_4.txt')
c5 = read_file('clustering_5.txt')

print nmi(c1, truth), jaccard_coefficient(c1, truth)
print nmi(c2, truth), jaccard_coefficient(c2, truth)
print nmi(c3, truth), jaccard_coefficient(c3, truth)
print nmi(c4, truth), jaccard_coefficient(c4, truth)
print nmi(c5, truth), jaccard_coefficient(c5, truth)

