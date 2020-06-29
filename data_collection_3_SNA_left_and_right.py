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
import matplotlib.mlab as mlab
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


L = nx.DiGraph()
#L.add_edge(1, 2) #draws edge from 1 to 2
#nx.draw(L, with_labels=True)
counter = 0
#add all nodes and edges onto graph - elites and their followers
for path in glob.iglob("followers_*.csv"): #for every elite
    counter += 1

    name = path.split("followers_")[1] 
    name = name.split(".csv")[0]
    name #gives us just the screen_name of the elite

    if name in LEFT_elites: #if the elites is 'LEFT'
        screen_name = '@'+name
        try: 
            id = api.get_user(screen_name).id # NB limited to 900 requests per 15 mins
            L.add_node(id, screen_name = screen_name) # added elites nodes with screen_name as attribute
        
            df = pd.read_csv(open(path), header=None) #read in all followers
            L.add_nodes_from(df[0], screen_name='NA')  # added all followers of each elite; this is a pd Series
    
            for node in df[0]:
                L.add_edge(node, id) #from node to elite
        except tweepy.TweepError as e: 
            print(e)

    print(f'finished {name}, {counter} out of 419')

L.number_of_nodes() # 5376961 --> 5370852 for directed & updated 
L.number_of_edges() # 15452888 --> 15422515 for directed & updated 

os.chdir(os.path.expanduser("~")) #back to home directory to save file
#ls

#save node list 
node_list_left = list(L.nodes(data=True))
type(node_list_left) #list
node_list_left[0] #example item
with open('node_list_LEFT_directed.csv', 'w') as f:
    for item in node_list_left:
        f.write(str(item) + '\n')


######## 4 - create RIGHT networkx graph ############################################

#create RIGHT_elites 
RIGHT_elites = [elite for elite in my_elites.index if my_elites.loc[[elite], ['side']].values[0]=='RIGHT']
len(RIGHT_elites) #191

os.chdir('followers_ELITEs')

R = nx.DiGraph()
counter = 0
#add all nodes and edges onto graph - elites and their followers
for path in glob.iglob("followers_*.csv"): #for every elite
    counter += 1

    name = path.split("followers_")[1] 
    name = name.split(".csv")[0]
    name #gives us just the screen_name of the elite

    if name in RIGHT_elites: #if the elites is 'LEFT'
        screen_name = '@'+name
        
        try: 
            id = api.get_user(screen_name).id # NB limited to 900 requests per 15 mins
            R.add_node(id, screen_name = screen_name) # added elites nodes with screen_name as attribute
        
            df = pd.read_csv(open(path), header=None) #read in all followers
            R.add_nodes_from(df[0], screen_name='NA')  # added all followers of each elite; this is a pd Series
            ## NB the screen_name attribute for elites will be over-written as 'NA' if they follow another elite.
            ## Hence, need to re-assign screen_names later
            for node in df[0]:
                R.add_edge(node, id) #from node to elite
        except tweepy.TweepError as e: 
            print(e)

    print(f'finished {name}, {counter} out of 419')

R.number_of_nodes() # 4197613 --> 4177424 for directed & updated
R.number_of_edges() # 9137946 --> 8998136 for directed & updated

os.chdir(os.path.expanduser("~")) #back to home directory to save file

#save node list - DONE
node_list_right = list(R.nodes(data=True))
node_list_right[0] #example item
with open('node_list_RIGHT_directed.csv', 'w') as f:
    for item in node_list_right:
        f.write(str(item) + '\n')


######## 5 - remove overlap between LEFT & RIGHT graph ############################################
os.chdir(os.path.expanduser("~")) #back to home directory to save files

#save directed graphs
nx.write_pajek(L, 'Graph_LEFT_overlap_included.net')
#nx.write_gexf(L, 'Graph_LEFT_overlap_included.gexf')
nx.write_pajek(R, 'Graph_RIGHT_overlap_included.net')
#nx.write_gexf(R, 'Graph_RIGHT_overlap_included.gexf')

L = nx.read_pajek('Graph_LEFT_overlap_included.net')
#L = nx.read_gexf('Graph_LEFT_overlap_included.gexf')
R = nx.read_pajek('Graph_RIGHT_overlap_included.net')
#R = nx.read_gexf('Graph_RIGHT_overlap_included.gexf')


#save node lists wthout metadata - to turn lists (not dict) into sets
node_list_left = list(L.nodes(data=False)) 
node_list_right = list(R.nodes(data=False))

# use set operations to find overlap
left = set(node_list_left)
right = set(node_list_right)
overlap = left.intersection(right)
len(overlap) #1521599 --> 1517567 directed

# save overlap list for future reference
with open('node_list_overlap.csv', 'w') as f: 
    for item in overlap:
        f.write(str(item) + '\n')

L.remove_nodes_from(overlap)
R.remove_nodes_from(overlap)

L.number_of_nodes() # 3855362 --> 3853285 without overlap
L.number_of_edges() # 1018168 --> 1019598 without overlap

R.number_of_nodes() # 2676014 --> 2659857 without overlap
R.number_of_edges() # 1911249 --> 1840621 without overlap

