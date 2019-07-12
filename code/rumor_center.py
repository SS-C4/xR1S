from operator import mul
from functools import reduce
from math import factorial
import networkx as nx

# def generate_source(adjacency):
#     num_nodes = len(adjacency)
#     while True:
#         source = rnd.randint(0,num_nodes-1)
#         if len(adjacency[source]) > 0:
#             break
#     return source
    
def rumor_centrality_up(up_messages, who_infected, calling_node, called_node):
    if called_node == calling_node:
        for i in who_infected[called_node]:
                up_messages = rumor_centrality_up(up_messages, who_infected, called_node, i)
    elif len(who_infected[called_node]) == 1:   # leaf node
        up_messages[calling_node] += 1 # check
    else:
        for i in who_infected[called_node]:
            if i != calling_node:
                up_messages = rumor_centrality_up(up_messages, who_infected, called_node, i)
        up_messages[calling_node] += up_messages[called_node]
    return up_messages

def rumor_centrality_down(down_messages, up_messages, who_infected, calling_node, called_node):
    if called_node == calling_node:
        for i in who_infected[called_node]:
            down_messages = rumor_centrality_down(down_messages, up_messages, who_infected, called_node, i)   
    else:
        down_messages[called_node] = (down_messages[calling_node][0]*up_messages[called_node],
                                        (len(who_infected)-up_messages[called_node])*down_messages[calling_node][1])
        for i in who_infected[called_node]:
            if i != calling_node:
                down_messages = rumor_centrality_down(down_messages, up_messages, who_infected, called_node, i)
    return down_messages 


def rumor_center(who_infected):
    # computes the estimate of the source based on rumor centrality
    initial_node = 0       # can use arbitrary initial index
    
    up_messages = [1]*len(who_infected) 
    down_messages = [(1,1)]*len(who_infected)

    up_messages = rumor_centrality_up(up_messages,who_infected,initial_node,initial_node)
    down_messages = rumor_centrality_down(down_messages,up_messages,who_infected,initial_node,initial_node)    
    
    max_down = max([float(i/j) for (i,j) in down_messages])
    max_down_ind = [i for i, (j,k) in enumerate(down_messages) if float(j/k) == max_down]

    #To break ties at random
    #broken_tie = max_down_ind[randrange(0,len(max_down_ind),1)]
    
    #Choose the first one
    broken_tie = max_down_ind[0]

    return broken_tie

def RC_values(who_infected, loc):
    initial_node = loc
    
    up_messages = [1]*len(who_infected) 
    down_messages = [(1,1)]*len(who_infected)

    up_messages = rumor_centrality_up(up_messages,who_infected,initial_node,initial_node)
    down_messages = rumor_centrality_down(down_messages,up_messages,who_infected,initial_node,initial_node)

    pr = reduce(mul, up_messages, 1)
    if pr == 0:
        scale = 1
    else:
        scale = (factorial(up_messages[loc])) // pr

    vals = [(i, (j*scale // k)) for i, (j,k) in enumerate(down_messages)]
    return vals
	
def nx_graph_to_adj(graph):
    tmp1 = graph.adjacency()    
    
    lene = 0
    for i in tmp1:
        lene += 1
    tmp2 = [[] for i in range(lene)]
    
    tmp1 = graph.adjacency()
    for i,j in tmp1:
        tmp2[int(i)] = j
    adj = [[k for k in i] for i in tmp2]

    return adj

def to_int(adj):
    tmp = [[] for i in range(len(adj))]
    for n,i in enumerate(adj):
        for m,j in enumerate(i):
            tmp[n].append(int(j))
    return tmp