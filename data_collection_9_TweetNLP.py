"""
data_collection_9_TweetNLP.py 

1 - create input files for ark TweetNLP 
2 - apply ark TweetNLP (in command line, Java)
3 - calculate noun proportion for each user, store in dictionary 
4 - re-tagging in different format - for content analysis 
5 - re-run analyses but excluding Pronouns 

@author: lizakarmannaya
"""
import pymongo 
from pymongo import MongoClient
import pandas as pd
import os 
import glob

################# 1 - create input files for ark TweetNLP #################


#preparing to save tagged tweet documents to mongo collection
client = MongoClient() #default host and port

###### 1.1 - LEFT ##################################
#db = client['TWITTER_LEFT']  ## NB REPEAT for RIGHT
db = client['TWITTER_RIGHT']  

#create db.tweets_tagged 
#tweets_tagged = db['tweets_tagged'] #new collection 
## SAVE TAGGES TWEETS IN HERE LATER? 



#### NOW CREATE LOOP TO LOOP OVER EVERY USER ID IN DB 

#the query is much faster if I firsrt create an index for 'user_id_str' (non-unique)
db.tweets_filtered.create_index('user_id_str') ## NB REPEAT for RIGHT
db.tweets_filtered.index_information()

def create_input_file(user_id_str):
    cursor = db.tweets_filtered.find({'user_id_str':user_id_str}, projection={'_id': 0, 'full_text': 1})
    #if length of cursor < 25... (following Sylwester & Purver, 2015)?? 
    for item in cursor: 
        tweet = item['full_text'] #extracting tweet texts from dictionary 
        if 'RT' not in tweet: #exclude all retweets 
            tweet_stripped = tweet.replace('\n','') #so that the POS tagger doesn't split a tweet with blank lines into separate tweets
            #to avoid saving blank files, only now open the destination (input) file 
            with open(f'ark-tweet-nlp-0.3.2/inputs/RIGHT/tweets_{user_id_str}.txt', 'a') as f:
                f.write("%s\n" % tweet_stripped)

#example for a single user, user_id_str = '123456'
#create_input_file('123456')
#df = pd.read_csv('ark-tweet-nlp-0.3.2/outputs/LEFT/tweets_123456_tagged.txt', sep='\t', header=None, names=['full_text', 'tags', 'confidence_values', 'tokens', 'N_count', 'N_proportion', 'N_count_filtered', 'N_proportion_filtered'])

#loop over all documents in LEFT/RIGHT collection & create input files
list_of_user_ids = db.tweets_filtered.distinct('user_id_str')
length = len(list_of_user_ids) #18225 LEFT; 18025 RIGHT
counter = 0
for user_id_str in list_of_user_ids:
    counter += 1 
    create_input_file(user_id_str)
    print(f'finished user {counter} out of {length}')


#close connection to MongoDB
client.close()

## NB  work out a way to claculate new, reduced sample - as some users had no own tweets 
# 17,789 input files in LEFT directory, BUT how many tweets per user? 
# 16,497 input files in RIGHT directory, BUT how many tweets per user?




################# 2 - apply ark TweetNLP (in command line, Java) #################

#COMMAND LINE input:

### cd /ark-tweet-nlp-0.3.2
### java -Xmx500m -jar ark-tweet-nlp-0.3.2.jar examples/example_tweets.txt
### java -Xmx500m -jar ark-tweet-nlp-0.3.2.jar inputs/LEFT/tweets_123456_four.txt >> outputs/LEFT/tweets_123456_four_tagged.txt

#LATER CREATE LOOP IN COMMAND FILE & EXECUTE FOR EVERY FILE IN inputs FOLDER 
#might also work:
### ./runTagger.sh examples/example_tweets.txt 

#input file = .txt file for each user_id_str where every new line is a tweet 



#command script:
#this script reads a .txt file from the inputs folder and outputs a tagged file of the same name into the outputs folder 

##cd ark-tweet-nlp-0.3.2/inputs/LEFT/
##for f in *.txt; do 
##    java -Xmx500m -jar ark-tweet-nlp-0.3.2.jar $f > ~/ark-tweet-nlp-0.3.2/outputs/LEFT/$f;
##done 

