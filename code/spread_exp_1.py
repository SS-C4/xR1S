from __future__ import division
import matplotlib.pyplot as plt
import random as rnd
import networkx as nx
from estimators import *
import numpy as np
import pyximport; pyximport.install()
import time

t0 = time.time()
#Restrict source to set R -> The first R nodes closest to the center
R = 2
#Stop after k infections in total (including source)
k = 3
#Number of estimators
n_est = 5
#Run experiments
N = 5000
#Number of divisions of [0,3] for threshold values
n_div = 297

def si_model_rumor_spreading(source, adjacency, N):
	infctn_pattern = [-1]*N;

	# adding the source node to the list of infected nodes
	infctn_pattern[0] = source
	susceptible_nodes = adjacency[source]
	susceptible_indices = [0]*len(susceptible_nodes)

	for i in range(1,N):

		# infect the first node
		infctd_node_idx = rnd.randrange(0,len(susceptible_nodes),1)
		infctn_pattern[i] = susceptible_nodes[infctd_node_idx]

		# updating susceptible_nodes and susceptible_indices
		susceptible_indices = [susceptible_indices[j] for j in range(len(susceptible_nodes)) if susceptible_nodes[j]
							   != susceptible_nodes[infctd_node_idx]]
		susceptible_nodes = [susceptible_nodes[j] for j in range(len(susceptible_nodes)) if susceptible_nodes[j]
							 != susceptible_nodes[infctd_node_idx]]
		infctd_nodes = set(infctn_pattern[:i+1])
		new_susceptible_nodes = set(adjacency[infctn_pattern[i]])
		new_susceptible_nodes = list(new_susceptible_nodes.difference(infctd_nodes))
		susceptible_nodes  = susceptible_nodes  + new_susceptible_nodes
		susceptible_indices = susceptible_indices + [i]*len(new_susceptible_nodes)

	return infctn_pattern

G = nx.read_adjlist("large")

#Degree of underlying tree
deg = len(G.edges('0'))

liss = [i for i in range(R)]

if k > G.number_of_nodes():
	k = G.number_of_nodes()

#1 & 1_1 are exp_1
#1 & 2 are exp_2
#positive = same = Should be more than threshold
#negative = diff = Should be less than threshold
tpr = [[] for i in range(n_est)]
fpr = [[] for i in range(n_est)]

op = [0 for i in range(n_est)]

FP = np.zeros((n_div,n_est), dtype = int)
TP = np.zeros((n_div,n_est), dtype = int)
FN = np.zeros((n_div,n_est), dtype = int)
TN = np.zeros((n_div,n_est), dtype = int)

#Populate array with random choices (1,2)
rchoice = np.random.randint(1,3,N)
print (np.count_nonzero(rchoice == 1))

#Run exp N times
for i in range(N):
	#choose between exp 1 or exp 2
	choice = rchoice[i]
	if choice == 1:
		source_1 = int(rnd.choice(liss))

		inf_nodes_1 = si_model_rumor_spreading(source_1, to_int(nx_graph_to_adj(G)), k)
		inf_nodes_1_1 = si_model_rumor_spreading(source_1, to_int(nx_graph_to_adj(G)), k)

		s1 = G.subgraph([str(i) for i in inf_nodes_1])
		s1_1 = G.subgraph([str(i) for i in inf_nodes_1_1])

		op[0] = est_0(s1, s1_1)
		op[1] = est_1(s1, s1_1)
		op[2] = est_2(s1, s1_1)
		op[3] = est_3(R, s1, s1_1)
		op[4] = est_4(s1, s1_1)

		for n_thr, threshold in enumerate(np.linspace(0,3,n_div)):
			for j in range(n_est):
				if op[j] >= threshold:
					TP[n_thr][j] += 1
				else:
					FN[n_thr][j] += 1

	else:
		source_1 = int(rnd.choice(liss))
		source_2 = int(rnd.choice(liss))

		inf_nodes_1 = si_model_rumor_spreading(source_1, to_int(nx_graph_to_adj(G)), k)
		inf_nodes_2 = si_model_rumor_spreading(source_2, to_int(nx_graph_to_adj(G)), k)

		s1 = G.subgraph([str(i) for i in inf_nodes_1])
		s2 = G.subgraph([str(i) for i in inf_nodes_2])

		op[0] = est_0(s1, s2)
		op[1] = est_1(s1, s2)
		op[2] = est_2(s1, s2)
		op[3] = est_3(R, s1, s2)
		op[4] = est_4(s1, s2)

		for n_thr, threshold in enumerate(np.linspace(0,3,n_div)):
			for j in range(n_est):
				if op[j] >= threshold:
					FP[n_thr][j] += 1
				else:
					TN[n_thr][j] += 1

for n_thr, threshold in enumerate(np.linspace(0,3,n_div)):
	for i in range(n_est):
		tpr[i] += [TP[n_thr][i]/(TP[n_thr][i]+FN[n_thr][i])]
		fpr[i] += [FP[n_thr][i]/(TN[n_thr][i]+FP[n_thr][i])]

print (time.time() - t0)

plt.plot([0,1], [0,1], 'b--')

colors = ['g','r','c','m','y','k']
markers = ['-','-','v-','^--','-','-']

for i in range(n_est):
	plt.plot(fpr[i], tpr[i], ''.join(colors[i] + markers[i]))

plt.axis([0,1,0,1])
plt.text(0.7, 0.4, "R: "+str(R) + "\nn_div: "+str(n_div) + "\nN: "+str(N) + "\nk: "+str(k) + "\ndeg: "+str(deg)\
	 +"\n\n\n\nML est is purple")
plt.savefig("../../tmp/"+str(R)+"_"+str(n_div)+"_"+str(N)+"_"+str(k)+"_"+str(deg))