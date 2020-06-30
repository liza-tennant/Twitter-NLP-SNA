"""
data_collection_8_mongo_filtering_and_aggregation.py 

This code goes through all followers in  filters them by activity

1 - connect to MongoDB
2 - aggregating tweets by use
3 - cleaning users


@author: lizakarmannaya
"""

import pymongo
from pymongo import MongoClient
#import mongodb
import json 
import keys
import pandas as pd
import tweepy
import timeit
import time
import pprint
import datetime
from datetime import datetime, timedelta
from email.utils import parsedate_tz


######## 1 - connect to MongoDB ########################
client = MongoClient() #default host and port
client.database_names()

db = client['TWITTER_LEFT']  ## NB REPEAT for RIGHT (below)
db.collection_names()
#accounts_LEFT = db['accounts'] #this is a collection 
#list(db.accounts.index_information())
#accounts.count() #100000
tweets_LEFT = db['tweets']
list(tweets_LEFT.index_information())
tweets_LEFT.count()

db = client['TWITTER_RIGHT']  
db.collection_names()
#accounts_RIGHT = db['accounts'] #this is a collection 
#list(db.accounts.index_information())
#accounts.count() #100000
tweets_RIGHT = db['tweets']
list(db.tweets.index_information())
tweets_RIGHT.count()


tweets_LEFT.count()
tweets_RIGHT.count()
## RESULT for LEFT: 10,603,262 tweets from 79,261 users
## RESULT for RIGHT: 9,135,838 tweets from 76,931 users


#tweets_LEFT.count_documents({"lang": "en"}) #NB tweets = db.tweets from before 
## RESULT for LEFT: 9,245,523 tweets are in english ("en") out of 10,603,262; 0 with lang=""
#tweets_RIGHT.count_documents({"lang": "en"}) #NB tweets = db.tweets from before 
## RESULT for RIGHT:

#tweets_LEFT.count_documents({'user.followers_count':{'$gte':25},'user.statuses_count':{'$gte':100}, 'user.lang': 'en'})
## RESULT for LEFT: 



#db = client['TWITTER_draft']
#draft=db['tweets']
#draft.count() #743
#draft2 = draft.find({'user.followers_count':{'$gte':25}, 'user.statuses_count':{'$gte':100}, 'user.lang': 'en'})
#draft2.count()



#########################################################################################################################
######## 3 - cleaning users - see O'Reilly useful notes ###
#########################################################################################################################

#filtered_LEFT = tweets_LEFT.find({"user.followers_count": {"$gte": 25}, "user.statuses_count": {"$gte": 100}, "lang": "en"})
#filtered_LEFT.count() # 8,079,657 tweets after filtering by 3 criteria 
#compare with original count of 10,603,262 tweets 
#type(filtered_LEFT) #pymongo.cursor.Cursor


#TRYING FOR DRAFT 
draft = client['TWITTER_draft']  
tweets_draft = draft['tweets']
tweets_draft.aggregate([
	{"$match": {"user.followers_count": {"$gte": 25}, "user.statuses_count": {"$gte": 100}, "lang": "en"}},
    {"$project" : { #tweet fields to keep
        "user_id_str" : 1 , "tweets" : 1 , "user": 1, "place":1, "geo":1, "coordinates":1, "created_at":1, "full_text":1, "id":1, 
        "entities":1, "in_reply_to_user_id":1, "in_reply_to_status_id":1, "is_quote_status":1, "retweeted":1, "lang":1} },
    #{"$group" : {"_id" : "$user_id_str", "tweets": { "$push": "$$ROOT" }, 'total_tweets': {"$sum": 1}, "user_object": { "$first": "$user" }}},
    {"$out" : "tweets_filtered" }
    ])
draft.collection_names() #this works! 



#apply the above to tweets_LEFT collection - EXCEEDS MEMORY!! 
tweets_LEFT.aggregate([
	{"$match": {"user.followers_count": {"$gte": 25}, "user.statuses_count": {"$gte": 100}, "lang": "en"}},
    {"$group" : {"_id" : "$user_id_str", "tweets": { "$push": "$$ROOT" }, 'total_tweets': {"$sum": 1}, "user_object": { "$first": "$user" }}},
    {"$out" : "tweets_filtered" }
    ], allowDiskUse = True)
db.collection_names() 
## trying to create a tweets_filtered COLLECTION IN the TWITTER_LEFT db 
## NB exceeds memory 
#OperationFailure: error opening file "/usr/local/var/mongodb/_tmp/extsort-doc-group.1": errno:24 Too many open files


