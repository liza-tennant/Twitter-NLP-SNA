"""
data_collection_3_SNA_left_and_right.py

This code uses followers_{elite}.csv files to create the full social network

1) Create empty graph.
2) For every elite (from my_elites.csv), I need to create a node on the graph, 
and then create nodes for all the followers, 
and then create edges between the elite and all of its followers. 
NB make sure repeated followers get recognised!

1 - authentication
2 - import df
3 - build graph with all LEFT elites and their followers
4 - repeat - create RIGHT networkx graph
5 - remove overlap between LEFT & RIGHT graph 
6 - save updated LEFT and RIGHT networkx graphs

@author: lizakarmannaya
"""
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tweepy
import keys
import fnmatch
import os
import glob

######### 1 - authenticaion #################################################
auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


######## 2 - import df ############################################

#import my_elites df
my_elites = pd.read_csv('my_elites.csv', index_col=0) 
my_elites['twitter_name_index'] = my_elites['twitter_name']
my_elites = my_elites.set_index('twitter_name_index') #using twitter_name = screen_name as index for later
my_elites.head()


######## 3 - create LEFT networkx graph ############################################

#create LEFT_elites (later will also create RIGHT_elites)
LEFT_elites = [elite for elite in my_elites.index if my_elites.loc[[elite], ['side']].values[0]=='LEFT']

len(LEFT_elites) #227


os.chdir('followers_ELITEs')
# how many followers_{elite} files are there?
len(os.listdir()) #419
os.listdir() #returns list of file names


L = nx.Graph()
counter = 0
#add all nodes and edges onto graph - elites and their followers
for path in glob.iglob("followers_*.csv"): #for every elite
    counter += 1

    name = path.split("followers_")[1] 
    name = name.split(".csv")[0]
    name #gives us just the screen_name of the elite

    if name in LEFT_elites: #if the elites is 'LEFT'
        screen_name = '@'+name
        id = api.get_user(screen_name).id # NB limited to 900 requests per 15 mins
        L.add_node(id, screen_name = screen_name) # added elites nodes with screen_name as attribute
        
        df = pd.read_csv(open(path), header=None) #read in all follwers
        L.add_nodes_from(df[0], screen_name='NA')  # added all followers of each elite; this is a pd Series
    
        for node in df[0]:
            L.add_edge(id, node)

    print(f'finished {name}, {counter} out of 419')

L.number_of_nodes() # 5376961
L.number_of_edges() # 15452888

os.chdir(os.path.expanduser("~")) #back to home directory to save file
#ls

#save node list 
node_list_left = list(L.nodes(data=True))
type(node_list_left) #list
node_list_left[0] #example item
with open('node_list_LEFT.csv', 'w') as f:
    for item in node_list_left:
        f.write(str(item) + '\n')


######## 4 - create RIGHT networkx graph ############################################

#create LEFT_elites and RIGHT_elites 
RIGHT_elites = [elite for elite in my_elites.index if my_elites.loc[[elite], ['side']].values[0]=='RIGHT']
len(RIGHT_elites) #191

os.chdir('followers_ELITEs')

R = nx.Graph()
counter = 0
#add all nodes and edges onto graph - elites and their followers
for path in glob.iglob("followers_*.csv"): #for every elite
    counter += 1

    name = path.split("followers_")[1] 
    name = name.split(".csv")[0]
    name #gives us just the screen_name of the elite

    if name in RIGHT_elites: #if the elites is 'LEFT'
        screen_name = '@'+name
        id = api.get_user(screen_name).id # NB limited to 900 requests per 15 mins
        R.add_node(id, screen_name = screen_name) # added elites nodes with screen_name as attribute
        
        df = pd.read_csv(open(path), header=None) #read in all follwers
        R.add_nodes_from(df[0], screen_name='NA')  # added all followers of each elite; this is a pd Series
    
        for node in df[0]:
            R.add_edge(id, node)

    print(f'finished {name}, {counter} out of 419')

R.number_of_nodes() # 4197613
R.number_of_edges() # 9137946

os.chdir(os.path.expanduser("~")) #back to home directory to save file

#save node list 
node_list_right = list(R.nodes(data=True))
node_list_right[0] #example item
with open('node_list_RIGHT.csv', 'w') as f:
    for item in node_list_right:
        f.write(str(item) + '\n')


######## 5 - remove overlap between LEFT & RIGHT graph ############################################

node_list_left = list(L.nodes(data=False)) #wthout metadata - to turn list (not dict) into set
node_list_right = list(R.nodes(data=False))

