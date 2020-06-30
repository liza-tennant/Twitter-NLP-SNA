"""
data_collection_13_TwetNLP_without_Pronouns.py 

1 - create the neccessary lists 
2 - compute proprtions, excluding pronouns
3 - save results for one side
4 - join together LEFT and RIGHT results dfs to import into R for analysis
5 - add centrality metrics to this new df

@author: lizakarmannaya
"""

import pandas as pd
import os 
import glob
import csv
import collections
import matplotlib.pyplot as plt
import re


####################################################
#### 1 - create the neccessary lists ####
####################################################

Noun_tags = ['N', 'S', 'L']
PN_tags = ['^', 'Z', 'M'] #proper nouns
Pronoun_tags = ['O']

special_chars = ['#', '@', '~', 'U', 'E', ','] #keepng 'G' (abbreviations) and '$' (numerals)
open_class_words = ['N', 'O', 'S', '^', 'Z', 'L', 'M', 'V', 'A', 'R', '!']

first_pers_pronouns = ['i', 'we', 'me','us','mine','ours','my','our','myself','ourselves'] 
second_pers_pronouns = ['you','yours','your','yourself','yourselves']
third_pers_pronouns = ['he', 'she', 'it', 'they', 'her','him','them','hers','his','its','theirs','his','their','herself','himself','itself','themselves']
other_pronouns = ['all','another','any','anybody','anyone','anything','both','each','either','everybody','everyone','everything','few','many','most','neither','nobody','none','noone','nothing','one','other','others','several','some','somebody','someone','something','such','that','these','this','those','what','whatever','which','whichever','who','whoever','whom','whomever','whose','as','that','what','whatever','thou','thee','thy','thine','ye','eachother','everybody','naught','nought','somewhat','thyself','whatsoever','whence','where','whereby','wherever']

pronouns = first_pers_pronouns + second_pers_pronouns + third_pers_pronouns + other_pronouns



####################################################
#### 2 - compute proprtions, excluding pronouns ####
##re-run for LEFT/RIGHT from here ##################
####################################################
os.chdir(os.path.expanduser("~"))
os.chdir('ark-tweet-nlp-0.3.2/outputs_conll/LEFT') #CHANGE to LEFT/RIGHT
#os.listdir()


results =[] #list of dicts to save each user's reslts into
errors_triple = [] #list of dicts to save errors into
errors_tweet = []