#NB had to copy .jar file to inputs/LEFT folder 

## NB REPEAT FOR RIGHT



### ERROR ####
# looping over directory below was picking up a .DS_Store file
# hence I deleted it from the LEFT & RIGHT directories through the command line:
# cd /ark-tweet-nlp-0.3.2/outputs/RIGHT
# find . -name "*.DS_Store" -type f -delete 




############### 3 - calculate noun proportion for each user, store in dictionary #################

def calculate_noun_proportion(df):
    for index in df.index:
        tags = df['tags'].values[index]
        #print(tags)
        #print(txt_file)
        try:
            tags = list(tags.split(' '))

            #now count nouns + nouns+possessive + nouns+verbal
            count = tags.count('N') + tags.count('S') + tags.count('L')
            df['N_count'].values[index] = count #adding count back into df
            count2 = tags.count('N') + tags.count('S') + tags.count('L') + tags.count('^') + tags.count('Z') + tags.count('M')
            df['N_Propernoun_count'].values[index] = count2
            count3 = tags.count('^') + tags.count('Z') + tags.count('M')
            df['Propernoun_count'].values[index]=count3

            #calcuating proportion - without excluding special characters
            noun_proportion = round((count/len(tags)), 4)
            df['N_proportion'].values[index]=noun_proportion
            noun_proportion2 = round((count2/len(tags)), 4)
            df['N_Propernoun_proportion'].values[index] = noun_proportion2
            propernoun_proportion = round((count3/len(tags)), 4)
            df['Propernoun_proportion'].values[index] = propernoun_proportion

            #calcuating proportion - WITH exclustion of special characters
            tags_filtered = [x for x in tags if x not in special_chars]
            if len(tags_filtered) > 0:
                noun_proportion_filtered = round((count/len(tags_filtered)), 4)
                noun_proportion_filtered2 = round((count2/len(tags_filtered)), 4)
                propernoun_proportion = round((count3/len(tags_filtered)), 4)
            else: 
                noun_proportion_filtered = 0 #to avoid dividing by 0 if tags_filtered is empty
                noun_proportion_filtered2 = 0
                propernoun_proportion = 0
            df['N_proportion_filtered'].values[index]=noun_proportion_filtered
            df['N_Propernoun_proportion_filtered'].values[index]=noun_proportion_filtered2
            df['Propernoun_proportion_filtered'].values[index]=propernoun_proportion

            #calculatiing proportion of nouns & proper nouns vs open-class words only 
            tags_open_class = [x for x in tags if x in open_class_words]
            if len(tags_open_class) > 0:
                noun_open_class_proportion = round((count/len(tags_open_class)), 4)
                noun_open_class_proportion2 = round((count2/len(tags_open_class)), 4)
                propernoun_open_proportion = round((count3/len(tags_open_class)), 4)
            else: 
                noun_open_class_proportion = 0 #to avoid dividing by 0 if tags_filtered is empty
                noun_open_class_proportion2 = 0
                propernoun_open_proportion = 0
            df['N_open_proportion'].values[index]=noun_open_class_proportion
            df['N_Propernoun_open_proportion'].values[index]=noun_open_class_proportion2
            df['Propernoun_open_proportion'].values[index]=propernoun_open_proportion


        except AttributeError as e: #pops up in some tweets that are wrongly tagged/output file wrongly parsed
            errors.append({'user_id': txt_file, 'tweet_index': index, 'error': e})
            #this leaves the uncalculated values as NaN, which get ignored during calculation

#os.chdir('ark-tweet-nlp-0.3.2/outputs/LEFT') #do this once
os.chdir('../RIGHT')
os.listdir()

