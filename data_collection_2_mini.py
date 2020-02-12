"""
data_collection_2_mini.py 

This code collects all followers_IDs of each of the elites, saving them in separate files titled 'fillowers_{elite}.csv'

1 - authenticaion
2 - create mini_elites dataframe with only the party accounts 
3 - define collect_followers(elite) function
4 - apply collect_followers() to every elite in the mini_elites, saving into separate files in the format 'followers_{elite}.csv'

@author: lizakarmannaya
"""

import tweepy
# import json  # for formatting output files
import keys  # this is my own file with 4 keys, stored in home directory
import pandas as pd
import time 
import csv
import os

######### 1 - authenticaion #################################################
auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

########### 2 - create mini_elites dataframe with only the party accounts ###########
my_elites = pd.read_csv('my_elites.csv', index_col=0)
my_elites.shape # 420, 7
my_elites.head()

mini_elites = my_elites[my_elites.Position=='party'] # only keep party pages
mini_elites.shape # 8, 7

mini_elites['followers_count'].sum() # = 2,499,533 
# 2499533/300000 = 8.33 hours
mini_elites


########### 3 - [copy from data_collection_2.py] defining ollect_followers() function ###########

def collect_followers(elite):
    """ This function takes the screen_name of an elite and outputs a csv file 
    titled 'followers_elitename.csv' into the home directory. """ 
    cursor = tweepy.Cursor(api.followers_ids, screen_name=elite, skip_status=True) 
    # NB check that 'elite' is a string??? - use str(elite) ?? 
    
    # set  up file to save the followers into
    filePath = os.path.join(r"/.../.../followers_" + elite + '.csv')
    #filePath = os.path.join(r"/home/ldw01/followers_" + elite + '.csv')
    with open(filePath, 'w') as f:
        # write data in file as long as Twitter limit has not been reached
        while True:
            try:
                for follower in cursor.items():       
                    f.write(str(follower) + '\n')
                print("finished!")
                break
            except tweepy.TweepError as e:
                print("error checking limits: %s" % e)
                # remain_search_limits = 0
                time.sleep(15*60)


########### 4 - apply collect_followers() to every elite in the 'mini_elites' dataframe ###########

for elite in mini_elites['twitter_name']:
    collect_followers(elite)
# expected to take 8.33 hours

# from forum: 
# I agree with @scubjwu. To me it happened when the connection went off. I have "fixed" by catching ReadTimeoutError and ConnectionError within the Timeout except.
#except (Timeout, ssl.SSLError, ReadTimeoutError, ConnectionError) as exc:
#Note that ReadTimeoutError belongs to urllib3 packages
#from requests.exceptions import Timeout, ConnectionError
#from requests.packages.urllib3.exceptions import ReadTimeoutError


followers = pd.read_csv('followers_brexitparty_uk.csv', header=None) # sub in other parties here
followers.head() # to check that index wasn't read wrong 
followers.shape 
# compare vs followers_count in mini_elites 
# df.loc[row_indexer, col_indexer] --> don't know row indexer
# x.iloc[1] = {'x': 9, 'y': 99}
mini_elites[['party', 'followers_count']]

# Conservatives 
# 483609 followers were collected; 483434 were counted in df - must have grown since then 

# Plaid_Cymru
# 47283 collected vs. 47274 counted

# UKLabour
# 826733 collected vs. 826660 counted

# duponline
# 43250 collected vs. 43242 counted

# theSNP
# 266134 collected vs. 266046 counted

# LibDems
# 323364 collected vs. 323391 counted - DECREASED? 
# check online now 
LibDems = api.get_user('LibDems')
LibDems.followers_count #N = 323368 - yes, they match 

# TheGreenParty
# 296296 collected vs. 296317 counted - DECREASED?
# check online now 
TheGreenParty = api.get_user('TheGreenParty')
TheGreenParty.followers_count #N = 296297 - yes, they match

# brexitparty 
# 213202 collected vs. 213169 counted 