# suse et operations to find overlap
left = set(node_list_left)
right = set(node_list_right)
overlap = left.intersection(right)
len(overlap) #1521599

L.remove_nodes_from(overlap)
R.remove_nodes_from(overlap)

L.number_of_nodes() # 3855362 without overlap
L.number_of_edges() # 1018168 without overlap

R.number_of_nodes() # 2676014 without overlap
R.number_of_edges() # 1911249 without overlap

#looks like a lot of elites were in the overlap - this is meaningful
# but we shall still keep them out of the analysis 
# to compare people who only communicate in their own LEFT or RIGHT community


#### Connected components (after excluding overlap) ####

nx.number_connected_components(L) #3033586 - this is loads!! 
nx.number_connected_components(R) #1111056 - loads! 
#[len(c) for c in sorted(nx.connected_components(L), key=len, reverse=True)]
#[len(c) for c in sorted(nx.connected_components(R), key=len, reverse=True)]

largest_cc_LEFT = max(nx.connected_components(L), key=len)
type(largest_cc_LEFT) #set
largest_cc_LEFT = L.subgraph(largest_cc_LEFT).copy()
largest_cc_LEFT.number_of_nodes() #821777
largest_cc_LEFT.number_of_edges() #1018168
#L_sub=nx.connected_component_subgraphs(L)[0]
#S_L = [L.subgraph(c).copy() for c in connected_components(G)]

largest_cc_RIGHT = max(nx.connected_components(R), key=len)
largest_cc_RIGHT = R.subgraph(largest_cc_RIGHT).copy()
largest_cc_RIGHT.number_of_nodes() #1564959
largest_cc_RIGHT.number_of_edges() #1911249



######## 6 - save updated LEFT and RIGHT networkx graphs ############################################
#save node lists - for random selection of 1mln & tweet downloading
node_list_left_filtered = list(L.nodes(data=True))
with open('node_list_LEFT_filtered.csv', 'w') as f:
    for item in node_list_left_filtered:
        f.write(str(item) + '\n')

node_list_right_filtered = list(R.nodes(data=True))
with open('node_list_RIGHT_filtered.csv', 'w') as f:
    for item in node_list_right_filtered:
        f.write(str(item) + '\n')

#also save overlap list for future reference
with open('node_list_overlap.csv', 'w') as f: 
    for item in overlap:
        f.write(str(item) + '\n')

#save as Pajek graphs 
nx.write_pajek(L, 'Graph_LEFT.net')
nx.write_pajek(R, 'Graph_RIGHT.net')

#save  as edgelists - NB does not save edge attributes 
nx.write_edgelist(L, 'Graph_LEFT.edgelist', data=True)
nx.write_edgelist(R, 'Graph_RIGHT.edgelist', data=True)


#save as gephi graphs - NOT DONE, TAKES TOO LONG 
nx.write_gexf(L, 'Graph_LEFT.gexf') #takes ... mins. start 19.05
nx.write_gexf(R, 'Graph_RIGHT.gexf') #takes ... mins. start 19.05


#read from Pajek
L = nx.read_pajek('Graph_LEFT.net')
R = nx.read_pajek('Graph_RIGHT.net')

#read from edgelist - NB add data=True
L = nx.read_edgelist('Graph_LEFT.edgelist') #by default creates nx.Graph=undirected
R = nx.read_edgelist('Graph_RIGHT.edgelist') 




#### save largest CCs ####

#node list
with open('largest_cc_LEFT_nodelist.csv', 'w') as f: 
    for item in largest_cc_LEFT.nodes():
        f.write(str(item) + '\n')

with open('largest_cc_RIGHT_nodelist.csv', 'w') as f: 
    for item in largest_cc_RIGHT.nodes():
        f.write(str(item) + '\n')


#edge list 
nx.write_edgelist(largest_cc_LEFT, 'largest_cc_LEFT.edgelist', data=True)
nx.write_edgelist(largest_cc_RIGHT, 'largest_cc_RIGHT.edgelist', data=True)


#gephi graph 
nx.write_gexf(largest_cc_LEFT, 'largest_cc_LEFT.gexf') 
nx.write_gexf(largest_cc_RIGHT, 'largest_cc_RIGHT.gexf') 

#save as Pajek graphs 
nx.write_pajek(largest_cc_LEFT, 'largest_cc_LEFT.net')
nx.write_pajek(largest_cc_RIGHT, 'largest_cc_RIGHT.net')