special_chars = ['#', '@', '~', 'U', 'E', ','] #keepng 'G' (abbreviations) and '$' (numerals)
open_class_words = ['N', 'O', 'S', '^', 'Z', 'L', 'M', 'V', 'A', 'R', '!']
results =[] #list of dicts to save each user's reslts into
errors = [] #list of dicts to save errors into
counter=0
for txt_file in glob.glob("*.txt"): 
    counter+=1
    df = pd.read_csv(txt_file, sep='\t', header=None, names=['full_text', 'tags', 'confidence_values', 'tokens', 'N_count', 'N_Propernoun_count', 'N_proportion', 'N_Propernoun_proportion', 'N_proportion_filtered', 'N_Propernoun_proportion_filtered', 'N_open_proportion', 'N_Propernoun_open_proportion', 'Propernoun_count', 'Propernoun_proportion', 'Propernoun_proportion_filtered', 'Propernoun_open_proportion'])
    #apply function
    calculate_noun_proportion(df)

    #extract user_id_str from file name 
    user_id_str = txt_file.split("tweets_")[1] 
    user_id_str = user_id_str.split(".txt")[0]
    #print(type(user_id_str)) #str

    d={'user_id_str':user_id_str, 'side':'RIGHT', 'mean_N_proportion':df['N_proportion'].mean(), 'mean_N_proportion_filtered':df['N_proportion_filtered'].mean(), 'mean_N_Propernoun_proportion':df['N_Propernoun_proportion'].mean(), 'mean_N_Propernoun_proportion_filtered':df['N_Propernoun_proportion_filtered'].mean(), 'mean_N_open_proportion': df['N_open_proportion'].mean(),'mean_N_Propernoun_open_proportion':df['N_Propernoun_open_proportion'].mean(), 'mean_Propernoun_proportion':df['Propernoun_proportion'].mean(), 'mean_Propernoun_proportion_filtered':df['Propernoun_proportion_filtered'].mean(), 'mean_Propernoun_open_proportion':df['Propernoun_open_proportion'].mean()}
    results.append(d)

    print(f'finished file {counter} out of 17789 LEFT/16496 RIGHT')

len(results) #correct - 17788 for LEFT, 16496 for RIGHT
results = pd.DataFrame(results)  
results.tail()

results.to_csv('RESULTS_RIGHT_multiverse_2.csv')
#saved in 'ark-tweet-nlp-0.3.2/outputs/LEFT/RESULTS_LEFT.csv' and 'RESULTS_LEFT_multiverse.csv'
#saved in 'ark-tweet-nlp-0.3.2/outputs/RIGHT/RESULTS_RIGHT.csv' and 'RESULTS_RIGHT_multiverse.csv'


errors 
len(errors) #201 errors in left, 164 in right 
errors = pd.DataFrame(errors)
errors
errors.to_csv('ERRORS_RIGHT_multiverse_2.csv')
#saved in 'ark-tweet-nlp-0.3.2/outputs/LEFT/RESULTS_LEFT.csv'
#saved in 'ark-tweet-nlp-0.3.2/outputs/RIGHT/RESULTS_RIGHT.csv'

#NB some users have quite a few tweets with 0 nouns 



#join together LEFT and RIGHT results dfs to import into R for analysis: 
os.chdir(os.path.expanduser("~"))
os.listdir()
df1 = pd.read_csv('ark-tweet-nlp-0.3.2/outputs/LEFT/RESULTS_LEFT_multiverse_2.csv', index_col=0)
df1.head()
df1 #17788 rows × 8 columns
df2 = pd.read_csv('ark-tweet-nlp-0.3.2/outputs/RIGHT/RESULTS_RIGHT_multiverse_2.csv', index_col=0)
df2.head()
df2 #16496 rows × 8 columns
df_results = pd.concat([df1, df2], ignore_index=True)
df_results #34284 rows × 8 columns
df_results.iloc[17786:17800,] #checked that they joined together correctly, ignoring the header 
df_results.to_csv('RESULTS_df_multiverse_2.csv')





##########################################################################
######## 4 - re-tagging in different format - for content analysis #######
##########################################################################

#command script ('myCommandScript_.command')
#this script reads a .txt file from the inputs folder and outputs a tagged file of the same name into the outputs folder 

##cd ark-tweet-nlp-0.3.2/inputs/LEFT/
##for f in *.txt; do 
##    java -Xmx500m -jar ark-tweet-nlp-0.3.2.jar $f > ~/ark-tweet-nlp-0.3.2/outputs_conll/LEFT/$f;
##done 

#NB had to copy .jar file to inputs/LEFT folder 



