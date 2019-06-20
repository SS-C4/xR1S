from rumor_center import *
from itertools import *
import random

def unique_perm(array):
    return {p for p in permutations(array)}

def to_int(adj):
    tmp = [[] for i in range(len(adj))]
    for n,i in enumerate(adj):
        for m,j in enumerate(i):
            tmp[n].append(int(j))
    return tmp

#Estimator 1
def est_1(g1_num, g2_num, ov_num):
    normal_fact = (max(g1_num, g2_num) - 1)
    return (float( normal_fact * ov_num / (g1_num*g2_num - ov_num) ))

#Adjacency and labels for graph 1
g1 = nx.read_adjlist("g1_adj")
g1_attr = [i for i in range(g1.number_of_nodes())]

g1_attr = ["a"+str(i) for i in g1_attr]
g1_attr = {str(i) : {'label' : lab} for i,lab in enumerate(g1_attr)}

nx.set_node_attributes(g1, g1_attr)

#Adjacency and labels for graph 2
g2 = nx.read_adjlist("g2_adj")

########################################
#Stuff after the overlap has been set

def stuff_after_overlap(g2_at):
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

    #find denom
    denom = sum([j for (i,j) in vals_g1])*sum([j for (i,j) in vals_g2]) - num

    #ratio
    return (float(num/denom))

########################################
#g2_at -> mapping of g2 -> g1
#Set g2_at to the exact overlap required

x = [i for i in range(g2.number_of_nodes())]
g2_at = [-1 for i in range(g2.number_of_nodes())]

'''
#for randomised testing; ov -> size of overlap
ov = 3
for i in range(ov):
    r = random.randint(0,g2.number_of_nodes()-1)
    while x[r] in g2_at:
        r = random.randint(0,g2.number_of_nodes()-1)
    
    s = random.randint(0,g2.number_of_nodes()-1)
    while g2_at[s] != -1:
        s = random.randint(0,g2.number_of_nodes()-1)
    g2_at[s] = x[r]

stuff_after_overlap(g2_at)
'''

#for exhaustive average of all possible overlaps of given size -> ov

for ov in range(1,min(g1.number_of_nodes(),g2.number_of_nodes())+1):
    replace_ov = list(combinations(x,ov))

    array = []
    for cc in replace_ov:
        g2_at = list(cc)+g2_at[ov:]
        for per in list(unique_perm(g2_at)):
            array += [stuff_after_overlap(list(per))]   
    
    me = mean(array)
    es_1 = est_1(g1.number_of_nodes(),g2.number_of_nodes(),ov)
    div = float(es_1/me)  

    print ("Overlap size = " + str(ov), ", Mean ratio = " + str(me), ", Est_1 = " + str(es_1), ", Div = " + str(div))
