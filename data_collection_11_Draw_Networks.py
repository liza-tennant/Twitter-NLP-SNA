"""
data_collection_11_Draw_Networks.py


1 - import df, extract lists of LEFT and RIGHT users
2 - import elites list to add into the sub-graph nodelist
3 - import L and R LwCC graphs 
3 - create sub-graphs for each side, only with the nodes in my sample 
4 - plot two sub-graphs 


@author: lizakarmannaya
"""
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import fnmatch
import os
import glob
from scipy.stats import skew, kurtosis, mode 
import json


#### 1 - import df, extract lists of LEFT and RIGHT users ########
df = pd.read_csv('RESULTS_df_multiverse_DIRECTED.csv', index_col=0)
df.head()

LEFT = df[df.side == 'LEFT']
user_ids_LEFT = LEFT['user_id_str']
len(user_ids_LEFT) #17788
#convert to string ids
user_ids_LEFT = [str(item) for item in user_ids_LEFT]


RIGHT = df[df.side == 'RIGHT']
user_ids_RIGHT = RIGHT['user_id_str']
len(user_ids_RIGHT) #16170
#convert to string ids
user_ids_RIGHT = [str(item) for item in user_ids_RIGHT]


#### 2 - import elites list to add into the sub-graph nodelist #####

#1. import my_elites df
my_elites = pd.read_csv('my_elites.csv', index_col=0) 
my_elites.head()
elites_ids = my_elites['user_id'] #pandas series of integer ids!! 
len(elites_ids) #420
#convert to string ids 
elites = [str(item) for item in elites_ids]

### LEFT ####
elites_LEFT = set(L.nodes()).intersection(elites)
len(elites_LEFT) #29

### RIGHT ###
elites_RIGHT = set(R.nodes()).intersection(elites)
len(elites_RIGHT) #35



#### 3 - import L and R LwCC graphs ##############################
L = nx.read_pajek('largest_wcc_LEFT_directed.net')
R = nx.read_pajek('largest_wcc_RIGHT_directed.net')
#this imports them as multigraph types --> convert to DiGraph
L = nx.DiGraph(L)
R = nx.DiGraph(R)


hits_L_hubs, hits_L_authorities = nx.hits(L)
type(hits_L_hubs) #this is a dictionary where key=a string corresponding to user_id_str, value=a float coresponding to the hubs value
#e.g. type(hits_L_hubs['123456'])

hits_R_hubs, hits_R_authorities = nx.hits(R)



#### 4 - create sub-graphs for each side, only with the nodes in my sample ####
#create list of nodes to keep on each side 
## LEFT 
nodes_to_keep_LEFT = user_ids_LEFT + list(elites_LEFT) #concatenating two lists of strings
len(nodes_to_keep_LEFT) #17817


L_sub = L.subgraph(nodes_to_keep_LEFT)
## save graph in two separate formats  
nx.write_pajek(L_sub, 'Graph_L_sub_directed.net') #save as Pajek graph
nx.write_gexf(L_sub, 'Graph_L_sub_directed.gexf') #save as gephi graph



#now create a dictionary including node sizes by hubs value 

next(iter(hits_L_hubs)) #print first key in Left dictionary 

node_size_LEFT_hubs = {}
for user_id in hits_L_hubs:
    if user_id in user_ids_LEFT: #if user is non-elite
        node_size_LEFT_hubs.update({user_id: hits_L_hubs[user_id]})
len(node_size_LEFT_hubs) #17788
type(node_size_LEFT_hubs)#dict
#list comprehension version
#node_size_LEFT_hubs = {user_id: hits_L_hubs[user_id] for user_id in hits_L_hubs if user_id in user_ids_LEFT}

#use list comprehension version for elites, as this are faster 
node_size_LEFT_authorities = {user_id: hits_L_authorities[user_id] for user_id in hits_L_authorities if user_id in elites_LEFT}
len(node_size_LEFT_authorities) #29
type(node_size_LEFT_authorities) #dict

