"""
data_collection_13_TwetNLP_without_Pronouns.py 

1 - create the neccessary lists 
2 - compute proprtions, excluding pronouns, covid words and emojis from all
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
#pip install emoji
import emoji




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

#try spot one emoji 
'💔' in emoji.UNICODE_EMOJI


coronavirus = ['coronavirus', 'sarscov2', 'covid', 'covid19', 'covid_19', 'covid-19', 'covid2019', 'covid_2019', 'covid-2019', 'cov19', 'cov_19', 'cov-19', 'cov2019', 'cov_2019', 'cov-2019', 'cv19', 'cv_19', 'cv-19', 'cv2019', 'cv_2019', 'cv-2019', 'covid19uk', 'covid2019uk']


####################################################
#### 2 - compute proprtions, excluding pronouns, covid words and emojis from all ####
##re-run for LEFT/RIGHT from here ##################
####################################################
os.chdir(os.path.expanduser("~"))
os.chdir('ark-tweet-nlp-0.3.2/outputs_conll/RIGHT') #CHANGE to LEFT/RIGHT
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
                            if triple[0].lower() not in coronavirus: #if not covid  word 
                                if triple[0].lower() not in emoji.UNICODE_EMOJI: #if not emoji
                                    nouns_in_tweet.append(triple[1])
                    elif triple[1].lower() in PN_tags: #if tagged as proper noun 
                        if triple[0].lower() not in pronouns: #if word itself not in pronouns list - multiversing 
                            if triple[0].lower() not in coronavirus:
                                if triple[0].lower() not in emoji.UNICODE_EMOJI:
                                    propernouns_in_tweet.append(triple[1])

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


            #add these values to a df - once for every tweeet
            try:
                #df['N_count'].values[index]=len(nouns_in_tweet)
                df['N_nopronouns_proportion'].values[index]=N_nopronouns_proportion
                df['N_nopronouns_proportion_filtered'].values[index]=N_nopronouns_proportion_filtered                
                df['N_nopronouns_open_proportion'].values[index]=N_nopronouns_open_proportion

                df['PN_proportion'].values[index]=PN_proportion
                df['PN_proportion_filtered'].values[index]=PN_proportion_filtered                
                df['PN_open_proportion'].values[index]=PN_open_proportion

            except IndexError as e: #to catch empty line/triple at the end of the file 
                errors_tweet.append({user_id: {tweet: e}})

    #create dictionary of mean proportions for every user 
    d={'user_id_str':user_id, 'side':'RIGHT', 'mean_N_nopronouns_proportion':df['N_nopronouns_proportion'].mean(), 'mean_N_nopronouns_proportion_filtered':df['N_nopronouns_proportion_filtered'].mean(), 'mean_N_nopronouns_open_proportion':df['N_nopronouns_open_proportion'].mean(), 
    'mean_PN_proportion':df['PN_proportion'].mean(), 'mean_PN_proportion_filtered':df['PN_proportion_filtered'].mean(), 'mean_PN_open_proportion':df['PN_open_proportion'].mean()
    }
    #append this dict to list of results for all users 
    results.append(d)

    print(f'finished file {counter} out of 17788 LEFT/16496 RIGHT')


len(results) #17788 for LEFT, 16496 for RIGHT
len(errors_triple) #6 for LEFT, 5 for RIGHT 
len(errors_tweet) #0 for LEFT, 0 for RIGHT


########################################
#### 3 - save results for one side #####
########################################
results = pd.DataFrame(results)  
results.tail()
results.to_csv('RESULTS_RIGHT_robustnesscheck.csv')
#saved in 'ark-tweet-nlp-0.3.2/outputs_conll/LEFT/RESULTS_LEFT_robustnesscheck.csv' 
#saved in 'ark-tweet-nlp-0.3.2/outputs_conll/RIGHT/RESULTS_RIGHT_multiverse_4.csv'

errors_triple = pd.DataFrame(errors_triple)
errors_triple
errors_triple.to_csv('ERRORS_RIGHT_multiverse_4.csv')

## now repeat for RIGHT 


########################################################################
#### 4 - join together LEFT and RIGHT results dfs to import into R for analysis
########################################################################

os.chdir(os.path.expanduser("~"))
#os.listdir()
df1 = pd.read_csv('ark-tweet-nlp-0.3.2/outputs_conll/LEFT/RESULTS_LEFT_robustnesscheck.csv', index_col=0)
df1.head()
df1 #17788 rows × 8 columns
df2 = pd.read_csv('ark-tweet-nlp-0.3.2/outputs_conll/RIGHT/RESULTS_RIGHT_robustnesscheck.csv', index_col=0)
df2.head()
df2 #16496 rows × 8 columns
df_results = pd.concat([df1, df2], ignore_index=True)
df_results #34284 rows × 8 columns
df_results.iloc[17786:17800,] #checked that they joined together correctly, ignoring the header in df2
df_results.head()
df_results.to_csv('RESULTS_df_robustnesscheck.csv')







########################################################################
#### 5 - add centrality metrics to this new df #########################
# NB this was not done for multiverse_4 - I just copied the centrality metrics from earlier 
########################################################################

df_centrality = pd.read_csv('RESULTS_df_multiverse_3_norponouns.csv', index_col=0)
df_centrality_short = df_centrality[['user_id_str','hubs']]
df_centrality_short

#merge this with df_results from above 
df_results.shape #(34284, 8)
df_centrality_short.shape #34284, 8)

df = pd.merge(df_results, df_centrality_short, on='user_id_str')
df.shape #(34284, 9)
df.head()
df.tail()

df['user_id_str_index'] = df['user_id_str']
df = df.set_index('user_id_str_index') #using twitter_name = screen_name as index for later

df.head()

df.to_csv('RESULTS_df_robustnesscheck_full.csv')