counter = 0
for txt_file in glob.glob("*.txt"): 
    index = -1
    counter+=1

    #extract user_id from file name 
    user_id = txt_file.split("tweets_")[1] 
    user_id = user_id.split(".txt")[0]

    with open(txt_file, 'r') as f:
        number_of_tweets = len(f.read().split('\n\n')[:-1]) #minus the last blank line
    #create dataframe of desired length 
    df = pd.DataFrame(index=range(number_of_tweets), columns=['N_nopronouns_proportion', 'N_nopronouns_proportion_filtered', 'N_nopronouns_open_proportion', 'PN_proportion', 'PN_proportion_filtered', 'PN_open_proportion', 'N_PN_proportion', 'N_PN_proportion_filtered', 'N_PN_open_proportion', 'Pronoun_proportion', 'Pronoun_proportion_filtered', 'Pronoun_open_proportion', 'Objects_proportion', 'Objects_proportion_filtered', 'Objects_open_proportion'])

    with open(txt_file, 'r') as f:
        for tweet in f.read().split('\n\n')[:-1]: #for every tweet from this user, minus the last blank line
            index += 1
            nouns_in_tweet = [] #create new list of noun tags in tweet
            propernouns_in_tweet = []
            pronouns_in_tweet = []
            tags_in_tweet = []
            lines = tweet.split('\n') #create iterable with every triple of tab-separasted tags            
            lines_split = [x.split('\t') for x in lines] #this is now a list of 3 items
            for triple in lines_split: #triple = [word, tag, confidence]
                try: 
                    tags_in_tweet.append(triple[1]) #save each tag into a list of all tags_in_tweet
                    if triple[1] in Noun_tags: #if tagged as noun
                        if triple[0].lower() not in pronouns: #if word itself not in pronouns list - multiversing 
                            nouns_in_tweet.append(triple[1])
                        elif triple[0].lower() in pronouns:
                            pronouns_in_tweet.append(triple[1]) #to add the pronouns misclassified as pronouns to pronouns_in_tweet
                    elif triple[1].lower() in PN_tags: #if tagged as proper noun 
                        propernouns_in_tweet.append(triple[1])
                    elif triple[1].lower() in Pronoun_tags: #if tagged as pronoun
                        pronouns_in_tweet.append(triple[1])
                except IndexError as e: #to catch empty line/triple at the end of the file 
                    errors_triple.append({user_id: {tweet: e}})
                    
            
            #N_nopronouns_proportion
            N_nopronouns_proportion = round((len(nouns_in_tweet)/len(tags_in_tweet)), 4)
            #N_nopronouns_proportion_filtered
            tags_filtered = [x for x in tags_in_tweet if x not in special_chars]
            if len(tags_filtered) > 0:
                N_nopronouns_proportion_filtered = round((len(nouns_in_tweet)/len(tags_filtered)), 4)
            else: 
                N_nopronouns_proportion_filtered = 0 #to avoid dividing by 0 if tags_filtered is empty

            #N_nopronouns_open_proportion
            tags_open_class = [x for x in tags_in_tweet if x in open_class_words]
            if len(tags_open_class) > 0:
                N_nopronouns_open_proportion = round((len(nouns_in_tweet)/len(tags_open_class)), 4)
            else: 
                N_nopronouns_open_proportion = 0 #to avoid dividing by 0 if tags_filtered is empty

            
            #PN_proportion
            PN_proportion = round((len(propernouns_in_tweet)/len(tags_in_tweet)), 4)
            #PN_proportion_filtered 
            if len(tags_filtered) > 0:
                PN_proportion_filtered = round((len(propernouns_in_tweet)/len(tags_filtered)), 4)
            else: 
                PN_proportion_filtered = 0 #to avoid dividing by 0 if tags_filtered is empty
            #PN_open_proportion
            if len(tags_open_class) > 0:
                PN_open_proportion = round((len(propernouns_in_tweet)/len(tags_open_class)), 4)
            else: 
                PN_open_proportion = 0 #to avoid dividing by 0 if tags_filtered is empty


            #N_PN_proportion - Nouns + Propernouns 
            N_PN_proportion = round((len(nouns_in_tweet + propernouns_in_tweet)/len(tags_in_tweet)), 4)
            #N_PN_proportion_filtered
            if len(tags_filtered) > 0:
                N_PN_proportion_filtered = round((len(nouns_in_tweet + propernouns_in_tweet)/len(tags_filtered)), 4)
            else: 
                N_PN_proportion_filtered = 0 #to avoid dividing by 0 if tags_filtered is empty
            #N_PN_open_proportion
            if len(tags_open_class) > 0:
                N_PN_open_proportion = round((len(nouns_in_tweet + propernouns_in_tweet)/len(tags_open_class)), 4)
            else: 
                N_PN_open_proportion = 0 #to avoid dividing by 0 if tags_filtered is empty


            #Pronoun_proportion 
            Pronoun_proportion = round((len(pronouns_in_tweet)/len(tags_in_tweet)), 4)
            #Pronoun_proportion_filtered 
            if len(tags_filtered) > 0:
                Pronoun_proportion_filtered = round((len(pronouns_in_tweet)/len(tags_filtered)), 4)
            else: 
                Pronoun_proportion_filtered = 0 #to avoid dividing by 0 if tags_filtered is empty
            #Pronoun_open_proportion
            if len(tags_open_class) > 0:
                Pronoun_open_proportion = round((len(pronouns_in_tweet)/len(tags_open_class)), 4)
            else: 
                Pronoun_open_proportion = 0 #to avoid dividing by 0 if tags_filtered is empty


            #Objects_proportion = all together: Nouns + Propenouns + Pronouns 
            Objects_proportion = round((len(nouns_in_tweet + propernouns_in_tweet + pronouns_in_tweet)/len(tags_in_tweet)), 4)
            #Objects_proportion_filtered
            if len(tags_filtered) > 0:
                Objects_proportion_filtered = round((len(nouns_in_tweet + propernouns_in_tweet + pronouns_in_tweet)/len(tags_filtered)), 4)
            else: 
                Objects_proportion_filtered = 0 #to avoid dividing by 0 if tags_filtered is empty
            #Objects_open_proportion
            if len(tags_open_class) > 0:
                Objects_open_proportion = round((len(nouns_in_tweet + propernouns_in_tweet + pronouns_in_tweet)/len(tags_open_class)), 4)
            else: 
                Objects_open_proportion = 0 #to avoid dividing by 0 if tags_filtered is empty



            #add these values to a df - once for every tweeet
            try:
                #df['N_count'].values[index]=len(nouns_in_tweet)
                df['N_nopronouns_proportion'].values[index]=N_nopronouns_proportion
                df['N_nopronouns_proportion_filtered'].values[index]=N_nopronouns_proportion_filtered                
                df['N_nopronouns_open_proportion'].values[index]=N_nopronouns_open_proportion

                df['PN_proportion'].values[index]=PN_proportion
                df['PN_proportion_filtered'].values[index]=PN_proportion_filtered                
                df['PN_open_proportion'].values[index]=PN_open_proportion

                df['N_PN_proportion'].values[index]=N_PN_proportion
                df['N_PN_proportion_filtered'].values[index]=N_PN_proportion_filtered                
                df['N_PN_open_proportion'].values[index]=N_PN_open_proportion

                df['Pronoun_proportion'].values[index]=Pronoun_proportion
                df['Pronoun_proportion_filtered'].values[index]=Pronoun_proportion_filtered                
                df['Pronoun_open_proportion'].values[index]=Pronoun_open_proportion

                df['Objects_proportion'].values[index]=Objects_proportion
                df['Objects_proportion_filtered'].values[index]=Objects_proportion_filtered                
                df['Objects_open_proportion'].values[index]=Objects_open_proportion

            except IndexError as e: #to catch empty line/triple at the end of the file 
                errors_tweet.append({user_id: {tweet: e}})

    #create dictionary of mean proportions for every user 
    d={'user_id_str':user_id, 'side':'LEFT', 'mean_N_nopronouns_proportion':df['N_nopronouns_proportion'].mean(), 'mean_N_nopronouns_proportion_filtered':df['N_nopronouns_proportion_filtered'].mean(), 'mean_N_nopronouns_open_proportion':df['N_nopronouns_open_proportion'].mean(), 
    'mean_PN_proportion':df['PN_proportion'].mean(), 'mean_PN_proportion_filtered':df['PN_proportion_filtered'].mean(), 'mean_PN_open_proportion':df['PN_open_proportion'].mean(), 
    'mean_N_PN_proportion': df['N_PN_proportion'].mean(), 'mean_N_PN_proportion_filtered':df['N_PN_proportion_filtered'].mean(), 'mean_N_PN_open_proportion':df['N_PN_open_proportion'].mean(),
    'mean_Pronoun_proportion':df['Pronoun_proportion'].mean(), 'mean_Pronoun_proportion_filtered':df['Pronoun_proportion_filtered'].mean(), 'mean_Pronoun_open_proportion':df['Pronoun_open_proportion'].mean(),
    'mean_Objects_proportion':df['Objects_proportion'].mean(), 'mean_Objects_proportion_filtered':df['Objects_proportion_filtered'].mean(), 'mean_Objects_open_proportion':df['Objects_open_proportion'].mean()
    }
    #append this dict to list of results for all users 
    results.append(d)

    print(f'finished file {counter} out of 17789 LEFT/16496 RIGHT')


