import networkx as nx
import sys

#m -> Height of each branch
#d -> Max degree of each node

if len(sys.argv) > 2:
	n = int(sys.argv[1])
	d = int(sys.argv[2])
else:
	n = 22
	d = 3

G = nx.Graph()
G.add_nodes_from([i for i in range(n)])

G.add_edges_from([(0,i) for i in range(1,d+1)])

unused = [i for i in range(d+1,n)]

for i in range(1,n):
	for k in range(d-1):
		G.add_edge(i,unused.pop(0))
		if len(unused) == 0:
			break
	if len(unused) == 0:
		break

nx.write_adjlist(G, "large")