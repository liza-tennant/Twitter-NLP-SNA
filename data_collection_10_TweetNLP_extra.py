"""
data_collection_13_TweetNLP_without_Pronouns.py 

1 - create the neccessary lists 
2 - compute proprtions, excluding pronouns
3 - save results for one side
4 - join together LEFT and RIGHT results dfs to import into R for analysis
5 - add centrality metrics to this new df
6 - run additional analyses to calcualte length of tweets on LEFT vs RIGHT
7 - run additional analyses to calcualte # of pairs of Proper Nouns on LEFT vs RIGHT


@author: lizakarmannaya
"""

import pandas as pd
import os 
import glob
import csv
import collections
import matplotlib.pyplot as plt
import re
from scipy import stats 
from statistics import mean, stdev 
from math import sqrt


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


####################################################################################
#### 6 - run additional analyses to calcualte length of tweets on LEFT vs RIGHT ####
####################################################################################
os.chdir(os.path.expanduser("~"))
#os.chdir('ark-tweet-nlp-0.3.2/outputs_conll/LEFT') 
os.chdir('ark-tweet-nlp-0.3.2/outputs_conll/RIGHT') #CHANGE to LEFT/RIGHT

results =[] 
errors_triple = [] 
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
    df = pd.DataFrame(index=range(number_of_tweets), columns=['length_of_tweet'])

    with open(txt_file, 'r') as f:
        for tweet in f.read().split('\n\n')[:-1]: #for every tweet from this user, minus the last blank line
            index += 1

            tags_in_tweet = []
            lines = tweet.split('\n') #create iterable with every triple of tab-separasted tags            
            lines_split = [x.split('\t') for x in lines] #this is now a list of 3 items
            for triple in lines_split: #triple = [word, tag, confidence]
                try: 
                    tags_in_tweet.append(triple[1]) #save each tag into a list of all tags_in_tweet
                except IndexError as e: 
                    errors_triple.append({user_id: {tweet: e}})
                    
            length_of_tweet = len(tags_in_tweet)

            #add these values to a df - once for every tweeet
            try:
                df['length_of_tweet'].values[index]=length_of_tweet
            except IndexError as e: #to catch empty line/triple at the end of the file 
                errors_tweet.append({user_id: {tweet: e}})

    #create dictionary of mean length for every user 
    d={'user_id_str':user_id, 'side':'RIGHT', 'mean_length_of_tweet':df['length_of_tweet'].mean()}
    #append this dict to list of results for all users 
    results.append(d)

    print(f'finished file {counter} out of 17789 LEFT/16496 RIGHT')

results = pd.DataFrame(results)  
results.tail()

os.chdir(os.path.expanduser("~"))
#results.to_csv('RESULTS_LEFT_lenght_of_tweet.csv')
results.to_csv('RESULTS_RIGHT_lenght_of_tweet.csv')


## now compare means 
LEFT_length = pd.read_csv('RESULTS_LEFT_lenght_of_tweet.csv', index_col=0)
RIGHT_length = pd.read_csv('RESULTS_RIGHT_lenght_of_tweet.csv', index_col=0)

left_length = LEFT_length['mean_length_of_tweet']
right_length = RIGHT_length['mean_length_of_tweet']


mean(left_length) #19.480082105855516
stdev(left_length) #7.357105633766712
plt.hist(left_length)

mean(right_length) #16.779441834916284
stdev(right_length) #8.263149432731872
plt.hist(right_length)


stats.ttest_ind(left_length, right_length) #statistic=32.006239762664805, pvalue=1.6440804657774395e-221
stats.ttest_ind(left_length, right_length, equal_var = False) #statistic=31.867081932487817, pvalue=1.6076753247244913e-219

cohens_d = (mean(left_length) - mean(right_length)) / (sqrt((stdev(left_length) ** 2 + stdev(right_length) ** 2) / 2))
cohens_d #0.34520672327581176

degrees_of_freedom = len(left_length) + len(right_length) - 1
degrees_of_freedom #34283

#--> on average, the length of RIGHT tweets (M=16.8, SD=8.3) was sig. shorter than the length of LEFT tweets (M=19.5, SD=7.4) (t(34238)=31.867, p=1.61e-219, Cohen's d=0.345)