len(results) #17789 for LEFT, 16496 for RIGHT
len(errors_triple) #6 for LEFT, 5 for RIGHT 
len(errors_tweet) #0 for LEFT, 0 for RIGHT


########################################
#### 3 - save results for one side #####
########################################
results = pd.DataFrame(results)  
results.tail()
results.to_csv('RESULTS_LEFT_multiverse_4.csv')
#saved in 'ark-tweet-nlp-0.3.2/outputs_conll/LEFT/RESULTS_LEFT_multiverse_4.csv' 
#saved in 'ark-tweet-nlp-0.3.2/outputs_conll/RIGHT/RESULTS_RIGHT_multiverse_4.csv'

errors_triple = pd.DataFrame(errors_triple)
errors_triple
errors_triple.to_csv('ERRORS_LEFT_multiverse_4.csv')


########################################################################
#### 4 - join together LEFT and RIGHT results dfs to import into R for analysis
########################################################################

os.chdir(os.path.expanduser("~"))
os.listdir()
df1 = pd.read_csv('ark-tweet-nlp-0.3.2/outputs_conll/LEFT/RESULTS_LEFT_multiverse_4.csv', index_col=0)
df1.head()
df1 #17788 rows × 17 columns
df2 = pd.read_csv('ark-tweet-nlp-0.3.2/outputs_conll/RIGHT/RESULTS_RIGHT_multiverse_4.csv', index_col=0)
df2.head()
df2 #16496 rows × 17 columns
df_results = pd.concat([df1, df2], ignore_index=True)
df_results #34284 rows × 5 columns
df_results.iloc[17786:17800,] #checked that they joined together correctly, ignoring the header in df2
df.head()
df_results.to_csv('RESULTS_df_multiverse_4.csv')







