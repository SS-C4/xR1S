from __future__ import division
from pylab import *
import random as rnd
import networkx as nx
import matplotlib.pyplot as plt
import numpy

rcParams['figure.figsize'] = 12, 12  # that's default image size for this interactive session

def draw_graph(graph, labels, attr, graph_layout='spring', to_draw='0', 
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):
    """ 
    Based on: https://www.udacity.com/wiki/creating-network-graphs-with-python
    We describe a graph as a list enumerating all edges.
    Ex: graph = [(1,2), (2,3)] represents a graph with 2 edges - (node1 - node2) and (node2 - node3)
    """
    
    # create networkx graph
    G=nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    #add attributes to nodes
    nx.set_node_attributes(G, attr)

    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    elif graph_layout == 'shell':
        graph_pos=nx.shell_layout(G)
    else:
        graph_pos=nx.planar_layout(G)

    # draw graph
    if to_draw == 0:
        nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
        nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
        nx.draw_networkx_labels(G, graph_pos, labels, font_size=node_text_size)
        # show graph
        plt.show()

    return G
    
def build_adjacency(filename, min_degree, num_nodes):
    
    adjacency = [[] for i in range(num_nodes)]
    
    # open the datafile
    f = open(filename,'rb')
    
    edges = f.readlines()
    
    # add all the edges
    for edge in edges:
        edge = edge.split()
        source = int(edge[0]) - 1
        destination = int(edge[1]) - 1
        if (destination < num_nodes):
            adjacency[source].append(destination)
            adjacency[destination].append(source)
    
    # zero out the people with fewer than min_degree friends
    while True:
        loopflag = True
        for i in range(len(adjacency)):
            if len(adjacency[i]) < min_degree and len(adjacency[i]) > 0:
                loopflag = False
                for node in adjacency[i]:
                    adjacency[node].remove(i)
                adjacency[i] = []
        if loopflag:
            break
    
    return adjacency

def adjacency_to_graph(adjacency):
    graph = []
    for node in range(len(adjacency)):
        if adjacency[node]:
            for neighbors in range(len(adjacency[node])):
                graph.append((node, adjacency[node][neighbors]))             
    return graph

def generate_source(adjacency):
    num_nodes = len(adjacency)
    while True:
        source = rnd.randint(0,num_nodes-1)
        if len(adjacency[source]) > 0:
            break
    return source
    
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
        down_messages[called_node] = down_messages[calling_node]*(float(up_messages[called_node])/(len(who_infected)-up_messages[called_node]))
        for i in who_infected[called_node]:
            if i != calling_node:
                down_messages = rumor_centrality_down(down_messages, up_messages, who_infected, called_node, i)
    return down_messages 


def rumor_center(who_infected):
    # computes the estimate of the source based on rumor centrality
    initial_node = 0       # can use arbitrary initial index
    
    up_messages = [1]*len(who_infected) 
    down_messages = [1]*len(who_infected)

    up_messages = rumor_centrality_up(up_messages,who_infected,initial_node,initial_node)
    down_messages = rumor_centrality_down(down_messages,up_messages,who_infected,initial_node,initial_node)    
    
    max_down = max(down_messages)
    max_down_ind = [i for i, j in enumerate(down_messages) if j == max_down]
    broken_tie = max_down_ind[rnd.randrange(0,len(max_down_ind),1)]
    
    return broken_tie

def RC_values(who_infected, loc):
    initial_node = loc
    
    up_messages = [1]*len(who_infected) 
    down_messages = [1]*len(who_infected)

    up_messages = rumor_centrality_up(up_messages,who_infected,initial_node,initial_node)
    down_messages = rumor_centrality_down(down_messages,up_messages,who_infected,initial_node,initial_node)
    
    scale = (numpy.math.factorial(up_messages[loc])) / (numpy.prod(up_messages))

    vals = [(i, j*scale) for i, j in enumerate(down_messages)]
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


