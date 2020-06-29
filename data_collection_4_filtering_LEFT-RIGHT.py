"""
data_collection_4_filtering_LEFT-RIGHT.py 

This code goes through all followers in  filters them by activity

1) Take collection of followers of one elite, get_user_objects for each 
2) apply spam and activity filters
3) repeat for all csvs of followers 
NB make sure repeated followers get recognised!!! 

1 - authentication for API 
2 - create 2 lists of nodes to filter
3 - create df_LEFT and df_RIGHT

@author: lizakarmannaya
"""

import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tweepy
import keys


######### 1 - authenticaion #################################################
auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


######### 2 - create 2 lists of nodes to filter #################################################

LEFT_nodes_to_filter = list(pd.read_csv('largest_cc_LEFT_nodelist.csv', header=None)[0])
len(LEFT_nodes_to_filter) #821777

#RIGHT_nodes_to_filter = list(pd.read_csv('largest_cc_RIGHT_nodelist.csv', header=None)[0])
#len(RIGHT_nodes_to_filter) #1564959



######### 3 - create df_LEFT and df_RIGHT #################################################

headings = "id, screen_name, created_at, followers_count, friends_count, statuses_count, location, lang, most-recent-status".split(', ') 
headings
df_LEFT = pd.DataFrame(columns=headings) 
#df_RIGHT = pd.DataFrame(columns=headings) 

# add nodes (ids) as rows in each df
df_LEFT['id']=LEFT_nodes_to_filter #looks like it keeps them as strings ?
df_LEFT.head() 
df_LEFT.to_csv('df_LEFT.csv')

#df_RIGHT['id']=RIGHT_nodes_to_filter
#df_RIGHT.head() 
#df_RIGHT.to_csv('df_RIGHT.csv')











## REPEAT BELOW FOR LEFT AND RIGHT 
############## read in df #######################
df = pd.read_csv('df_LEFT.csv', index_col=0) ### sub in RIGHT here later

df['id'] #check that this returns list/series of ids 
df['id_index'] = df['id']
df=df.set_index('id_index')
df.head()
df.shape



######### 4 - apply api.lookup_users & record relevant info ###########################

user_ids = list(df['id']) # list; collection of user_ids
#type(user_ids) #pandas.core.series.Series turned into list
results = []
counter=0
for i in range(0, len(user_ids), 100): ## NB need to make sure I pass in a list divisible by 100
    try:
        for user in api.lookup_users(user_ids = user_ids[i:i+100]):
            counter+=1
            results.append(user) #NB using append, not extend
            print(counter)

    except tweepy.TweepError as e:
        print('Something went wrong, quitting...', e)
        pass

## now I have a 'results' object, from which I can extract relevant detials for filtering 
length = len(results)
print(length)
print(f'len(results) ={length}') #819299

#save results list from LEFT df
with open('results_from_df_LEFT_cc_for_filtering.txt', 'w') as f:
    f.write(str(results))


#build up df with relevant info from 'results' object
counter = 0
for user in results: #loop through each user object in results set 
    counter += 1
    for row in df['id']: #loop through rows in df - could also use df.index?
        if user.id == row: #otherwise id column will not match id index etc.
        #possibly the above will do the error handling for me = discard deleted users
            df.loc[[row], ['id']] = user.id #can check against index next 
            df.loc[[row], ['screen_name']] = user.screen_name
            df.loc[[row], ['created_at']] = user.created_at
            df.loc[[row], ['followers_count']] = user.followers_count
            df.loc[[row], ['friends_count']] = user.friends_count
            df.loc[[row], ['statuses_count']] = user.statuses_count
            df.loc[[row], ['location']] = user.location
            df.loc[[row], ['lang']] = user.lang
           # df.loc[[row], ['most-recent-status']] = user.status.created_at ## CHECK!!! - this was not done for rows 1-67000 of df!!!
           #the aove drops when user has no status
            
            print(f'finished user {counter} out of {length}')


df.head()

df.to_csv('df_LEFT_cc_for_filtering.csv')

df['followers_count']

results[2].status


for user in results:
    try:
        if user.status in results:
            for row in df.index: #loop through rows in df - could also use df.index?
                if user.id == row:
                    print(user.status.created_at)
    except AttributeError as e:
        print('NA. Error:' + e)



    df.loc[[row], ['most-recent-status']] = user.status.created_at 
else:
    df.loc[[row], ['most-recent-status']] = 'NA' 



#### NB repeat for RIGHT list




#### EDITED ON MAC FROM HERE ####


######### 5 - apply filtering - FINISH!!! ################

## APPLY FILTERING in pandas to df 
##Following Barbera (2015), discard followers who:
##      Have sent <100 tweets
##      Have <25 followers
##      Have not sent one tweet in the past six months  
##      Are located outside the borders of the country 
##      potentially with the exception of geographical relevance, as Twitter has restricted access to geographical information

##      NB Barbera used http://www.datasciencetoolkit.org/ geocoder 

df_filtered[~ df.followers_count>25 & df.statuses_count>100]
#add most recent status >= date 6 months ago 
past6mths = '2019-10-01 00:00:00'
df_filtered[~ df_filtered.most-recent-status > past6mths]
#add location within borders of the country? 
df_filtered.lang
df_filtered.location

## NB remember to also get rid of rows where screen_names = NaN   
#df_filtered[~ df_filtered.id != 'NaN']    




#save filtered df
df_filtered.to_csv('df_LEFT_cc_filtered.csv')


# save filtered list of user_ids to use to filter nodes in network 
filtered_nodes = list(df_filtered['id'])




#### NB LEFT-RIGHT split from here onwards


## IMPORT graphs  AGAIN
G=nx.read_pajek('largest_cc_LEFT.net')
G=nx.read_pajek('largest_cc_RIGHT.net')

to_remove = list(G.nodes()) - filtered_nodes #NB check this works!! 
#then apply this: 
G.remove_nodes_from(to_remove)

#save nodelist for tweet collection
with open('largest_cc_LEFT_nodelist_filtered.csv', 'w') as f: ## NB sub in RIGHT here
    for item in G.nodes():
        f.write(str(item) + '\n')

#save as Pajek graph
nx.write_pajek(G, 'largest_cc_LEFT_filtered.net')
nx.write_pajek(G, 'largest_cc_RIGHT_filtered.net')


#for reading Pajek later 
G=nx.read_pajek('largest_cc_LEFT_filtered.net')
G=nx.read_pajek('largest_cc_RIGHT_filtered.net')

