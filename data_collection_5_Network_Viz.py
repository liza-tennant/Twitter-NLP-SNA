"""
data_collection_5_Network_Viz.py


1) Import Graph
2) 
3) 


1 - 
2 - try to visualise 
2 - calculate network stats

@author: lizakarmannaya
"""

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import pymongo
from pymongo import MongoClient

#G = nx.read_gexf('Graph_8_parties_filtered.gexf')


################### - try to visualise with networkx ###################

# G = brexitparty + UKLabour + Conservatives
outdeg = G.degree
#G.degree

to_keep = [n for (n, deg) in outdeg if deg > 1]
S = G.subgraph(to_keep)

S.number_of_nodes() # 445,711
S.number_of_edges() # 1,189,419

nx.write_gexf(S, 'Graph_8_parties_degree2plus.gexf')

S = nx.read_gexf('Graph_8_parties_degree3plus.gexf')

# nx.draw(S, pos=)
nx.draw_circular(S) # takes too long 
#plt.savefig("path.png")


# nx.draw(G, pos=graphviz_layout(G))
# + https://stackoverflow.com/questions/21978487/improving-python-networkx-graph-layout

 
####################  - calculate network stats ###################
 
print("Network density:", nx.density(G))

print("Network diameter:", nx.diameter(G)) # takes very long 

print(nx.is_connected(G)) # will return false if graph has >1 component - returns True 

components = nx.connected_components(G)
largest_component = max(components, key=len)

print(nx.transitivity(G))

#calculate centrality metrics for every node
degree_dict = dict(G.degree(G.nodes()))
nx.set_node_attributes(G, degree_dict, 'degree')

print(G['@UKLabour']) # to access all neighbours of @UKlabour
#print(G[node_id])
#type(G[node_id])
G.nodes()

# to add bew attribute & value to node
# G.nodes[1]['room'] = 714


#?? NB could split them up into political culsters first, before next steps?? ?
# if yes - see modularity in Notes 

betweenness_dict = nx.betweenness_centrality(G) # Run betweenness centrality
eigenvector_dict = nx.eigenvector_centrality(G) # Run eigenvector centrality

# Assign each to an attribute in your network
nx.set_node_attributes(G, betweenness_dict, 'betweenness')
nx.set_node_attributes(G, eigenvector_dict, 'eigenvector')


sorted(d for n, d in G.degree())
#[0, 1, 1, 2]
nx.clustering(G)
#{1: 0, 2: 0, 3: 0, 'spam': 0}




################# 1 - LEFT graph ###################

#import list of users to keep in the final network 
df = pd.read_csv('df_LEFT_dates_by_user.csv', index_col=0)
df.head()

#first_list = list(df['user_id_str']) #turn into list, otherwise it's a series
#type(first_list[0]) #int
#len(first_list) #48035 - need to delete the final to_delete set from past analysis 

#with open('users_to_delete_LEFT.txt', 'r') as f:
#    second_list = f.read().splitlines()
#len(second_list) #29807

#subtract first list from second list
#another way: use sets  
#nodes_to_keep = [x for x in first_list if x not in second_list]
#len(nodes_to_keep)

#import list of users from database of filtered tweets 
client = MongoClient() #default host and port
client.database_names()
db = client['TWITTER_LEFT']  ## NB REPEAT for RIGHT (below)
followers = list(db.tweets_filtered.distinct("user_id_str")) 
len(followers) # 18225 unique users - 3 elites removed
type(followers[0]) #str - need to convert 
followers = [int(i) for i in followers] #converting each item to int
client.close()

#read in elites 
my_elites = pd.read_csv('my_elites.csv', index_col=0)
my_elites.head()
elites = list(my_elites['user_id'])
type(elites[0]) #int
#elites[0:5] #check 
#add them together 
nodes_to_keep = followers + elites 
len(nodes_to_keep) #18645
type(nodes_to_keep[0]) #int

#read graphs from Pajek (.net)
G = nx.read_pajek('Graph_LEFT.net') #too slow
#G = nx.read_pajek('Graph_RIGHT.net')

G = nx.read_edgelist('Graph_LEFT.edgelist', nodetype=int) #NB this does not include node attributes 
G.number_of_nodes() #821777

#build subgraph with only the relevant nodes
S = G.subgraph(nodes_to_keep)
S.number_of_nodes() #18254 - some of these elites have been filtered out for tweet analysis
S.number_of_edges() #27321
nx.draw(S)
nx.draw(S, pos=nx.spring_layout(S), node_size=[v * 100 for v in d.values()])
nx.draw(S, pos=nx.spring_layout(S), node_size=5, alpha=0.5)
plt.savefig("Graph_LEFT_filtered_plus_all_elites_5.png")

d = nx.degree(S)
d = [(d[node]+1) * 20 for node in S.nodes()]
d

degree_dict = dict(S.degree(S.nodes()))
nx.set_node_attributes(S, degree_dict, 'degree')

nx.draw_networkx(S, with_labels=False, pos=nx.spring_layout(S), node_size=1, node_color='orangered', alpha=0.3, width=0.05, edge_color='lightgrey')
