from operator import mul
from functools import reduce
from math import factorial
import networkx as nx
from random import random, randrange, randint
import numpy as np

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
    broken_tie = max_down_ind[randrange(0,len(max_down_ind),1)]
    
    # #Choose the first one
    # broken_tie = max_down_ind[0]

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
	
#Jordan center stuff
def get_messages(parent,node,adjacency,up_count,up_count_2nd,up_id,up_id_2nd):
    # obtains the message from node to parent
    
    children = adjacency[node]
    
    # deal with leaves
    if len(children) > 1:    
        # forward messages appropriately
        for child in children:     
            
            if child == parent:
                continue
            up_count, up_count_2nd, up_id, up_id_2nd = get_messages(node, child, adjacency, up_count, up_count_2nd, up_id, up_id_2nd)
            up_count, up_count_2nd, up_id, up_id_2nd = update_counts(node, child, up_count, up_count_2nd, up_id, up_id_2nd)
    
    return up_count, up_count_2nd, up_id, up_id_2nd
    
def update_counts(parent, node, up_count, up_count_2nd, up_id, up_id_2nd):
    # updates the message arrays for jordan centrality
    
    candidates = np.array([up_count[parent], up_count_2nd[parent], up_count[node]+1])
        
    sorted_vals = np.sort(candidates)
    indices = np.argsort(candidates)
    
    up_count[parent] = sorted_vals[-1]
    up_count_2nd[parent] = sorted_vals[-2]
    if (indices[-1] == 2): # the incoming max is the largest
        up_id_2nd[parent] = up_id[parent]
        up_id[parent] = node
        
    elif (indices[-2] == 2): # the incoming max is 2nd largest
        # up_id stays the same
        up_id_2nd[parent] = node
            
    return up_count, up_count_2nd, up_id, up_id_2nd
    
def find_center(root, up_count, up_count_2nd, up_id, up_id_2nd):
    # finds the center of the graph using jordan centrality metric, after messages have been passed
    idx = root
    l1 = up_count[idx]
    l2 = up_count_2nd[idx]
    breakflag = False
    while True:
        if (l1-l2) == 0:
            idx_jordan = idx
            break
        elif (abs(l1-l2)) == 1:
            if breakflag:
                # break ties randomly
                if random() < 0.5:
                    idx_jordan = idx
                # choose the first one
                break
            breakflag = True
            idx_jordan = idx
        elif breakflag:
            # there's no tie, so use the previously found index
            break
            
        idx = up_id[idx]
        l2 = l2 + 1
        l1 = l1 - 1

        if (l1 <= 1):
            idx_jordan = idx
            break
    return idx_jordan

def jordan_center(adjacency):
    # computes the estimate of the source based on jordan centrality
    num_nodes = len(adjacency)
    
    if num_nodes == 1:
        return 0
    elif num_nodes == 2:
        return int(random.random() < 0.5)

    # choose a root that is not a leaf
    while True:
        root = randint(0,num_nodes-1)
        if len(adjacency[root]) > 1:
            break
    # initialize lists
    up_count = [0 for i in range(num_nodes)]
    up_count_2nd = [0 for i in range(num_nodes)]
    up_id = [-1 for i in range(num_nodes)]
    up_id_2nd = [-1 for i in range(num_nodes)]
    
    # start passing messages
    up_count, up_count_2nd, up_id, up_id_2nd = get_messages(root, root, adjacency, up_count, up_count_2nd, up_id, up_id_2nd)
    
    # now find the jordan center
    idx_jordan = find_center(root, up_count, up_count_2nd, up_id, up_id_2nd)
    return idx_jordan

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