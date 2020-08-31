"""
data_collection_7_tweets_to_mongo.py 

This code goes through all followers in  filters them by activity

1 - authentication for API 
2 - connect to MongoDB
3 - read in twitter user_ids (and add to Mongodb if first run)
4 - collect 200 most recent tweets from each account in db 
5 - cleaning users

@author: lizakarmannaya; adapted from https://gist.github.com/gdsaxton/0702e7c716e01c0306a3321428b7a79a 
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

######### 1 - authenticaion #################################################
auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)



######### 2 - connect to MongoDB #################################################

#NB remember to run in terminal: mongod 
# + see notes on Mac 

#source for below: https://gist.github.com/gdsaxton/0702e7c716e01c0306a3321428b7a79a
#Below we are simply making a connection to MongoDB, creating our database, 
# then our database tables, then indexes on those tables. Note that, if this 
# is the first time you’re running this code, the database and tables and indexes 
# will be created; if not, the code will simply access the database and tables. 
# Note: MongoDB refers to database tables as ‘collections’ and to columns or variables as ‘fields.’

client = MongoClient() #default host and port
#define mongodb database - creates new one if it does not exist 
#db = client['TWITTER_LEFT']  ## NB REPEAT for RIGHT
db = client['TWITTER_RIGHT']  ## NB REPEAT for RIGHT

# CREATE ACCOUNTS COLLECTION (TABLE) IN YOUR DATABASE FOR TWITTER ACCOUNT-LEVEL DETAILS
accounts = db['accounts'] #this is a collection 
# NOT DONE! using _id distinct instead. CREATE AN INDEX ON THE COLLECTION TO AVOID INSERTION OF DUPLICATES
#db.accounts.create_index([('user_id', pymongo.ASCENDING)], unique=True)

# SHOW INDEX ON ACCOUNTS TABLE
list(db.accounts.index_information())

#SHOW NUMBER OF ACCOUNTS IN TABLE
accounts.count() #100000 after loading in


# DEFINE COLLECTION (TABLE) WHERE YOU'LL INSERT THE TWEETS
tweets = db['tweets']

# CREATE UNIQUE INDEX FOR TABLE (TO AVOID DUPLICATES)
#db.tweets.create_index([('id_str', pymongo.ASCENDING)], unique=True)

#SHOW INDEX ON TWEETS COLLECTION
list(db.tweets.index_information())

#SHOW NUMBER OF TWEETS IN TABLE
tweets.count()

#TO SEE LIST OF CURRENT MONGODB DATABASES
client.database_names()

#TO SEE LIST OF COLLECTIONS IN THE *TWITTER* DATABASE
db.collection_names()



#testing the importing of df
#df = pd.read_csv('sample_draft.csv') 
#df = pd.read_csv('sample1_LEFT.csv', header=None) #REPEAT FOR RIGHT
#df = pd.read_csv('sample1_RIGHT.csv', header=None) 
#df.rename(columns={0: '_id'}, inplace=True)
#df.columns
#records = json.loads(df.T.to_json()).values()
#records
#len(records)
#for id in records:
    #print(id)


#FOR DROPPPING COLLECTION
#db.accounts.drop()

#db.accounts.find().count()
#db.accounts
#db.accounts.count()


######### 3 - read in twitter user_ids (and add to Mongodb if first run) #################################################

## NB sub in 'sample1.csv' for name of CSV file with user_ids 

# IF ACCOUNTS COLLECTION IS EMPTY READ IN CSV FILE AND ADD TO MONGODB
if db.accounts.find().count() < 1:
    #df = pd.read_csv('sample1_LEFT.csv', header=None) #REPEAT FOR RIGHT
    df = pd.read_csv('sample1_RIGHT.csv', header=None) 
    df.rename(columns={0: '_id'}, inplace=True)
    records = json.loads(df.T.to_json()).values()
    print("No account data in MongoDB, attempting to insert", len(records), "records")
    try:
        db.accounts.insert_many(records)
    except pymongo.errors.BulkWriteError as e:
        print('Error:', e.details, '\n')
        pass  
else:
    print("There are already", accounts.count(), "records in the *accounts* table")

#LIST ROWS IN ACCOUNTS COLLECTION
list(db.accounts.find())[:]

# CREATE LIST OF TWITTER HANDLES FOR DOWNLOADING TWEETS
twitter_accounts = db.accounts.distinct('_id') #alredy in ascending order 
print(len(twitter_accounts)) #100000
twitter_accounts #[:1]=first account in list 



######### 4 - collect tweets from all accounts in db #############################################

#define function to collect 200 tweets from all user_ids in a csv file
def collect_tweets_from_user(user_id):
    try:
        """This function collects latest 200 tweets from a users in csv file. 
        It saves tweets in MongoDB database. """
        tweets = api.user_timeline(user_id=user_id, count=200, tweet_mode='extended')
        #tweets = a json collection of 200 full-length tweets, including RTs and @s. 
        return tweets
    except Exception as e:
        print("Error reading id %s, exception: %s" % (user_id, e))
        return None 
        #pass
    #print(len(tweets))
    
    #tweets.full_text
    #can now subset resultset - e.g. tweets[0] = 1st tweet out of 200



# Loop Over Each of the user_ids in the Accounts Table and Download Tweets

start_time = timeit.default_timer()

starting_count = tweets.count() #8857828
#type(twitter_accounts) #list

#finished on index number 80323, first failed id=317928959
twitter_accounts.index(1075600656029761536) #80323
len(db.tweets.distinct('user_id_str')) #16911 --> 34685 --> 56432 --> 72054 
tweets.count() #5107609


#rate_limit=900
for s in twitter_accounts[80323:]:
    
    #SET THE DUPLICATES COUNTER FOR THIS TWITTER ACCOUNT TO ZERO
    duplicates = 0
    
    #CHECK FOR TWITTER API RATE LIMIT (900 CALLS/15-MINUTE WINDOW)
    #NB the function below has a 180 req/min limit - hence trying without it 
    #rate_limit = api.rate_limit_status()['resources']['statuses']['/statuses/user_timeline']['remaining']
    #print('\n\n', '# of remaining API calls: ', rate_limit)

    #tweet_id = str(mentions.find_one( { "query_screen_name": s}, sort=[("id_str", 1)])["id_str"])
    print('Grabbing tweets sent by user_id: ', s, '-- index number: ', twitter_accounts.index(s))
        
    #WE CAN GET 200 TWEETS PER CALL AND UP TO 3,200 TWEETS TOTAL, MEANING 16 PAGES' PER ACCOUNT 
    #print("------XXXXXX------ STARTING USER, ...estimated remaining API calls:", rate_limit) #NB definition of rate_limit has been commented out
    print("------XXXXXX------ STARTING USER")

    d = collect_tweets_from_user(s) #user_id
    #d = get_data_user_timeline_all_pages(s, page)          
    if not d:
        print("THERE WERE NO STATUSES RETURNED........MOVING TO NEXT ID")
        pass
    if type(d) == type(None): #=if could not access user statuses in collect_tweets_from_user:
        continue
    if len(d)==0:    #THIS ROW IS DIFFERENT FROM THE MENTIONS AND DMS FILES
        print("THERE WERE NO STATUSES RETURNED........MOVING TO NEXT ID")
        pass
    #if not d['statuses']:
    #    break      
    #DECREASE rate_limit TRACKER VARIABLE BY 1
    #rate_limit -= 1
    #print('.......estimated remaining API rate_limit: ', rate_limit)
    ##### WRITE THE DATA INTO MONGODB -- LOOP OVER EACH TWEET
    for entry in d:
        
        #CONVERT TWITTER DATA TO PREP FOR INSERTION INTO MONGO DB
        t = json.dumps(entry._json)
        #print('type(t)', type(t)                   #<type 'str'>
        loaded_entry = json.loads(t)
        #print(type(loaded_entry) , loaded_entry)   #<type 'dict'>
        
        #ADD THE FOLLOWING THREE VARIABLES TO THOSE RETURNED BY TWITTER API
        loaded_entry['date_inserted'] = time.strftime("%d/%m/%Y")
        loaded_entry['time_date_inserted'] = time.strftime("%H:%M:%S_%d/%m/%Y")
        loaded_entry['user_id_str'] = loaded_entry['user']['id_str']
        loaded_entry['_id'] = loaded_entry['id_str'] #set tweet id as index


        #INSERT THE TWEET INTO THE DATABASE -- UNLESS IT IS ALREADY IN THE DB
        try:
            tweets.insert_one(loaded_entry)
        except pymongo.errors.DuplicateKeyError as e:
            #print(e, '\n')
            duplicates += 1
            pass     
        
        
    print('------XXXXXX------ FINISHED USER', s, "--", len(d), "TWEETS")

    #IF THERE ARE TOO MANY DUPLICATES THEN SKIP TO NEXT ACCOUNT 
    if duplicates > 20:
        print('\n********************There are %s' % duplicates, 'duplicates....moving to next ID********************\n')
        continue        
        #break  
                
    
      


################################################################
############ COLLECTING THE REST ##############################
################################################################
twitter_accounts.index(966396905772040193) #89917
#hence collect from twitter_accounts[89917:]
len(twitter_accounts[89917:]) #10083

#db.tweets.
#data = db.author.find_one({'email' : email, 'password' : password}, {'_id': 1})








#times for the last bit only
elapsed = timeit.default_timer() - start_time
print('# of minutes: ', elapsed/60) ## of minutes:  1386.83627762855
print("Number of new tweets added this run: ", tweets.count() - starting_count) #Number of new tweets added this run:  278010
print("Number of tweets now in DB: ", tweets.count(), '\n', '\n') #Number of tweets now in DB:  9135838            

db.accounts.count()#     
db.accounts.index_information         
db.accounts.aggregate



###### PART VII: PRINT OUT NUMBER OF TWEETS IN DATABASE FOR EACH ACCOUNT ######  

for user in db.tweets.aggregate([
    {"$group":{"_id":"$user_id_str", "sum":{"$sum":1}}} 
    ]):
    print(user['_id'], user['sum'])

####simply print number of distinct user_id_str in tweets collection 
db.tweets.user_id_str.count()
len(db.tweets.distinct('user_id_str')) #79261
## save unique user_id_str
db_unique_users_LEFT=db.tweets.distinct('user_id_str')
with open('db_unique_users_LEFT.csv', 'w') as f:
    for val in db_unique_users_LEFT:
        f.write(val+'\n')
db_unique_users_RIGHT=db.tweets.distinct('user_id_str')
len(db_unique_users_RIGHT) #76931
with open('db_unique_users_RIGHT.csv', 'w') as f:
    for val in db_unique_users_RIGHT:
        f.write(val+'\n')


pipeline = [{"$group":{"_id": "user_id_str", "sum":{"$sum":1}}}]
db.tweets.aggregate(pipeline)



## trying to access the data in db
tweet_cursor = db.tweets.find({})
print(tweet_cursor.count()) #347091
user_cursor = db.tweets.distinct('user.id')
print(len(user_cursor)) #4...
for tweet in tweet_cursor:
    try:
        print('------')
        print('user_id:-', tweet["user"]["id"])
        print('text:-', tweet["full_text"])
        print('Created_at:-', tweet["created_at"])
    except:
        print("Error in Encoding")
        pass

#can retrieve individual tweets 

#to fetch all docs within a collection:
#docs = [d for d in db.collection.find()] 
accounts = [d for d in db.accounts.find()] 
accounts

connection.close()