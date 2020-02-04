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
followers_lauralascau # df with 1 column, indexed 0
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

G.number_of_edges() #8829
G.number_of_nodes() #8830


# storing metadata on the graph
#G.node[1][‘label’] = ‘blue’

#G.nodes(data=True)
# Out [8]: [(1, {‘label’: ’blue’}), (2, {}), (3, {})]
# returns list of 2 tuples, in which the first element is the node, and
# the second is a dictionary where key: value pairs correspond to our meta-data

# drawing the graph
nx.draw(G) #takes a while
plt.show()
nx.draw(G, pos=nx.circular_layout(G), node_color='r', edge_color='b')

nx.draw(S)

petersen = nx.petersen_graph()
nx.draw(petersen)

c = CircosPlot(G) #doesn't work!! 
c.draw()