## --> trying in parts: 
#first, project only the neccessary parts of the tweet object 
tweets_LEFT.aggregate([
    {"$project" : { #tweet fields to keep
     "user_id_str" : 1 , "tweets" : 1 , "user": 1, "place":1, "geo":1, "coordinates":1, "created_at":1, "full_text":1, "id":1, 
     "entities":1, "in_reply_to_user_id":1, "in_reply_to_status_id":1, "is_quote_status":1, "retweeted":1, "lang":1} },
    {"$out" : "tweets_filtered" }
    ], allowDiskUse = True)

#second, matching (filtering) and overwriting the tweets_filtered file 
db.tweets_filtered.aggregate([
	{"$match": {"user.followers_count": {"$gte": 25}, "user.statuses_count": {"$gte": 100}, "lang": "en"}},
    {"$out" : "tweets_filtered" }
    ], allowDiskUse = True)

db.tweets_filtered.count() # 8,079,657 tweets after filtering by 3 criteria 
#compare with original count of 10,603,262 tweets 
## FROM HOW MANY USERS? 

#third, group by user, overwriting the tweets_filtered file
db.tweets_filtered.aggregate([
    {"$group" : {"_id" : "$user_id_str", "tweets": { "$push": "$$ROOT" }, 'total_tweets': {"$sum": 1}, "user_object": { "$first": "$user" }}},
    #{"$out" : "tweets_filtered" }
    ], allowDiskUse = True)
## NB the third step exceeds memory - too many documents open 

#fourth, filter users to keep those who tweeted in the last 6 months, try location 



#repeat for RIGHT
#first, project only the neccessary parts of the tweet object 
tweets_RIGHT.aggregate([
    {"$project" : { #tweet fields to keep
     "user_id_str" : 1 , "tweets" : 1 , "user": 1, "place":1, "geo":1, "coordinates":1, "created_at":1, "full_text":1, "id":1, 
     "entities":1, "in_reply_to_user_id":1, "in_reply_to_status_id":1, "is_quote_status":1, "retweeted":1, "lang":1} },
    {"$out" : "tweets_filtered" }
    ], allowDiskUse = True)

#second, matching (filtering) and overwriting the tweets_filtered file 
db.tweets_filtered.aggregate([
	{"$match": {"user.followers_count": {"$gte": 25}, "user.statuses_count": {"$gte": 100}, "lang": "en"}},
    {"$out" : "tweets_filtered" }
    ], allowDiskUse = True)

db.tweets_filtered.count() #5,138,832
#compare with original count of 9,135,838 tweets
## FROM HOW MANY USERS? 



#third, group by user, overwriting the tweets_filtered file
db.tweets_filtered.aggregate([
    {"$group" : {"_id" : "$user_id_str", "tweets": { "$push": "$$ROOT" }, 'total_tweets': {"$sum": 1}, "user_object": { "$first": "$user" }}},
    #{"$out" : "tweets_filtered" }
    ], allowDiskUse = True)

#fourth, filter users to keep those who tweeted in the last 6 months, try location 




####################################################################################
#### filtering by most recent tweet ####

#create list of ids for later - NOT NEEDED?? 
mylist = []
cursor = db.tweets_filtered.find(projection='id')
for dictionary in cursor: 
    #print(type(i)) #dict
    for item in dictionary:
        value = dictionary['_id']
        mylist.append(value)
len(mylist) # 8079657 for left - same as the length of tweets
#5138832 for right - same as the length of tweets
mylist #list of strings 



#save cursor results to dictionary 
projection = ["id", "created_at", "user_id_str"] #keep only the relevant fields
cursor = db.tweets_filtered.find(projection=projection) 
list_of_dicts = []
for item in cursor:
    list_of_dicts.append(item)
len(list_of_dicts) #list of dicts, length for left = 8079657 dict objects
#len for right = 5138832 

#save list of dictionaries to pd df 
df = pd.DataFrame(list_of_dicts)
df.head()
#df2 = pd.DataFrame.from_dict(list_of_dicts, orient='index', columns=["tweet_id", "created_at", "user_id"])

#df.to_csv('df_LEFT_dates.csv')
df.to_csv('df_RIGHT_dates.csv')

df = pd.read_csv('df_RIGHT_dates.csv', index_col=0)
df.head()

#df_test = df[0:200] #has at least tow users in it 
#df_test
#filter created_at field of df by 

groupby = df.groupby(['user_id_str'], as_index=False)
#groupby.groups
groupby.describe()
#create dataframe 'latest', which we will loop through to filter by created_at date 
latest = groupby['created_at'].max() #this shows the LATEST/most recent created_at date for groups
type(latest) #pd series 
latest.head()
######
latest.tail()####





#set index of df to make looping through rows simpler 
latest['user_id_index'] = latest['user_id_str']
latest=latest.set_index('user_id_index')
latest.head()
len(latest.user_id_str) #48035 unique users for left; 37735 for right

