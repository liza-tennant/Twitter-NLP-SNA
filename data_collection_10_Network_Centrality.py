"""
data_collection_10_Network_Centrality.py

This code calcualtes centrality metrics...

1 - load in graphs - Largest weakly Connected Components!! 
2 - [missing]
3 - code for directed graph
3.4 - HITs algorithm
4 - re-calculating centrality within my sub-graph only 

(5 - draw network graphs with hubs centrality metrics --> see next .py doc)

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


#### 1 - load in graphs - Largest weakly Connected Components!! ####
os.chdir(os.path.expanduser("~"))

L = nx.read_pajek('largest_wcc_LEFT_directed.net')
R = nx.read_pajek('largest_wcc_RIGHT_directed.net')
#this imports them as multigraph types --> convert to DiGraph
L = nx.DiGraph(L)
R = nx.DiGraph(R)



#########################################
#### 3 - code for directed graph ########
#Katz centrality, PageRank centrality, others 

## NB PageRank doesn't make much sense in my network, as all connections from non-elite nodes are outward. But the visualisation code is below anyway.

page_rank_L = nx.pagerank(L) #default alpha = 0.85
page_rank_R = nx.pagerank(R)

page_rank_L


#### 3.1 plotting  page_rank centrality for entire 2 samples - with elites 
x = page_rank_L.values()
num_bins = 40
plt.hist(x, num_bins, log=False, facecolor='red', alpha=0.5)
plt.savefig('RESULTS/hist_LEFT_pagerank') #in IPython, have to execute together with line above to avoid saving blank canvas 
plt.show()

x = page_rank_R.values()
num_bins = 40
plt.hist(x, num_bins, log=False, facecolor='blue', alpha=0.5)
plt.savefig('RESULTS/hist_RIGHT_pagerank') #in IPython, have to execute together with line above to avoid saving blank canvas 
plt.show()

#find users in this sample with elites with highers page_rank 
#LEFT
sorted_page_rank = {k: v for k, v in sorted(page_rank_L.items(), key=lambda item: item[1])}
most_central = list(sorted_page_rank.keys())[-10:] #the last/most central 10 users
most_central 

#RIGHT
sorted_page_rank = {k: v for k, v in sorted(page_rank_R.items(), key=lambda item: item[1])}
most_central = list(sorted_page_rank.keys())[-10:] #the last/most central 10 users
most_central 


#### 3.2 plotting page_rank for whole sample without elites 
#exclude elites 

#1. import my_elites df as at the start of  document data_collection_3
my_elites = pd.read_csv('my_elites.csv', index_col=0) 
my_elites['twitter_name_index'] = my_elites['twitter_name']
my_elites = my_elites.set_index('twitter_name_index') #using twitter_name = screen_name as index for later
my_elites.head()

elites_ids = my_elites['user_id'] #pandas series
len(elites_ids) #420

##now delete these elites from page_rank_L - LEFT: 
#need to create a list of strings first 
to_delete = []
for item in elites_ids: 
    key = str(item)
    to_delete.append(key)

len(to_delete) #420 

### LEFT ####
to_delete_LEFT = set(L.nodes()).intersection(to_delete)
len(to_delete_LEFT) #29

for item in to_delete_LEFT:
    del page_rank_L[item]

len(page_rank_L) #822752

#build histogram of all pagerank centrality  
x = page_rank_L.values()
num_bins = 40
plt.hist(x, num_bins, log=False, facecolor='red', alpha=0.5)
plt.savefig('RESULTS/hist_LEFT_page_rank_noelites') #have to execute together with line above to avoid saving blank canvas 
plt.show()

#find most central users who are non-elites
sorted_page_rank = {k: v for k, v in sorted(page_rank_L.items(), key=lambda item: item[1])}
most_central = list(sorted_page_rank.keys())[-10:] #the last/most central 10 users
most_central 


### repeat for RIGHT ###
to_delete_RIGHT = set(R.nodes()).intersection(to_delete)
len(to_delete_RIGHT) #35

for item in to_delete_RIGHT:
    del page_rank_R[item]

len(page_rank_R) #1542221

#build histogram of all pagerank centrality  
x = page_rank_R.values()
num_bins = 40
plt.hist(x, num_bins, log=False, facecolor='blue', alpha=0.5)
plt.savefig('RESULTS/hist_RIGHT_page_rank_noelites') #have to execute together with line above to avoid saving blank canvas 
plt.show()

#find most central users who are non-elites
sorted_page_rank = {k: v for k, v in sorted(page_rank_R.items(), key=lambda item: item[1])}
most_central = list(sorted_page_rank.keys())[-10:] #the last/most central 10 users
most_central 





#now need to extract PageRank centrality values for the relevant 17K+16K & add values to dataframe
df = pd.read_csv('RESULTS_df_multiverse_2.csv', index_col=0)
df['page_rank'] = 'NaN'
df.head()

errors = []
for index in df.index:
    user_id = df['user_id_str'].values[index] #NB this is a numpy integer
    if df['side'].values[index] == 'LEFT':
        try: 
            df['page_rank'].values[index] = page_rank_L[str(user_id)]
        except KeyError as e: 
            errors.append(e)
            print(e)
            df['page_rank'].values[index] = 'NaN'
    elif df['side'].values[index] == 'RIGHT': 
        try:
            df['page_rank'].values[index] = page_rank_R[str(user_id)]
        except KeyError as e: 
            errors.append(user_id)
            print(e)
            df['page_rank'].values[index] = 'NaN'
    else:
        print('error')
        
len(errors) #326 
#the user_ids in the 'errors' list are users for whom there was no page_rank measure 

L.nodes['123456'] 

df.head()

#re-set index of df to be the user_id_str
df['user_id_str_index'] = df['user_id_str']
df = df.set_index('user_id_str_index') #using twitter_name = screen_name as index for later
df.head()

12345678 in df.index #True - NB index is integer, not str 
#need to drop elites


df.shape #(34284, 14)

type(df.index[0])
type(errors[0])

## need to drop these 326 users who were not in the new directed graph from the older df_RESULTS
df = df.drop(index=errors)

df.shape #(33958, 14)

df.to_csv('RESULTS_df_multiverse_DIRECTED_with_page_rank.csv')





#### 3.3 - out-degree centrality 

out_degree_centrality_L = nx.out_degree_centrality(L)

x = out_degree_centrality_L.values()
num_bins = 40
plt.hist(x, num_bins, log=False, facecolor='red', alpha=0.5)
#plt.savefig('RESULTS/hist_RIGHT_page_rank_noelites') #have to execute together with line above to avoid saving blank canvas 
plt.show()

out_degree_centrality_R = nx.out_degree_centrality(R)

x = out_degree_centrality_R.values()
num_bins = 40
plt.hist(x, num_bins, log=False, facecolor='blue', alpha=0.5)
#plt.savefig('RESULTS/hist_RIGHT_page_rank_noelites') #have to execute together with line above to avoid saving blank canvas 
plt.show()

## NB I have missed the part where I check who the most central users are based on this metric - with elites, without elites, in my sub-sample 


df = pd.read_csv('RESULTS_df_multiverse_DIRECTED_with_page_rank.csv', index_col=0)
df['out_degree_centrality'] = 'NaN'
df.head()
df = df.reset_index()

errors2 = []
for index in df.index:
    user_id = df['user_id_str'].values[index] #NB this is a numpy integer
    if df['side'].values[index] == 'LEFT':
        try: 
            df['out_degree_centrality'].values[index] = out_degree_centrality_L[str(user_id)]
        except KeyError as e: 
            errors2.append(e)
            print(e)
            df['out_degree_centrality'].values[index] = 'NaN'
    elif df['side'].values[index] == 'RIGHT': 
        try:
            df['out_degree_centrality'].values[index] = out_degree_centrality_R[str(user_id)]
        except KeyError as e: 
            errors2.append(user_id)
            print(e)
            df['out_degree_centrality'].values[index] = 'NaN'
    else:
        print('error')
        
df.head()
df = df.set_index('user_id_str_index') #using twitter_name = screen_name as index for later

df.to_csv('RESULTS_df_multiverse_DIRECTED.csv')




########################################
#### 3.4 - applying HITS algorithm #####
########################################
#compute hubs and authorities socores for each node in graph 
hits_L_hubs, hits_L_authorities = nx.hits(L)

plt.hist(hits_L_hubs.values(), 40, log=False, facecolor='red', alpha=0.5)
plt.savefig('RESULTS/hist_LEFT_hubs_with_elites') #have to execute together with line above to avoid saving blank canvas 
plt.show()

#deleting elites from graph 
my_elites = pd.read_csv('my_elites.csv', index_col=0) 
my_elites['twitter_name_index'] = my_elites['twitter_name']
my_elites = my_elites.set_index('twitter_name_index') #using twitter_name = screen_name as index for later
my_elites.head()

elites_ids = my_elites['user_id'] #pandas series
len(elites_ids) #420

##now delete these elites from page_rank_L - LEFT: 
#need to create a list of strings first 
to_delete = []
for item in elites_ids: 
    key = str(item)
    to_delete.append(key)

len(to_delete) #420 

### LEFT ####
to_delete_LEFT = set(L.nodes()).intersection(to_delete)
len(to_delete_LEFT) #29

hits_L_hubs_noelites = hits_L_hubs ## NB this currently doesn't help distibguish them  
for item in to_delete_LEFT:
    del hits_L_hubs_noelites[item]
len(hits_L_hubs_noelites) #822752
L.number_of_nodes() #822781

plt.hist(hits_L_hubs_noelites.values(), 40, log=False, facecolor='red', alpha=0.5)
plt.savefig('RESULTS/hist_LEFT_hubs_noelites') #have to execute together with line above to avoid saving blank canvas 

plt.hist(hits_L_hubs_noelites.values(), 40, log=True, facecolor='red', alpha=0.5)
plt.savefig('RESULTS/hist_LEFT_hubs_noelites_logscale') #have to execute together with line above to avoid saving blank canvas 


LEFT_hubs = pd.DataFrame.from_dict(data=hits_L_hubs_noelites, orient='index', columns=['hubs'])
LEFT_hubs.to_csv('hubs_scores/LEFT_hubs_noelites.csv')



#repeat for RIGHT
hits_R_hubs, hits_R_authorities = nx.hits(R)
#example hits_L_authorities['123456'] #0

plt.hist(hits_R_hubs.values(), 40, log=False, facecolor='blue', alpha=0.5)
plt.savefig('RESULTS/hist_RIGHT_hubs_with_elites') #have to execute together with line above to avoid saving blank canvas 

#deleting elites from graph 
to_delete_RIGHT = set(R.nodes()).intersection(to_delete)
len(to_delete_RIGHT) #35

hits_R_hubs_noelites = hits_R_hubs ### NB this currently doesn't help distibguish them - pointless
for item in to_delete_RIGHT:
    del hits_R_hubs_noelites[item]
len(hits_R_hubs_noelites) #1542221
len(hits_R_hubs) #1542221
R.number_of_nodes() #1542256

plt.hist(hits_R_hubs_noelites.values(), 40, log=False, facecolor='blue', alpha=0.5)
plt.savefig('RESULTS/hist_RIGHT_hubs_noelites') #have to execute together with line above to avoid saving blank canvas 

plt.hist(hits_R_hubs_noelites.values(), 40, log=True, facecolor='blue', alpha=0.5)
plt.savefig('RESULTS/hist_RIGHT_hubs_noelites_logscale') #have to execute together with line above to avoid saving blank canvas 


RIGHT_hubs = pd.DataFrame.from_dict(data=hits_R_hubs_noelites, orient='index', columns=['hubs'])
RIGHT_hubs.to_csv('hubs_scores/RIGHT_hubs_noelites.csv')
RIGHT_hubs




#### calculating skew and kurtosis for entire sample's hubs centrality 
L_hubs = list(hits_L_hubs.values()) #currently this is without the elites, as they were taken out above 
len(L_hubs) #822752
skew(L_hubs) #-0.1830900326354742
kurtosis(L_hubs) #-1.8363738717470777
np.mean(L_hubs)
mode(L_hubs)
np.median(L_hubs)
np.std(L_hubs)

R_hubs = list(hits_R_hubs.values()) #currently this is without the elites, as they were taken out above 
len(R_hubs) #1542221
skew(R_hubs) #-0.6376712808927192
kurtosis(R_hubs) #-1.16105655692604
np.mean(R_hubs)
mode(R_hubs)
np.median(R_hubs)
np.std(R_hubs)

entire_hubs = L_hubs+R_hubs
len(entire_hubs) #2,364,973
skew(entire_hubs) #0.7903545150997883
kurtosis(entire_hubs) #-0.3640943243229504
np.mean(entire_hubs)
mode(entire_hubs)
np.median(entire_hubs)
np.std(entire_hubs)



#### save hubs & authorities values into results df ####
df = df.reset_index()
df['authorities']='NaN'
df['hubs'] = 'NaN'
df.head()

errors3 = []
for index in df.index:
    user_id = df['user_id_str'].values[index] #NB this is a numpy integer
    if df['side'].values[index] == 'LEFT':
        try: 
            df['authorities'].values[index] = hits_L_authorities[str(user_id)]
            df['hubs'].values[index] = hits_L_hubs[str(user_id)]
        except KeyError as e: 
            errors3.append(e)
            print(e)
            df['authorities'].values[index] = 'NaN'
            df['hubs'].values[index]='NaN'
    elif df['side'].values[index] == 'RIGHT': 
        try:
            df['authorities'].values[index] = hits_R_authorities[str(user_id)]
            df['hubs'].values[index] = hits_R_hubs[str(user_id)]
        except KeyError as e: 
            errors3.append(user_id)
            print(e)
            df['authorities'].values[index] = 'NaN'
            df['hubs'].values[index] = 'NaN'
    else:
        print('error')
        
df.head()
df['authorities']
df['hubs']
df = df.set_index('user_id_str_index') #using twitter_name = screen_name as index for later

df.to_csv('RESULTS_df_multiverse_DIRECTED.csv')

#plt.hist(df['authorities'], log=False, facecolor='purple', alpha=0.5)
#plt.hist(df['hubs'], log=False, facecolor='purple', alpha=0.5)




#############################################################################
########### 4 - re-calculating centrality within my sub-graph only ##########
#############################################################################

#re-load in elites 
my_elites = pd.read_csv('my_elites.csv', index_col=0) 
#my_elites['twitter_name_index'] = my_elites['twitter_name']
#my_elites = my_elites.set_index('twitter_name_index') #using twitter_name = screen_name as index for later
#my_elites.head()
elites_ids = [str(item) for item in my_elites['user_id']] 
len(elites_ids) #420

#re-loaded L and R graphs as at the start of this document

#split elites by graph
elites_LEFT = set(L.nodes()).intersection(elites_ids)
len(elites_LEFT) #29

elites_RIGHT = set(R.nodes()).intersection(elites_ids)
len(elites_RIGHT) #35



df = pd.read_csv('RESULTS_df_multiverse_2.csv', index_col=0)
df.head()

df_LEFT = df[df['side']=='LEFT']
df_LEFT.shape #(17788, 13)
user_ids_LEFT = [str(item) for item in df_LEFT['user_id_str']]

df_RIGHT = df[df['side']=='RIGHT']
df_RIGHT.shape #(16496, 13)
user_ids_RIGHT = [str(item) for item in df_RIGHT['user_id_str']]


L_small_nodes = list(elites_LEFT) + user_ids_LEFT
len(L_small_nodes) #17817
L_small = L.subgraph(L_small_nodes) 
L_small.number_of_nodes() #17817
L_small.number_of_edges() #26796

R_small_nodes = list(elites_RIGHT) + user_ids_RIGHT
len(R_small_nodes) #16531
R_small = R.subgraph(R_small_nodes) 
R_small.number_of_nodes() #16205 - ???? 
R_small.number_of_edges() #21188

#save these new small graphs
nx.write_gexf(L_small, 'L_small.gexf') 
nx.write_gexf(R_small, 'R_small.gexf') 

#save as Pajek graphs 
nx.write_pajek(L_small, 'L_small.net')
nx.write_pajek(R_small, 'R_small.net')




#calculate hubs and authorities scores 
hits_L_small_hubs, hits_L_small_authorities = nx.hits(L_small)

hits_R_small_hubs, hits_R_small_authorities = nx.hits(R_small)


#plot histograms for new hits scores 
plt.hist(hits_L_small_hubs.values(), 40, log=False, facecolor='red', alpha=0.5)
plt.savefig('RESULTS/hist_LEFT_small_hubs_with_elites') #have to execute together with line above to avoid saving blank canvas 

hits_L_small_hubs_noelites = hits_L_small_hubs ### NB this currently modifies the original list 
for item in elites_LEFT:
    del hits_L_small_hubs_noelites[item]
len(hits_L_small_hubs_noelites) #17788
len(hits_L_small_hubs) #177788 - NB the original list is also modified!!! 

plt.hist(hits_L_small_hubs_noelites.values(), 40, log=False, facecolor='red', alpha=0.5)
plt.savefig('RESULTS/hist_LEFT_small_hubs_noelites') #have to execute together with line above to avoid saving blank canvas 




##repeat for RIGHT 
#plot histograms for new hits scores 
plt.hist(hits_R_small_hubs.values(), 40, log=False, facecolor='blue', alpha=0.5)
plt.savefig('RESULTS/hist_RIGHT_small_hubs_with_elites') #have to execute together with line above to avoid saving blank canvas 

hits_R_small_hubs_noelites = hits_R_small_hubs ### NB this currently doesn't help distibguish them - pointless
for item in elites_RIGHT:
    del hits_R_small_hubs_noelites[item]
len(hits_R_small_hubs_noelites) #16170
len(hits_R_small_hubs) #16170 - NB modified the original dictionary!! 

plt.hist(hits_R_small_hubs_noelites.values(), 40, log=False, facecolor='blue', alpha=0.5)
plt.savefig('RESULTS/hist_RIGHT_small_hubs_noelites') #have to execute together with line above to avoid saving blank canvas 




##save these new hubs scores into RESULTS_df_multiverse_4.csv
df = pd.read_csv('RESULTS_df_multiverse_4.csv', index_col=0)

#### save hubs & authorities values into results df ####
df['authorities_small']='NaN'
df['hubs_small'] = 'NaN'
df.head()

errors3 = []
for index in df.index:
    user_id = df['user_id_str'].values[index] #NB this is a numpy integer
    if df['side'].values[index] == 'LEFT':
        try: 
            df['authorities_small'].values[index] = hits_L_small_authorities[str(user_id)]
            df['hubs_small'].values[index] = hits_L_small_hubs[str(user_id)]
        except KeyError as e: 
            errors3.append(e)
            #print(e)
            df['authorities_small'].values[index] = 'NaN'
            df['hubs_small'].values[index]='NaN'
    elif df['side'].values[index] == 'RIGHT': 
        try:
            df['authorities_small'].values[index] = hits_R_small_authorities[str(user_id)]
            df['hubs_small'].values[index] = hits_R_small_hubs[str(user_id)]
        except KeyError as e: 
            errors3.append(user_id)
            #print(e)
            df['authorities_small'].values[index] = 'NaN'
            df['hubs_small'].values[index] = 'NaN'
    else:
        print('error')
        
len(errors3) #326 errors - must be missing values 

df.head()
df['authorities_small']
df['hubs_small']
df['user_id_str_index'] = df['user_id_str']
df = df.set_index('user_id_str_index') #using twitter_name = screen_name as index for later

df.to_csv('RESULTS_df_multiverse_5.csv')



##also plot out_degree_centrality for nre small graphs 
out_degree_centrality_L = nx.out_degree_centrality(L_small)

x = out_degree_centrality_L.values()
num_bins = 40
plt.hist(x, num_bins, log=False, facecolor='red', alpha=0.5)
plt.savefig('RESULTS/hist_LEFT_small_out_degree_centrality_with_elites') #have to execute together with line above to avoid saving blank canvas 
plt.show()

out_degree_centrality_R = nx.out_degree_centrality(R_small)

x = out_degree_centrality_R.values()
num_bins = 40
plt.hist(x, num_bins, log=False, facecolor='blue', alpha=0.5)
plt.savefig('RESULTS/hist_RIGHT_small_out_degree_centrality_with_elites') #have to execute together with line above to avoid saving blank canvas 
plt.show()


######################################
######## COMPLETE FROM HERE ################
######################################

#### read in graphs again 
L_small = nx.read_pajek('L_small.net')
R_small = nx.read_pajek('R_small.net')

L_small = nx.DiGraph(L_small)
R_small = nx.DiGraph(R_small)


#### TRY TO VISUALISE THESE SMALL GRAPHS 
## [code to be filled in]