#now combine the to node_size dictionsries into one 
node_size_LEFT = {**node_size_LEFT_hubs, **node_size_LEFT_authorities}
len(node_size_LEFT) #17817
type(node_size_LEFT) #dict

## save to file 
a_file = open("Graph_LEFT_node_size_dict.json", "w")
json.dump(node_size_LEFT, a_file)
a_file.close()


## LATER can add node_color - two different colors for hubs and authorities + scale by size/importance?



## RIGHT 
nodes_to_keep_RIGHT = user_ids_RIGHT + list(elites_RIGHT)
len(nodes_to_keep_RIGHT) #16205

R_sub = R.subgraph(nodes_to_keep_RIGHT)
## save graph in two separate formats 
nx.write_pajek(R_sub, 'Graph_R_sub_directed.net') #save as Pajek graph
nx.write_gexf(R_sub, 'Graph_R_sub_directed.gexf') #save as gephi graph

node_size_RIGHT_hubs = {user_id: hits_R_hubs[user_id] for user_id in hits_R_hubs if user_id in user_ids_RIGHT}
len(node_size_RIGHT_hubs) #16170

node_size_RIGHT_authorities = {user_id: hits_R_authorities[user_id] for user_id in hits_R_authorities if user_id in elites_RIGHT}
len(node_size_RIGHT_authorities) #35

#now combine the to node_size dictionsries into one 
node_size_RIGHT = {**node_size_RIGHT_hubs, **node_size_RIGHT_authorities}
len(node_size_RIGHT) #16205
type(node_size_RIGHT) #dict

## save to file 
a_file = open("Graph_RIGHT_node_size_dict.json", "w")
json.dump(node_size_RIGHT, a_file)
a_file.close()




#### 5 - plot two sub-graphs  ###################################
### 5.1 re-load-in graphs and node_size dictionaries

##LEFT
#read in graph 
L_sub = nx.read_pajek('Graph_L_sub_directed.net')
#read in node_size dictionary for LEFT 
a_file = open("Graph_LEFT_node_size_dict.json", "r")
node_size_LEFT = a_file.read()
a_file.close()

node_size_LEFT =[v * 100 for v in node_size_LEFT.values()]

#draw LEFT graph for my subsample 

#nx.draw_networkx(L_sub, with_labels=False, pos=nx.spring_layout(L_sub), alpha=0.5, width=0.4, node_size = node_size_LEFT, node_color="orangered", edge_color="grey")
#plt.savefig('RESULTS/Graph_L_sub') #have to execute together with line above to avoid saving blank canvas 
##NB the above didn't work - TypeError: loop of ufunc does not support argument 0 of type dict which has no callable sqrt method

nx.draw_networkx(L_sub, with_labels=False, pos=nx.spring_layout(L_sub), alpha=0.5, width=0.4, node_size = 10, node_color="orangered", edge_color="grey")
plt.savefig('RESULTS/Graph_L_sub') #have to execute together with line above to avoid saving blank canvas 


##RIGHT
#read in graph 
R = nx.read_pajek('Graph_R_sub_directed.net')
#read in node_size dictionary for RIGHT 
a_file = open("Graph_RIGHT_node_size_dict.json", "r")
node_size_RIGHT = a_file.read()
a_file.close()

#draw RIGHT graph for my subsample
#nx.draw_networkx(R_sub, with_labels=False, pos=nx.spring_layout(R_sub), alpha=0.5, width=0.4, node_size = node_size_LEFT, node_color="blue", edge_color="grey")
#plt.savefig('RESULTS/Graph_R_sub_2') #have to execute together with line above to avoid saving blank canvas 

nx.draw_networkx(R_sub, with_labels=False, pos=nx.spring_layout(R_sub), alpha=0.5, width=0.4, node_size = 10, node_color="blue", edge_color="grey")
plt.savefig('RESULTS/Graph_R_sub') #have to execute together with line above to avoid saving blank canvas 


#to solve problem and assign hubs value to node:
# - create attribute 'hubs_value' on each node 
# - draw graph with node_size = (hubs_value * 100) for each node


