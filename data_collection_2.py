"""
data_collection_2.py 

This code collects all followers_IDs of each of the elites, saving them in separate files titled 'fillowers_(elite).csv'

1 - authenticaion
2 - define collect_followers(elite) function
3 - apply collect_followers() to every elite, saving into separate files in the format 'followers_(elite).csv'

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


########### 2 - defining a function to list all followers_IDs of the elites ###############

#### code adapted from Sylwester & Perver (2015) ######
# NB the below takes ages - 30,000 follower_ids per 15 mins
# useful to get follower_IDs because: anonymised(ish) and the id never changes
def collect_followers(elite):
    """ This function takes the screen_name of an elite and outputs a csv file 
    titled 'followers_elitename.csv' into the home directory. """ 
    cursor = tweepy.Cursor(api.followers_ids, screen_name=elite, skip_status=True) 
    # NB check that 'elite' is a string??? - use str(elite) ?? 
    
    # set  up file to save the followers into
    filePath = os.path.join(r"/Users/lizakarmannaya/followers_" + elite + '.csv')
    saveFile = open(filePath, 'a')  # 'a' = append

    # write data in file as long as Twitter limit has not been reached
    while True:
        try:
            for follower in cursor.items():       
                #print "follower = %s" % follower
                saveFile.write(str(follower))
                saveFile.write('\n') 
            print("finished!")
            saveFile.close()
            break
        except tweepy.TweepError as e:
                print("error checking limits: %s" % e)
                remain_search_limits = 0
                time.sleep(15*60)

# eg - applying function to a single user 
collect_followers('BimAfolami') # it works!! 
# NB if I repeat the above command, it will simply APPEND the followers again 
# hence need to make sure I delete all files from home directory before re-running
BimAfolami = api.get_user('BimAfolami')
BimAfolami.followers_count #N = 8829
# check that length of this new csv corresponds to followers.count 
csv = pd.read_csv('followers_BimAfolami.csv', header=None)
csv.head()
csv.shape #output: 8829 rows, 1 col - yes, they match 



########### 3 - apply collect_followers() to every elite, saving into separate files ###########

## NB maybe split this up into parts, just in case it crashes? 

# Now I can run collect_followers() on every elite from filtered 'my_elites.csv' file 
my_elites = pd.read_csv('my_elites.csv', index_col=0)
my_elites.shape
my_elites.head()
for elite in my_elites['twitter_name']:
    collect_followers(elite)
# this will produce 365 files titled followers_(elite).csv 
# into the home directory '/Users/lizakarmannaya'

#NB exclude followers of both Liberals and Conservatives? 