########################################################################
#### 5 - add centrality metrics to this new df #########################
# NB this was not done for multiverse_4 - I just copied the centrality metrics from earlier 
########################################################################


#### now modify code from data_collection_10 to add hubs centrality back into 'RESULTS_df_multiverse_3.csv'
import networkx as nx
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import fnmatch
from scipy.stats import skew, kurtosis, mode 

os.chdir(os.path.expanduser("~"))

L = nx.read_pajek('largest_wcc_LEFT_directed.net')
R = nx.read_pajek('largest_wcc_RIGHT_directed.net')
#this imports them as multigraph types --> convert to DiGraph
L = nx.DiGraph(L)
R = nx.DiGraph(R)

L.number_of_nodes() #822781
R.number_of_nodes() #1542256

#compute out-degree centrality + hubs/authorities metrics for enitre wLCC graphs 
out_degree_centrality_L = nx.out_degree_centrality(L)
out_degree_centrality_R = nx.out_degree_centrality(R)

hits_L_hubs, hits_L_authorities = nx.hits(L)
hits_R_hubs, hits_R_authorities = nx.hits(R)

#find values for users in my sub-sample & add these to df 
df = pd.read_csv('RESULTS_df_multiverse_3.csv', index_col=0)
df['out_degree_centrality'] = 'NaN'
df['authorities']='NaN'
df['hubs'] = 'NaN'
df.head()
df = df.reset_index()

errors2 = []
for index in df.index:
    user_id = df['user_id_str'].values[index] #NB this is a numpy integer
    if df['side'].values[index] == 'LEFT':
        try: 
            df['out_degree_centrality'].values[index] = out_degree_centrality_L[str(user_id)]
            df['authorities'].values[index] = hits_L_authorities[str(user_id)]
            df['hubs'].values[index] = hits_L_hubs[str(user_id)]
        except KeyError as e: 
            errors2.append(e)
            print(e)
            df['out_degree_centrality'].values[index] = 'NaN'
            df['authorities'].values[index] = 'NaN'
            df['hubs'].values[index]='NaN'

    elif df['side'].values[index] == 'RIGHT': 
        try:
            df['out_degree_centrality'].values[index] = out_degree_centrality_R[str(user_id)]
            df['authorities'].values[index] = hits_R_authorities[str(user_id)]
            df['hubs'].values[index] = hits_R_hubs[str(user_id)]
        except KeyError as e: 
            errors2.append(user_id)
            print(e)
            df['out_degree_centrality'].values[index] = 'NaN'
            df['authorities'].values[index] = 'NaN'
            df['hubs'].values[index] = 'NaN'
    else:
        print('error')

    print(f'finished {index} out of 34284')


df.head()
df.shape
errors2

df['user_id_str_index'] = df['user_id_str']
df = df.set_index('user_id_str_index') #using twitter_name = screen_name as index for later

df.head()
df = df.drop(columns='index')

df.to_csv('RESULTS_df_multiverse_3_norponouns.csv')
