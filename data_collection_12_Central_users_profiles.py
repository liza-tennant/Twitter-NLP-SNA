"""
data_collection_12_WordCounts.py 

1 - 100 most central users on LEFT and RIGHT 
2 - 100 most central users on LEFT and RIGHT 

@author: lizakarmannaya
"""

import pandas as pd
import os 
import glob
import csv
import collections
import matplotlib.pyplot as plt
import re
import emoji

import pymongo
from pymongo import MongoClient
import json 
import keys
import pandas as pd
import tweepy
import timeit
import time

import nltk
from nltk.corpus import stopwords


#import df 
df = pd.read_csv('RESULTS_df_multiverse_6.csv', index_col=0)
df.head()
df.shape #(34284, 20)

df_LEFT = df[df['side']=='LEFT']
df_LEFT.shape #(17788, 20)
df_LEFT.head()
df_RIGHT = df[df['side']=='RIGHT']
df_RIGHT.shape #(16496, 20)



########################################################
#### 1 - 100 most central users on LEFT and RIGHT ######
########################################################

## find 100 most hubs-central users in df 


df_LEFT_sorted = df_LEFT.sort_values(by='hubs', ascending=False) #most central at the top
df_LEFT_sorted.head()
df_LEFT_sorted.tail()
df_LEFT_sorted = df_LEFT_sorted.head(100)
LEFT_central_ids = list(df_LEFT_sorted['user_id_str']) #this is a list of user_ids for the 100 most central LEFT users 

df_RIGHT_sorted = df_RIGHT.sort_values(by='hubs', ascending=False) #most central at the top
df_RIGHT_sorted = df_RIGHT_sorted.head(100)
RIGHT_central_ids = list(df_RIGHT_sorted['user_id_str'])

type(RIGHT_central_ids[0]) #int


#### access their profile info, storing in single list ####

## authenticaion ####
auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

## collect profile info ####
LEFT_100 = api.lookup_users(user_ids=LEFT_central_ids) #list of 100 ids max 
LEFT_100[0].description

LEFT_profiles = []

for user in LEFT_100:
    description = user.description.split(' ')
    for word in description: 
        LEFT_profiles.append(word)

len(LEFT_100) #98 profiles still valid 
len(LEFT_profiles) #1333 words 

#LEFT_profiles


RIGHT_100 = api.lookup_users(user_ids=RIGHT_central_ids) #list of 100 ids max 
RIGHT_100[0].description

RIGHT_profiles = []

for user in RIGHT_100:
    description = user.description.split(' ')
    for word in description: 
        RIGHT_profiles.append(word)

len(RIGHT_100) #95 profiles still valid 
len(RIGHT_profiles) #1261 words 



#### clean words in this list ####

def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def clean_wordlist(wordlist):
    wordlist_clean = [string.lower().strip().replace("#", "") for string in wordlist]
    #remove punctuation and symbols - only keep alphabetic tokens 
    wordlist_clean = [word for word in wordlist_clean if word.isalpha()] #using NLTK 
    #remove stopwords 
    stop_words = set(stopwords.words('english'))
    wordlist_clean = [w for w in wordlist_clean if not w in stop_words]
    #filters from before
    wordlist_clean = [re.sub(r"((’|')(s|ll|d|ve|m|re))", "", string) for string in wordlist_clean] 
    wordlist_clean = [remove_emoji(string) for string in wordlist_clean] ##NB define this function earlier
    wordlist_clean = list(filter(None, wordlist_clean)) #drop empty stirng which is the result of dropping emoji
    return wordlist_clean

LEFT_profiles_clean = clean_wordlist(LEFT_profiles)
RIGHT_profiles_clean = clean_wordlist(RIGHT_profiles)



###visualise & save most common profile description words for these 100 x 2 users

#LEFT
counts_LEFT = collections.Counter(LEFT_profiles_clean)
counts_LEFT_30 = pd.DataFrame(counts_LEFT.most_common(30), columns=['words', 'count'])
fig, ax = plt.subplots(figsize=(14, 8))
counts_LEFT_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="red")
ax.set_title("Common words found in profile descriptions of 100 most central LEFT users")
plt.rc('font', size=16)         

plt.savefig('RESULTS/WordCounts/LEFT_100_mostcentral.png')


#RIGHT
counts_RIGHT = collections.Counter(RIGHT_profiles_clean)
counts_RIGHT_30 = pd.DataFrame(counts_RIGHT.most_common(30), columns=['words', 'count'])
fig, ax = plt.subplots(figsize=(14, 8))
counts_RIGHT_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="blue")
ax.set_title("Common words found in profile descriptions of 100 most central RIGHT users")
plt.rc('font', size=16)          # controls default text sizes

plt.savefig('RESULTS/WordCounts/RIGHT_100_mostcentral.png')






########################################################
#### 2 - 100 least central users on LEFT and RIGHT #####
########################################################

df_LEFT_sorted = df_LEFT.sort_values(by='hubs', ascending=False) #most central at the top
df_LEFT_sorted = df_LEFT_sorted.tail(100)
LEFT_noncentral_ids = list(df_LEFT_sorted['user_id_str']) #this is a list of user_ids for the 100 most central LEFT users 

df_RIGHT_sorted = df_RIGHT.sort_values(by='hubs', ascending=False) #most central at the top
df_RIGHT_sorted = df_RIGHT_sorted.tail(100)
RIGHT_noncentral_ids = list(df_RIGHT_sorted['user_id_str'])


LEFT_100 = api.lookup_users(user_ids=LEFT_noncentral_ids) #list of 100 ids max 
LEFT_100[0].description

LEFT_profiles = []

for user in LEFT_100:
    description = user.description.split(' ')
    for word in description: 
        LEFT_profiles.append(word)

len(LEFT_100) # 98 profiles still valid 
len(LEFT_profiles) # 1491 words 

LEFT_profiles


RIGHT_100 = api.lookup_users(user_ids=RIGHT_noncentral_ids) #list of 100 ids max 
RIGHT_100[0].description

RIGHT_profiles = []

for user in RIGHT_100:
    description = user.description.split(' ')
    for word in description: 
        RIGHT_profiles.append(word)

len(RIGHT_100) # 97 profiles still valid 
len(RIGHT_profiles) # 938 words 




LEFT_profiles_clean = clean_wordlist(LEFT_profiles)
RIGHT_profiles_clean = clean_wordlist(RIGHT_profiles)



###visualise & save most common profile description words for these 100 x 2 users

#LEFT
counts_LEFT = collections.Counter(LEFT_profiles_clean)
counts_LEFT_30 = pd.DataFrame(counts_LEFT.most_common(30), columns=['words', 'count'])
fig, ax = plt.subplots(figsize=(14, 8))
counts_LEFT_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="red")
ax.set_title("Common words found in profile descriptions of 100 least central LEFT users")
plt.rc('font', size=16)         

plt.savefig('RESULTS/WordCounts/LEFT_100_leastcentral.png')


#RIGHT
counts_RIGHT = collections.Counter(RIGHT_profiles_clean)
counts_RIGHT_30 = pd.DataFrame(counts_RIGHT.most_common(30), columns=['words', 'count'])
fig, ax = plt.subplots(figsize=(14, 8))
counts_RIGHT_30.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="blue")
ax.set_title("Common words found in profile descriptions of 100 least central RIGHT users")
plt.rc('font', size=16)          # controls default text sizes

plt.savefig('RESULTS/WordCounts/RIGHT_100_leastcentral.png')