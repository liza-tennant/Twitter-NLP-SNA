"""
data_collection_5_random_sampler.py 

This code takes an input csv (largest_cc_LEFT_nodelist_filtered.csv or 
largest_cc_RIGHTT_nodelist_filtered.csv)with user_ids (nodes from the graph), 
randomly samples 100,000 from them and saves the sample as sample1_LEFT.csv or sample1_RIGHT.csv. 

1 - draw random samples of 100000 from left CC nodelist (user_id lists) & save as sample1_<...>.csv 
2 - REPEAT FOR largest_cc_RIGHT_nodelist_filtered.csv

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

