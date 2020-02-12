"""
data_collection_2_SNA.py

This code uses my_elites.csv and followers_(elite).csv files to create a social network

1) Create empty graph.
2) For every elite in my_elites.csv, I need to create a node on the graph, 
and then create nodes for all the followers, 
and then create edges between the elite and all of its followers. 
3) Then repeat for every elite. 
NB make sure repeated followers get recognised!!! 

1 - 
2 - 
3 - 

@author: lizakarmannaya
"""

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
# $ conda install -c conda-forge nxviz

from nxviz import CircosPlot

# initialise empty graph into which we can import nodes and edges
G = nx.Graph()


####################  build graph for one elite first  ##################

followers_lauralascau = pd.read_csv('followers_lauralascau.csv', header=None)  
# NB work out how to read file line by line!!
followers_lauralascau # df with 217 rows, 1 column, indexed 0
G.add_nodes_from(followers_lauralascau[0])  # this is a pd Series
G.add_node('@lauralascau')

# for later:
# convert_node_labels_to_integers(G, first_label=0, ordering='default',
#   label_attribute=None)[source]
G.nodes()
# Out: [1, 2, 3]


# add edge between  two nodes
# e.g. G.add_edge(1, 2)
for node in G.nodes():
    if node != '@lauralascau':
        G.add_edge('@lauralascau', node)

G.edges()
# Out: [(1, 2)]
# returns list of tuples representing the edges,
# in which each tuple shows the nodes that are present on that edge

G.number_of_edges() #217
G.number_of_nodes() #218


# storing metadata on the graph
#G.node[1][‘label’] = ‘blue’

#G.nodes(data=True)
# Out [8]: [(1, {‘label’: ’blue’}), (2, {}), (3, {})]
# returns list of 2 tuples, in which the first element is the node, and
# the second is a dictionary where key: value pairs correspond to our meta-data

#add followers of DuncanBrumby
collect_followers('DuncanBrumby')
followers_DuncanBrumby = pd.read_csv('followers_DuncanBrumby.csv', header=None)  
# followers_DuncanBrumby #290 rows
G.add_node('@DuncanBrumby') #this may be redundant 
for node in followers_DuncanBrumby[0]:
    G.add_edge('@DuncanBrumby', node)

    #if follower not in G.nodes():
        #G.add_nodes_from(followers_DuncanBrumby[0])  # this is a pd Series

#for node in G.nodes():
#    if node in followers_DuncanBrumby:
#        if node != '@DuncanBrumby':
#            G.add_edge('@DuncanBrumby', node)

G.number_of_nodes() #468
G.number_of_edges() #509

collect_followers('AnnaCox_')
followers_AnnaCox_ = pd.read_csv('followers_AnnaCox_.csv', header=None)  
G.add_node('@AnnaCox_') #this may be redundant 
for node in followers_AnnaCox_[0]:
    G.add_edge('@AnnaCox_', node)

# drawing the graph
nx.draw(G, node_size=20, node_color='r', edge_color='black', linewidths=0.3, alpha=0.6, pos=nx.spring_layout(G)) #takes a while

#nx.draw_circular(G, node_size=10)

nx.draw_networkx(G, with_labels=False, node_size=10, width=0.5, node_color='r', edge_color='b', alpha=0.5, labels=None)	

#plt.draw()
#plt.show()
nx.draw(G, pos=nx.circular_layout(G), node_color='r', edge_color='b')

G.clear()
G.nodes() #empty
plt.clf()
plt.savefig("out.png")

S = nx.Graph()
S.add_edge('one', 'two') # hence dont need to create nodes first - they are created automatically when I create edges 
nx.draw(S)

petersen = nx.petersen_graph()
nx.draw(petersen)

c = CircosPlot(G) #doesn't work!! 
c.draw()