#create another column in df, with date/time in datetime format 
def to_datetime(datestring):
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1])
#create new column 
latest['most_recent_datetime']= 'NaN' #as a placeholder 
for user in latest['user_id_str']: 
    date = latest.loc[[user], ['created_at']] 
    date = date.iloc[0]['created_at'] #extract string value from object
    latest.loc[[user], ['most_recent_datetime']] = to_datetime(date)
latest.head()

#eg
#minimum = to_datetime(latest['created_at'].min())

#create date 6 months ago for comparison 
d = datetime(2019, 10, 7, 12) #2019-10-07 12:00:00

#trial = latest.loc[[4667], ['most_recent_datetime']]
#trial = trial.iloc[0]
#trial
#trial < d 

users_to_delete=[]
length = len(latest.user_id_str) 
counter=0
for user in latest['user_id_str']: 
    counter += 1
    date = latest.loc[[user], ['most_recent_datetime']] 
    date = date.iloc[0]['most_recent_datetime'] #extract string value from object
    print(f'checking user {counter} out of {length}')
    if date < d: # if latest tweet was made more than 6 months ago, 
        # add user_id_str to users_to_delete
        user_id = latest.loc[[user], ['user_id_str']] 
        user_id = user_id.iloc[0]['user_id_str'] #extract string value from df object
        users_to_delete.append(user_id)

len(users_to_delete) #29807 to delete from LEFT; 19708 to delete from RIGHT
#latest['most_recent_datetime'].min() #'Fri Apr 19 14:13:15 +0000 2019'
#datetime.datetime(2007, 11, 14, 9, 14, 52)


#with open('users_to_delete_LEFT.txt', 'w') as f:
with open('users_to_delete_RIGHT.txt', 'w') as f:
    for item in users_to_delete:
        f.write("%s\n" % item)

#update the saved df 
#latest.to_csv('df_LEFT_dates_by_user.csv')
latest.to_csv('df_RIGHT_dates_by_user.csv')




#finally, from tweets_filtered collection, delete users whose user_id_str is in users_to_delete_LEFT.txt  
#for both LEFT and RIGHT 

#FOR LEFT 
with open('users_to_delete_LEFT.txt', 'r') as f:
    users_to_delete2 = f.read().splitlines()
len(users_to_delete2) #29802

db = client['TWITTER_LEFT']  
db.collection_names()

#check that comparisin works
users_to_delete2[0] #example id (non-existent) '1234'
'1234' in users_to_delete2 #True 

result = db.tweets_filtered.delete_many(
    {"user_id_str": {"$in": users_to_delete2}})
print ("deleted count:", result.deleted_count)

#new desciptive stats
db.tweets_filtered.count() #3,135,463 tweets
len(db.tweets_filtered.distinct("user_id_str")) # 18,228 unique users


#FOR RIGHT
with open('users_to_delete_RIGHT.txt', 'r') as f:
    users_to_delete2 = f.read().splitlines()
len(users_to_delete2) #19708

db = client['TWITTER_RIGHT']  

result = db.tweets_filtered.delete_many(
    {"user_id_str": {"$in": users_to_delete2}})
print ("deleted count:", result.deleted_count)

#new descriptive stats 
db.tweets_filtered.count() #2,350,745 tweets
len(db.tweets_filtered.distinct("user_id_str")) # 18,027 unique users




#### finally, filter out tweets from elites ####
## create user_id cokumn in my_elites.csv
my_elites = pd.read_csv('my_elites.csv', index_col=0)
my_elites.head()
my_elites['user_id'] = 'NaN' ##as a placeholder 
#api auth
auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#loop through my_elites
for twitter_name in my_elites.index: 
    screen_name = '@'+twitter_name
    id = api.get_user(screen_name).id
    my_elites.loc[[twitter_name], ['user_id']] = id

my_elites.head()

my_elites.to_csv('my_elites.csv')
type(elites[0])

#create list of elite ids
elites = list(my_elites['user_id'])
123456789 in elites # currently item needs to be an integer
len(elites) #420
elites = [str(i) for i in elites] #converting each item to string
elites
type(elites[0]) #str
'123456789' in elites #True 

#delete users who are in elites list form db
#1. LEFT 
db = client['TWITTER_LEFT']  

result = db.tweets_filtered.delete_many(
    {"user_id_str": {"$in": elites}})
print ("deleted count:", result.deleted_count) #585

#new descriptive stats 
db.tweets_filtered.count() # 3,134,878 tweets
len(db.tweets_filtered.distinct("user_id_str")) # 18,225 unique users


#2. RIGHT
db = client['TWITTER_RIGHT']  

result = db.tweets_filtered.delete_many(
    {"user_id_str": {"$in": elites}})
print ("deleted count:", result.deleted_count) #400

#new descriptive stats 
db.tweets_filtered.count() #2,350,345 tweets
len(db.tweets_filtered.distinct("user_id_str")) # 18,025 unique users


#close connection to MongoDB
client.close()



 
