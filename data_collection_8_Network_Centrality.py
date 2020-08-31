"""
data_collection_10_Network_Centrality.py

This code calcualtes centrality metrics...

1 - load in graphs - Largest weakly Connected Components!! 
2 - applying HITs algorithm
4 - re-calculating centrality within my sub-graph only 

(4 - draw network graphs with hubs centrality metrics --> see next .py doc)

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

L = nx.read_pajek('study2_largest_wcc_LEFT_directed.net')
R = nx.read_pajek('study2_largest_wcc_RIGHT_directed.net')
#this imports them as multigraph types --> convert to DiGraph
L = nx.DiGraph(L)
R = nx.DiGraph(R)


########################################
#### 2 - applying HITS algorithm #####
########################################

#for LEFT
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
len(hits_L_hubs_noelites) #822752 - without elites
L.number_of_nodes() #822781 - with elites 

##NB re-run these 3 sections below
plt.hist(hits_L_hubs_noelites.values(), 40, log=False, facecolor='red', alpha=0.5)
plt.savefig('RESULTS/hist_LEFT_hubs_noelites') #have to execute together with line above to avoid saving blank canvas 

plt.hist(hits_L_hubs_noelites.values(), 40, log=True, facecolor='red', alpha=0.5)
plt.savefig('RESULTS/hist_LEFT_hubs_noelites_logscale') #have to execute together with line above to avoid saving blank canvas 


LEFT_hubs = pd.DataFrame.from_dict(data=hits_L_hubs_noelites, orient='index', columns=['hubs'])
LEFT_hubs.to_csv('hubs_scores/LEFT_hubs_noelites.csv')




#repeat for RIGHT
hits_R_hubs, hits_R_authorities = nx.hits(R)
#example hits_L_authorities['703690879'] #0

plt.hist(hits_R_hubs.values(), 40, log=False, facecolor='blue', alpha=0.5)
plt.savefig('RESULTS/hist_RIGHT_hubs_with_elites') #have to execute together with line above to avoid saving blank canvas 

#deleting elites from graph 
to_delete_RIGHT = set(R.nodes()).intersection(to_delete)
len(to_delete_RIGHT) #35

hits_R_hubs_noelites = hits_R_hubs ### NB this currently doesn't help distibguish them - pointless
for item in to_delete_RIGHT:
    del hits_R_hubs_noelites[item]
len(hits_R_hubs_noelites) #1542221 - without elites
#len(hits_R_hubs) #1542221 - original dict is also modified
R.number_of_nodes() #1542256 - with elites 

#NB re-run these 3 sections below
plt.hist(hits_R_hubs_noelites.values(), 40, log=False, facecolor='blue', alpha=0.5)
plt.savefig('RESULTS/hist_RIGHT_hubs_noelites') #have to execute together with line above to avoid saving blank canvas 

plt.hist(hits_R_hubs_noelites.values(), 40, log=True, facecolor='blue', alpha=0.5)
plt.savefig('RESULTS/hist_RIGHT_hubs_noelites_logscale') #have to execute together with line above to avoid saving blank canvas 


RIGHT_hubs = pd.DataFrame.from_dict(data=hits_R_hubs_noelites, orient='index', columns=['hubs'])
RIGHT_hubs.to_csv('hubs_scores/RIGHT_hubs_noelites.csv')
RIGHT_hubs




#### calculating skew and kurtosis for entire sample's hubs centrality 
## NB re-run these?
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

df = pd.read_csv('RESULTS_df_multiverse_4.csv', index_col=0)
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
        
len(errors3) #326

df.head()
df.shape #(34284, 20)

df['authorities']
df['hubs']
# create user_id_str_index from user_id_str
# df = df.set_index('user_id_str_index') #using twitter_name = screen_name as index for later

df.to_csv('RESULTS_df_multiverse_6.csv')

#plt.hist(df['authorities'], log=False, facecolor='purple', alpha=0.5)
#plt.hist(df['hubs'], log=False, facecolor='purple', alpha=0.5)




#############################################################################
########### 3 - re-calculating centrality within my sub-graph only ##########
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









