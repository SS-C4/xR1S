from rumor_center import *
import random

def to_int(adj):
    tmp = [[] for i in range(len(adj))]
    for n,i in enumerate(adj):
        for m,j in enumerate(i):
            tmp[n].append(int(j))
    return tmp

#Adjacency and labels for graph 1
g1 = nx.read_adjlist("g1_adj")
g1_attr = [i for i in range(g1.number_of_nodes())]

g1_attr = ["a"+str(i) for i in g1_attr]
g1_attr = {str(i) : {'label' : lab} for i,lab in enumerate(g1_attr)}

nx.set_node_attributes(g1, g1_attr)

#Adjacency and labels for graph 2
g2 = nx.read_adjlist("g2_adj")

########################################
#mapping of g2 -> g1

x = [i for i in range(6)]
g2_at = [111 for i in range(6)]

ov = 3
for i in range(ov):
    r = random.randint(0,5)
    while x[r] in g2_at:
        r = random.randint(0,5)
    
    s = random.randint(0,5)
    while g2_at[s] != 111:
        s = random.randint(0,5)
    g2_at[s] = x[r]

print (g2_at)

########################################

g2_attr = ["a"+str(i) for i in g2_at]
g2_attr = {str(i) : {'label' : lab} for i,lab in enumerate(g2_attr)}

nx.set_node_attributes(g2, g2_attr)

#overlap -> true if labels are the same
#overlap is in terms of g1.nodes()
overlap = []
for i in g1.nodes():
    for j in g2.nodes():
        if g1.nodes[i]['label'] == g2.nodes[j]['label']:
            overlap += [i]
            break

#check if g1 and g2 are trees, if not, convert them to their BFS trees wrt node and find the max

if nx.is_tree(g1) and nx.is_tree(g2):    
    #find rumor centers and RC values for all nodes
    loc_1 = rumor_center(to_int(nx_graph_to_adj(g1)))
    vals_g1 = RC_values(to_int(nx_graph_to_adj(g1)), loc_1)

    vals_g1 = [(str(i),j) for (i,j) in vals_g1] 

    loc_2 = rumor_center(to_int(nx_graph_to_adj(g2)))
    vals_g2 = RC_values(to_int(nx_graph_to_adj(g2)), loc_2)

    vals_g2 = [(str(i),j) for (i,j) in vals_g2]
else:
    vals_g1 = [0 for i in range(g1.number_of_nodes())]
    for i in g1.nodes():
        h = (nx.bfs_tree(g1, i)).to_undirected()

        loc = rumor_center(to_int(nx_graph_to_adj(h)))
        tmpvals = RC_values(to_int(nx_graph_to_adj(h)), loc)
        vals_g1[int(i)] = tmpvals[int(i)]

    vals_g2 = [0 for i in range(g2.number_of_nodes())]
    for i in g2.nodes():
        h = (nx.bfs_tree(g2, i)).to_undirected()
        
        loc = rumor_center(to_int(nx_graph_to_adj(h)))
        tmpvals = RC_values(to_int(nx_graph_to_adj(h)), loc)
        vals_g2[int(i)] = tmpvals[int(i)]

    vals_g1 = [(str(i),j) for (i,j) in vals_g1] 
    vals_g2 = [(str(i),j) for (i,j) in vals_g2] 

#find num
num = 0
for i in overlap:
    num += vals_g1[int(i)][1] * vals_g2[g2_at.index(int(i))][1]
print(num)

#find denom
denom = sum([j for (i,j) in vals_g1])*sum([j for (i,j) in vals_g2]) - num
print(denom)

#ratio
print(float(num/denom))



