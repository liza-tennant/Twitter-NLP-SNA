"""
data_collection_1.py 
This code imports elites_original.csv and filters it into 'my_elites.csv', which will be used subsequently.

1 - authenticaion
2 - import csv 'elites_original.csv'
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


# ################# 2 - Importing elites_original.csv ###############

# read elites_original.csv - a list of all MPs, parties, party leaders and MEPs who have Twitter accounts
elites_original = pd.read_csv('elites_original.csv')
print(elites_original.head())
print(elites_original.tail())
print(elites_original.shape) # 467, 6


################# 3 - filter elites_original and turn it into my_elites.csv #################
# eg surveys_df[surveys_df.year == 2002]
# eg surveys_df[(surveys_df.year >= 1980) & (surveys_df.year <= 1985)]
my_elites = elites_original[elites_original.Validated=='y'] # exclude non-validates accounts
my_elites.shape # 426, 6 
my_elites = my_elites[my_elites.party !='Speaker'] # exclude Speaker (non-partisan)
my_elites.shape # 425, 6 
## also exclude 'Independent' party elites?

# add column followers_count to my_elites dataframe
followers_counts = []
for elite in my_elites['twitter_name']: 
    try: 
        print(f'fetching user {elite}')
        count = api.get_user(elite).followers_count
        print(f'{elite} has {count} followers')
        followers_counts.append(count)
    except:
        print(f'error fetching user {elite}, adding count of -1')
        followers_counts.append(-1) 
        # to allow us to filter out those whose followers_cound could not be retreived later

followers_counts[0:10] # check list
my_elites['followers_count'] = followers_counts
my_elites.shape # 425, 7
# filter out those with followers_count = '-1'
my_elites = my_elites[my_elites.followers_count != -1] 
print(my_elites.shape) # 424, 7

# descriptive stats of my_elites['followers_count']
plt.hist(my_elites['followers_count'], bins=100)
print(my_elites['followers_count'].describe)
print(my_elites['followers_count'].mean()) # 58021.29481132075
print(my_elites['followers_count'].median()) # 17783.5
print(my_elites['followers_count'].min()) # 1210
print(my_elites['followers_count'].max()) # 2370402

# exclude elites who have <2000 followers (following Barbera)
my_elites = my_elites[my_elites.followers_count >2000]
print(my_elites.shape) # 420, 7

#save the new, completely filtered dataframe to 'my_elites.csv'
my_elites.to_csv('my_elites.csv')