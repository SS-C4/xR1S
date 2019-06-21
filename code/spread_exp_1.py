from __future__ import division
import matplotlib.pyplot as plt
from pylab import *
import random as rnd
import networkx as nx
from rumor_center import *
from estimators import *


#Restrict source to set R -> The first R nodes closest to the center
R = 5

#list_of_source is the set of nodes which can be possible sources
def generate_source(adjacency, list_of_sources):
    num_nodes = len(adjacency)
    while True:
        source = rnd.choice(list_of_sources)
        if len(adjacency[source]) > 0:
            break
    return source

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

#Stop after k infections in total (including source)
k = 30

if k > G.number_of_nodes():
	k = G.number_of_nodes()

#1 & 1_1 are exp_1 
#1 & 2 are exp_2
#Less than threshold = diff
#More than threshold = same

#Run experiments
N = 100

#positive = same
#negative = diff
tpr_1 = [] 
fpr_1 = []
tpr_2 = []
fpr_2 = []

for threshold in np.linspace(0,1,10):
	FP1 = FN1 = TP1 = TN1 = 0
	FP2 = FN2 = TP2 = TN2 = 0
	
	for i in range(N):
		#choose between exp 1 or exp 2
		choice = rnd.randint(1,2)

		if choice == 1:
			source_1 = generate_source(to_int(nx_graph_to_adj(G)), liss)

			adj1, inf_nodes_1 = si_model_rumor_spreading(source_1, to_int(nx_graph_to_adj(G)), k)
			adj1_1, inf_nodes_1_1 = si_model_rumor_spreading(source_1, to_int(nx_graph_to_adj(G)), k)

			s1 = G.subgraph([str(i) for i in inf_nodes_1])
			s1_1 = G.subgraph([str(i) for i in inf_nodes_1_1])
			
			op1 = est_1(G, s1, s1_1)
			op2 = est_2(G, s1, s1_1)

			#2 cases
			if op1 > threshold:
				FN1 += 1
			else:
				TP1 += 1

			if op2 > threshold:
				FN2 += 1
			else:
				TP2 += 1


		else:
			source_1 = generate_source(to_int(nx_graph_to_adj(G)), liss)
			source_2 = generate_source(to_int(nx_graph_to_adj(G)), liss)

			adj1, inf_nodes_1 = si_model_rumor_spreading(source_1, to_int(nx_graph_to_adj(G)), k)
			adj2, inf_nodes_2 = si_model_rumor_spreading(source_2, to_int(nx_graph_to_adj(G)), k)

			s1 = G.subgraph([str(i) for i in inf_nodes_1])
			s2 = G.subgraph([str(i) for i in inf_nodes_2])

			op1 = est_1(G, s1, s2)
			op2 = est_2(G, s1, s2)

			#2 cases
			if op1 > threshold:
				TN1 += 1
			else:
				FP1 += 1

			if op2 > threshold:
				TN2 += 1
			else:
				FP2 += 1

	tpr_1 += [TP1/(TP1+FN1)]
	fpr_1 += [FP1/(TN1+FP1)]

	tpr_2 += [TP2/(TP2+FN2)]
	fpr_2 += [FP2/(TN2+FP2)]

plt.plot([0,1], [0,1], 'b-')
plt.plot(tpr_1, fpr_1, 'r-') 
plt.plot(tpr_2, fpr_2, 'y--')
plt.axis([0,1,0,1])
plt.show()