#looks like a lot of elites were in the overlap - this is meaningful
# but we shall still keep them out of the analysis 
# to compare people who only communicate in their own LEFT or RIGHT community


#### Connected components (after excluding overlap) ####
nx.is_semiconnected(L) #False

largest_wcc_LEFT = max(nx.weakly_connected_components(L), key=len)
#len(nx.weakly_connected_components(L)) - doesn;t work --> cannot currently work out how many CCs are in LEFT directed graph 
largest_wcc_LEFT = L.subgraph(largest_wcc_LEFT).copy()
largest_wcc_LEFT.number_of_nodes() #822781
largest_wcc_LEFT.number_of_edges() #1019598

## REPEAT FOR RIGHT
largest_wcc_RIGHT = max(nx.weakly_connected_components(R), key=len)
#len(nx.weakly_connected_components(R)) - doesn;t work --> cannot currently work out how many CCs are in RIGHT directed graph 
largest_wcc_RIGHT = R.subgraph(largest_wcc_RIGHT).copy()
largest_wcc_RIGHT.number_of_nodes() #1542256
largest_wcc_RIGHT.number_of_edges() #1840621

#count number of weakly connected components 
nx.number_weakly_connected_components(L) #3030505
nx.number_weakly_connected_components(R) #1117602


## the below is for UNDIRECTED GRAPH only --> no longer applicable
#nx.number_connected_components(L) #3033586 --> - this is loads!! 
#nx.number_connected_components(R) #1111056 - loads! 
#[len(c) for c in sorted(nx.connected_components(L), key=len, reverse=True)]
#[len(c) for c in sorted(nx.connected_components(R), key=len, reverse=True)]

#largest_cc_LEFT = max(nx.connected_components(L), key=len)
#type(largest_cc_LEFT) #set
#largest_cc_LEFT = L.subgraph(largest_cc_LEFT).copy()
#largest_cc_LEFT.number_of_nodes() #821777
#largest_cc_LEFT.number_of_edges() #1018168

#largest_cc_RIGHT = max(nx.connected_components(R), key=len)
#largest_cc_RIGHT = R.subgraph(largest_cc_RIGHT).copy()
#largest_cc_RIGHT.number_of_nodes() #1564959
#largest_cc_RIGHT.number_of_edges() #1911249



######## 6 - save updated LEFT and RIGHT networkx graphs ############################################
#save node lists - for downloading tweets from random selection of 100K
node_list_left_filtered = list(L.nodes(data=True))
with open('node_list_LEFT_directed_no_overlap.csv', 'w') as f:
    for item in node_list_left_filtered:
        f.write(str(item) + '\n')

node_list_right_filtered = list(R.nodes(data=True))
with open('node_list_RIGHT_directed_no_overlap.csv', 'w') as f:
    for item in node_list_right_filtered:
        f.write(str(item) + '\n')


#save as Pajek graphs 
nx.write_pajek(L, 'Graph_LEFT_directed_no_overlap.net')
nx.write_pajek(R, 'Graph_RIGHT_directed_no_overlap.net')

#save  as edgelists - NB does not save edge attributes 
nx.write_edgelist(L, 'Graph_LEFT_directed_no_overlap.edgelist', data=True)
nx.write_edgelist(R, 'Graph_RIGHT_directed_no_overlap.edgelist', data=True)


#save as gephi graphs - NOT DONE, TAKES TOO LONG 
#nx.write_gexf(L, 'Graph_LEFT.gexf') #takes ... mins. start 19.05
#nx.write_gexf(R, 'Graph_RIGHT.gexf') #takes ... mins. start 19.05


#read from Pajek
L = nx.read_pajek('Graph_LEFT.net')
R = nx.read_pajek('Graph_RIGHT.net')

#read from edgelist - NB must add data=True --> can't? 
L = nx.read_edgelist('Graph_LEFT.edgelist') #by default creates nx.Graph=undirected
R = nx.read_edgelist('Graph_RIGHT.edgelist') 




#### save largest CCs - for directed ####

#node list
with open('largest_wcc_LEFT_directed_nodelist.csv', 'w') as f: 
    for item in largest_wcc_LEFT.nodes():
        f.write(str(item) + '\n')

with open('largest_wcc_RIGHT_directed_nodelist.csv', 'w') as f: 
    for item in largest_wcc_RIGHT.nodes():
        f.write(str(item) + '\n')


#edge list - NB doesn't record meta-data ('screen_name' attribute of nodes)
nx.write_edgelist(largest_wcc_LEFT, 'largest_wcc_LEFT_directed.edgelist', data=True)
nx.write_edgelist(largest_wcc_RIGHT, 'largest_cc_RIGHT_directed.edgelist', data=True)


#save as gephi graphs 
nx.write_gexf(largest_wcc_LEFT, 'largest_wcc_LEFT_directed.gexf') 
nx.write_gexf(largest_wcc_RIGHT, 'largest_wcc_RIGHT_directed.gexf') 

#save as Pajek graphs 
nx.write_pajek(largest_wcc_LEFT, 'largest_wcc_LEFT_directed.net')
nx.write_pajek(largest_wcc_RIGHT, 'largest_wcc_RIGHT_directed.net')