####################################################################################
#### 7 - run additional analyses to calcualte # of pairs of Proper Nouns on LEFT vs RIGHT ####
####################################################################################
os.chdir(os.path.expanduser("~"))
#os.chdir('ark-tweet-nlp-0.3.2/outputs_conll/LEFT') 
os.chdir('ark-tweet-nlp-0.3.2/outputs_conll/RIGHT') 
#os.listdir()

#re-define PN_tags, special_chars and open_class_words as above 


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
    #create dataframe of desired length - for each user 
    df = pd.DataFrame(index=range(number_of_tweets), columns=['PN_pairs_total', 'PN_pairs_per_tweet'])
    PN_pairs = 0 #list of integers = # of PN pairs in every tweet

    with open(txt_file, 'r') as f:
        
        for tweet in f.read().split('\n\n')[:-1]: #for every tweet from this user, minus the last blank line
            index += 1
            nouns_in_tweet = [] #create new list of noun tags in tweet
            propernouns_in_tweet = []
            pronouns_in_tweet = []
            tags_in_tweet = []
            lines = tweet.split('\n') #create iterable with every triple of tab-separasted tags            
            lines_split = [x.split('\t') for x in lines] #this is now a list of 3 items
            
            propernoun_counter = 0

            for triple in lines_split: #triple = [word, tag, confidence]
                try: 
                    tags_in_tweet.append(triple[1]) #save each tag into a list of all tags_in_tweet
                    if triple[1].lower() in PN_tags: #if tagged as proper noun 
                        propernouns_in_tweet.append(triple[1])
                        propernoun_counter += 1
                        if propernoun_counter >1:
                            PN_pairs += 1 #this user used a pair of Proper Nouns next to each other
                            propernoun_counter = 0
                    else:
                        propernoun_counter = 0
                except IndexError as e: #to catch empty line/triple at the end of the file 
                    errors_triple.append({user_id: {tweet: e}})
  
    #create dictionary of mean proportions for every user 
    d={'user_id_str':user_id, 'side':'RIGHT', 'PN_pairs_total':int(PN_pairs), 'PN_pairs_per_tweet':int(PN_pairs)/number_of_tweets}
    #append this dict to list of results for all users 
    results.append(d)

    print(f'finished file {counter} out of 17789 LEFT/16496 RIGHT')


results = pd.DataFrame(results)
results.tail()

os.chdir(os.path.expanduser("~"))
#results.to_csv('RESULTS_LEFT_PN_pairs.csv')
results.to_csv('RESULTS_RIGHT_PN_pairs.csv')


## now compare means 
LEFT_pairs = pd.read_csv('RESULTS_LEFT_PN_pairs.csv', index_col=0)
RIGHT_pairs = pd.read_csv('RESULTS_RIGHT_PN_pairs.csv', index_col=0)

left_pairs = LEFT_pairs['PN_pairs_per_tweet']
right_pairs = RIGHT_pairs['PN_pairs_per_tweet']


mean(left_pairs) #0.17524338794135574
stdev(left_pairs) #0.20630986998362993
plt.hist(left_pairs)

mean(right_pairs) #0.19582607646704403
stdev(right_pairs) #0.28227161458250244
plt.hist(right_pairs)


stats.ttest_ind(left_pairs, right_pairs) #statistic=-7.746664061474904, pvalue=9.692959716416872e-15
stats.ttest_ind(left_pairs, right_pairs, equal_var = False) #statistic=-7.658528709630229, pvalue=1.9371635625573803e-14

cohens_d = (mean(left_pairs) - mean(right_pairs)) / (sqrt((stdev(left_pairs) ** 2 + stdev(right_pairs) ** 2) / 2))
cohens_d #-0.08325467026744812

degrees_of_freedom = len(left_pairs) + len(right_pairs) - 1
degrees_of_freedom #34283

#--> on average, the RIGHT used more Proper Noun pairs per tweet (M=19.5%, SD=28.2%) 
# than the LEFT  (M=17.5%, SD=20.6%) (t(34238)=7.747, p=9.69e-15, Cohen's d= -0.083)
