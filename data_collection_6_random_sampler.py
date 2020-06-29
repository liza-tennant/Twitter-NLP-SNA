"""
data_collection_6_random_sampler.py 

This code goes through all followers in  filters them by activity

1 - draw random samples of 100000 from left & right CC nodelists (user_id lists)


@author: lizakarmannaya
"""

import pandas as pd
import numpy as np
import csv
from random import randrange

 
######### 1 - draw random samples of 100000 ########################################

#adapted from Sylwester & Purver (2015)

#input file
inputFile = "largest_cc_LEFT_nodelist_filtered.csv"


#output files
sample1 = "sample1_LEFT.csv"
sample2 = "sample2_LEFT.csv"
sample3 = "sample3_LEFT.csv"
sample4 = "sample4_LEFT.csv"
sample5 = "sample5_LEFT.csv"
sample6 = "sample6_LEFT.csv"
sample7 = "sample7_LEFT.csv"
sample8 = "sample8_LEFT.csv"

remainingList = "remaining_LEFT.csv"

def splitText(fileName):
    
    text = []
    for line in open(fileName, 'r'):
        text.extend(line.strip().split('\r')) 
    return text

def isInList(targetList, targetEl):

    for e in targetList:
        if e == targetEl:
            return True          
    return False 
   
def drawRandom(targetList, sample, fileName):
   
    newList = []
    for i in range(sample):
        #select random index and get element
        random_index = randrange(0,len(targetList))
        e = targetList[random_index]
        #print(e)
        #add element to a new list
        newList.append(e)
        #remove element from original list
        targetList.pop(random_index)
    #print(type(newList[0])) #<class 'str'>

    with open(fileName, 'w') as f: #wb = Same as w but opens in binary mode.
        #print(newList) #list of strings 
        #writer = csv.writer(f)
        for val in newList:
            f.write(val+'\n')
            #writer.writerow([val,])
    return newList

def filterList(originalList, sampleList):
    filteredList = []
    for e in originalList:
        result = isInList(sampleList, e)
        #print result
        if result == False:
            filteredList.append(e)
    return filteredList

def writeToFile(listWithoutSamples, fileName):
    #with open(fileName, 'wb') as f:
    #    writer = csv.writer(f, delimiter=',')
    #    for val in listWithoutSamples:
    #        writer.writerow([val])
    with open(fileName, 'w') as f:
        for val in listWithoutSamples:
            f.write(val+'\n')
    return listWithoutSamples


originalList = splitText('largest_cc_LEFT_nodelist.csv')
len(originalList) #821777, list

#the below is DONE 
#sample1 = drawRandom(originalList, 100000, 'sample1_LEFT.csv')
#sample1 = pd.read_csv('sample1_LEFT.csv', header=None)
#sample1

filtered = filterList(originalList, sample1)
len(filtered) #721777
writeToFile(filtered, remainingList) #remainingList defined above

#d = pd.read_csv('largest_cc_LEFT_nodelist.csv', header=None)
#d[0:10]















































######## 4 - drafts - try to collect 200 most recent tweets from one account #################


#from O'Reilly books - example for NASA 
nasa_tweets = api.user_timeline(user_id=11348282, count=200, tweet_mode='extended') #screen_name='nasa'
for tweet in nasa_tweets:
    print(f'{tweet.user.screen_name}:{tweet.full_text}\n')
#when 'extended' mode is specified, all tweets are returned with 'full_text' as the relevant text field 
type(nasa_tweets) #tweepy.models.ResultSet


len('NASA:On Feb. 28, @NASAEarth satellites observed reduced levels of atmospheric nitrogen dioxide over China since the coronavirus outbreak. But measurable change in one pollutant does not mean air quality is suddenly healthy. Heres why: https://t.co/2Z5juBUeEO https://t.co/97PXQBcKyh') #282

print(nasa_tweets[0]._json.keys())
print(nasa_tweets[4].truncated)
print(len(nasa_tweets[4].text)) #140
print(nasa_tweets[4].text[-20:])
print(len(nasa_tweets[4].retweeted_status.text)) #140


# Extended Tweets are identified with a root-level "truncated" boolean. 
# When true ("truncated": true), the "extended_tweet" fields should be parsed instead of the root-level fields.
status = api.statuses_lookup(id_ = ['1240342876636229632'], tweet_mode='extended')
status[0]._json.keys()
status[0].truncated #False if we use 'extended' mode above
status[0].full_text


nasa_tweets[0].user._json.keys()
len(nasa_tweets) #200


#creatng csv for test database 
list_of_ids = [11348282, 17471979] #NASA & NatGeo 
#list_of_ids.to_csv('sample_draft.csv') #can't turn list to csv

largest_cc_LEFT_nodelist = pd.read_csv('largest_cc_LEFT_nodelist.csv', header=None, index_col=0)
largest_cc_LEFT_nodelist[0:5].to_csv('sample_draft.csv')
largest_cc_LEFT_nodelist[0:5]
