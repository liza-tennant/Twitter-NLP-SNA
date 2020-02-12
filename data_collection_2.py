"""
data_collection_2.py 

This code collects all followers_IDs of each of the elites, saving them in separate files titled 'fillowers_{elite}.csv'

1 - authenticaion
2 - define collect_followers(elite) function
3 - apply collect_followers() to each of the 420 elites, saving into separate files in the format 'followers_{elite}.csv'

@author: lizakarmannaya
"""

import tweepy
# import json  # for formatting output files
import keys  # this is my own file with 4 keys, stored in /Users/lizakarmannaya
import pandas as pd
import time 
import csv
import os

######### 1 - authenticaion #################################################

auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


########### 2 - defining a function to list all followers_IDs of the elites ###############

#### adapted from Sylwester & Purver (2015) ######
# NB the below takes ages - 30,000 follower_ids per 15 mins
# useful to get follower_IDs because: anonymised(ish) and the id never changes
def collect_followers(elite):
    """ This function takes the screen_name of an elite and outputs a csv file 
    titled 'followers_elitename.csv' into the home directory. """ 
    cursor = tweepy.Cursor(api.followers_ids, screen_name=elite, skip_status=True) 
    # NB check that 'elite' is a string??? - use str(elite) ?? 
    
    # set  up file to save the followers into
    filePath = os.path.join(r"/Users/lizakarmannaya/followers_" + elite + '.csv')
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

# eg - applying function to a single user 
collect_followers('BimAfolami') # it works!
BimAfolami = api.get_user('BimAfolami')
BimAfolami.followers_count #N = 8934
# check that length of this new followers_....csv corresponds to followers.count 
csv = pd.read_csv('followers_BimAfolami.csv', header=None)
csv.head()
csv.shape #output: 8933 rows, 1 col - they NEARLY match... 

# eg - try another one
collect_followers('JamesCleverly')
csv = pd.read_csv('followers_JamesCleverly.csv', header=None)
csv.head()
csv.shape # 73881, 1
JamesCleverly = api.get_user('JamesCleverly')
JamesCleverly.followers_count #N = 73881 - they match 


########### 3 - apply collect_followers() to every elite, saving into separate files ###########

# Now I can run collect_followers() on every elite from filtered 'my_elites.csv' file 
my_elites = pd.read_csv('my_elites.csv', index_col=0)
my_elites.shape # 420, 7
my_elites.head()

# example - getting a single row for a sinle elite 
my_elites.loc[lambda df: my_elites['twitter_name'] == 'jeremycorbyn'] #2370388
# thus, the total number of followers in my_elites should exceed 2.3mln
my_elites.loc[lambda df: my_elites['twitter_name'] == 'BorisJohnson'] #1530638
# NB capitals matter

# how many followers do we need to collect from the Twitter API?
my_elites['followers_count'].sum() # 24,594,916
# divided by 30000 followers per hour = 819.831 hours = 34 days


## NB maybe split this the next stage into parts, just in case it crashes? 

## do jeremycorbyn and BorisJohnson first? or the party pages?

for elite in my_elites['twitter_name']:
    collect_followers(elite)
# this will produce 420 files titled followers_{elite}.csv 
# into the home directory '/Users/lizakarmannaya'

## NB later exclude followers of both Liberals and Conservatives? 