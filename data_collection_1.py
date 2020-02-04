"""
data_collection_1.py 
This code imports elites.csv and filters it into 'my_elites.csv', which will be used subsequently.

1 - authenticaion
2 - import csv 'elites_filtered.csv'
3 - edit this and save it into 'my_elites.csv'

@author: lizakarmannaya
"""

import tweepy
import keys  # this is my own file with 4 keys, stored in /Users/lizakarmannaya
import pandas as pd
import time 
import csv
import os
import matplotlib.pyplot as plt


######## 1 - authenticaion #################################################

auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# The keyword argument wait_on_rate_limit=True tells Tweepy to wait 15 minutes
# each time it reaches a given API method’s rate limit.
# The keyword argument wait_on_rate_limit_notify=True tells Tweepy that, if it
# needs to wait due to rate limits, it should notify you by displaying a
# message at the command line.


# ################# 2 - Importing elites_filtered.csv ###############

# read elites_filtered.csv
elites_filtered = pd.read_csv('elites_filtered.csv')
elites_filtered.head()
elites_filtered.tail()
elites_filtered.shape # 400, 6


################# 3 - filter elites_filtered more and turn it into my_elites.csv #################
# eg surveys_df[surveys_df.year == 2002]
# eg surveys_df[(surveys_df.year >= 1980) & (surveys_df.year <= 1985)]
my_elites = elites_filtered[elites_filtered.Validated=='y'] # exclude non-validates accounts
my_elites.shape #366, 6 
my_elites = my_elites[my_elites.party !='Speaker'] # exclude Speaker (non-partisan)
my_elites.shape #365, 6 

# add column followers_count to my_elites dataframe
followers_counts = []
for elite in my_elites['twitter_name']: 
    count = api.get_user(elite).followers_count
    followers_counts.append(count)

followers_counts[0:10]
my_elites['followers_count'] = followers_counts
my_elites.head()
my_elites['followers_count']
# build histograms of followers.counts using plt
plt.hist(my_elites['followers_count'])
my_elites['followers_count'].describe
my_elites['followers_count'].mean() # 58933.24931506849
my_elites['followers_count'].median() # 18322.0
my_elites['followers_count'].min() # 1214
my_elites['followers_count'].max() # 2,367,748

# my_elites = pd.read_csv('my_elites.csv', index_col=0)
# my_elites.shape #365, 7
# TO DO: exclude elites who have <2000 followers (following Barbera)
my_elites = my_elites[my_elites.followers_count >2000]
my_elites.shape #362, 7
my_elites.head()

#save the new, completely filtered dataframe to 'my_elites.csv'
my_elites.to_csv('my_elites.csv')