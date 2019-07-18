import matplotlib.pyplot as plt
from matplotlib import rcParams
import random as rnd
import networkx as nx
from estimators import *
import pyximport; pyximport.install()
from numpy import linspace, cumsum, unique
import time
import os

rcParams['figure.figsize'] = 12, 12 

t0 = time.time()
#Restrict source to set R -> The first R nodes closest to the center
R = 30
#Stop after k infections in total (including source)
k = 201
#Number of estimators
n_est = 3
#Run experiments
N = 5000
#Number of divisions of [0,TT]
n_div = 801
#Spread rate $\lambda$
l = 1
#Time_max for taking snapshot (Do not set above 5-10)
T_max = 20

#Maximum threshold required (for ML) (Should be bounded by R / (sqrt(pi*k/2) - 1) for a line)
#Needs to be much higher for higher degree of tree
TT = 10

# #Gives size of snapshot after waiting for T_max
# def snap_size(deg, T_max):
# 	T = 0
# 	k = 1
# 	while T <= T_max:
# 		T += np.random.exponential(float(1/(l*deg + (k-1)*(deg-2))))
# 		k += 1
# 	return k

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

#Sizes of snapshots
m = k
n = k

#1 & 1_1 are exp_1
#1 & 2 are exp_2
#positive = same = Should be more than threshold
#negative = diff = Should be less than threshold
tpr = [[] for i in range(n_est)]
fpr = [[] for i in range(n_est)]

op = [0 for i in range(n_est)]

FP = [n_est*[0] for _ in range(n_div)]
TP = [n_est*[0] for _ in range(n_div)]
FN = [n_est*[0] for _ in range(n_div)]
TN = [n_est*[0] for _ in range(n_div)]

#Populate array with random choices (1,2)
rchoice = [rnd.choice([1,2]) for _ in range(N)]

#Run exp N times
for i in range(N):
	#choose between exp 1 or exp 2
	choice = rchoice[i]
	if choice == 1:
		source_1 = int(rnd.choice(liss))

		inf_nodes_1 = si_model_rumor_spreading(source_1, to_int(nx_graph_to_adj(G)), m)
		inf_nodes_1_1 = si_model_rumor_spreading(source_1, to_int(nx_graph_to_adj(G)), n)

		s1 = G.subgraph([str(i) for i in inf_nodes_1])
		s1_1 = G.subgraph([str(i) for i in inf_nodes_1_1])

		op[0] = est_2(s1, s1_1)
		op[1] = est_3(R, s1, s1_1)
		op[2] = est_4(G, s1, s1_1)

		for n_thr, threshold in enumerate(linspace(-0.01,TT,n_div)):
			for j in range(n_est):
				if op[j] > threshold:
					TP[n_thr][j] += 1
				else:
					FN[n_thr][j] += 1

	else:
		source_1 = int(rnd.choice(liss))
		source_2 = int(rnd.choice(liss))
		while source_2 == source_1:
			source_2 = int(rnd.choice(liss))

		inf_nodes_1 = si_model_rumor_spreading(source_1, to_int(nx_graph_to_adj(G)), m)
		inf_nodes_2 = si_model_rumor_spreading(source_2, to_int(nx_graph_to_adj(G)), n)

		s1 = G.subgraph([str(i) for i in inf_nodes_1])
		s2 = G.subgraph([str(i) for i in inf_nodes_2])

		op[0] = est_2(s1, s2)
		op[1] = est_3(R, s1, s2)
		op[2] = est_4(G, s1, s2)

		for n_thr, threshold in enumerate(linspace(-0.01,TT,n_div)):
			for j in range(n_est):
				if op[j] > threshold:
					FP[n_thr][j] += 1
				else:
					TN[n_thr][j] += 1

for n_thr, threshold in enumerate(linspace(-0.01,TT,n_div)):
	for i in range(n_est):
		tpr[i] += [TP[n_thr][i]/(TP[n_thr][i]+FN[n_thr][i])]
		fpr[i] += [FP[n_thr][i]/(TN[n_thr][i]+FP[n_thr][i])]

print (time.time() - t0)

plt.plot([0,1], [0,1], 'b--')

colors = ['g','r','c','m','y','k']
markers = ['v-','--','o-','^-','-','-']

for i in range(n_est):
	plt.plot(fpr[i], tpr[i], ''.join(colors[i] + markers[i]))

plt.axis([-0.1,1.1,-0.1,1.1])
plt.text(0.7, 0.4, "R: "+str(R) + "\nn_div: "+str(n_div) + "\nN: "+str(N) + "\nk: "+str(k) + "\ndeg: "+str(deg)\
	 + "\n(m,n): ("+str(m)+","+str(n) + ")\n\n\n\nML est is the dotted line")
plt.savefig("../../tmp/"+str(R)+"_"+str(N)+"_"+str(k)+"_"+str(deg))

#Remove if using on a different system
os.system("../../copy_to_down.sh")