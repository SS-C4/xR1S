from __future__ import division
import matplotlib.pyplot as plt
from pylab import *
import random as rnd
import networkx as nx
from rumor_center import *
from estimators import *


#Restrict source to set R -> The first R nodes closest to the center
R = 20
#Stop after k infections in total (including source)
k = 100
#Number of estimators
n_est = 5
#Run experiments
N = 4000
#Number of divisions of [0,1] for threshold values
n_div = 100

def si_model_rumor_spreading(source, adjacency, N):
    infctn_pattern = [-1]*N;
    who_infected = [[] for i in range(N)]

    # adding the source node to the list of infected nodes
    infctn_pattern[0] = source
    susceptible_nodes = adjacency[source]
    susceptible_indices = [0]*len(susceptible_nodes)

    for i in range(1,N):

        # infect the first node
        infctd_node_idx = rnd.randrange(0,len(susceptible_nodes),1)
        infctn_pattern[i] = susceptible_nodes[infctd_node_idx]
        who_infected[i] = [susceptible_indices[infctd_node_idx]]
        who_infected[susceptible_indices[infctd_node_idx]].append(i)

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

    return who_infected, infctn_pattern

G = nx.read_adjlist("large")

liss = [0]
z_nei = [int(i) for i in G.neighbors('0')]

for i in range(1, R):
	if i % 3 == 1:
		liss += [i]
	elif i % 3 == 2:
		liss += [z_nei[1] + i - 2]
	else:
		liss += [z_nei[2] + i - 3]

if k > G.number_of_nodes():
	k = G.number_of_nodes()

#1 & 1_1 are exp_1
#1 & 2 are exp_2
#Less than threshold = diff
#More than threshold = same
#positive = same = More than threshold
#negative = diff = Less than threshold
tpr = [[] for i in range(n_est)]
fpr = [[] for i in range(n_est)]

for threshold in np.linspace(0,1,n_div):
	FP = [0 for i in range(n_est)]
	TP = [0 for i in range(n_est)]
	FN = [0 for i in range(n_est)]
	TN = [0 for i in range(n_est)]

	op = [0 for i in range(n_est)]

	for i in range(N):
		#choose between exp 1 or exp 2
		choice = rnd.randint(1,2)
		if choice == 1:
			source_1 = int(rnd.choice(liss))

			adj1, inf_nodes_1 = si_model_rumor_spreading(source_1, to_int(nx_graph_to_adj(G)), k)
			adj1_1, inf_nodes_1_1 = si_model_rumor_spreading(source_1, to_int(nx_graph_to_adj(G)), k)

			s1 = G.subgraph([str(i) for i in inf_nodes_1])
			s1_1 = G.subgraph([str(i) for i in inf_nodes_1_1])

			op[0] = est_0(G, s1, s1_1)
			op[1] = est_1(G, s1, s1_1)
			op[2] = est_2(G, s1, s1_1)
			op[3] = est_3(G, s1, s1_1)
			op[4] = est_4(G, s1, s1_1)

			for i in range(n_est):
				if op[i] > threshold:
					TP[i] += 1
				elif op[i] < threshold:
					FN[i] += 1

		else:
			source_1 = int(rnd.choice(liss))
			source_2 = int(rnd.choice(liss))

			adj1, inf_nodes_1 = si_model_rumor_spreading(source_1, to_int(nx_graph_to_adj(G)), k)
			adj2, inf_nodes_2 = si_model_rumor_spreading(source_2, to_int(nx_graph_to_adj(G)), k)

			s1 = G.subgraph([str(i) for i in inf_nodes_1])
			s2 = G.subgraph([str(i) for i in inf_nodes_2])

			op[0] = est_0(G, s1, s2)
			op[1] = est_1(G, s1, s2)
			op[2] = est_2(G, s1, s2)
			op[3] = est_3(G, s1, s2)
			op[4] = est_4(G, s1, s2)

			for i in range(n_est):
				if op[i] > threshold:
					FP[i] += 1
				elif op[i] < threshold:
					TN[i] += 1

	for i in range(n_est):
		tpr[i] += [TP[i]/(TP[i]+FN[i])]
		fpr[i] += [FP[i]/(TN[i]+FP[i])]

plt.plot([0,1], [0,1], 'b--')

colors = ['g','r','c','m','y','k']
markers = ['o','v','^','<','>','*']

for i in range(n_est):
	plt.plot(fpr[i], tpr[i], ''.join(colors[i] + markers[i]))

plt.axis([0,1,0,1])
plt.text(0.7, 0.4, "R: "+str(R) + "\nn_div: "+str(n_div) + "\nN: "+str(N) + "\nk: "+str(k))
plt.show()
