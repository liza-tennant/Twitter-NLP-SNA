# Twitter-NLP-SNA
This is the code used in my MPhil project at the University of Cambridge, analysing political behaviour and communication on Twitter using Social Network Analysis and Natural Language Processing. 

Note: 
All code is executed in IPython, hence executing a line such as '>>> list_name' prints out the entire list titled 'list_name', without requiring a 'print(list_name)' statement. 

## This collection of code does the following: 
  1. parse in a pre-made csv file of elites (politicians, 
  2. connect to the Twitter API (using a private set of keys, which will need to be re-created if this code were to be replicated) 
  3. collect all the followers of each of the elites
  4. build a network of elites and theior followers 
  5. split the network up into LEFT and RIGHT (remove overlapping/central nodes)
  6. randomly sample 100,000 users from each network 
  7. collect 200 most recent tweets from each of the users in LEFT and RIGHT networks, saving into MongoDB database 
  8. filter the users in each sample by activity 
  9. 
  10. 
  
## Packages required: 
- import pymongo
- from pymongo import MongoClient
- import json 
- import keys 
-- #this is a file with my keys for the Twitter API - will need to be re-created by anyone willing to replicate API access, and their own keys will need to be obtained from the Twitter developers website
- import pandas as pd
- import tweepy
- import timeit
- import time
- import pprint
- import datetime
- from datetime import datetime, timedelta
- from email.utils import parsedate_tz
