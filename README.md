# Twitter-NLP-SNA
This is the code used in my MPhil project at the University of Cambridge, analysing political behaviour and communication on Twitter using Social Network Analysis and Natural Language Processing. 

Note: 
All code is executed in IPython, hence executing a line such as '>>> list_name' prints out the entire list titled 'list_name', without requiring a 'print(list_name)' statement. 

## This collection of code does the following: 

12 documents were used in Python for data collection, as follows: 
  1. parse in a pre-made csv file of elites and their Twitter accounts, as of March 2020 (elites include UK MPs, MEPs, and Political Party accounts) 
  2. connect to the Twitter API (using a private set of keys, which will need to be re-created if this code were to be replicated), collect all followers_IDs of each of the elites, saving them in separate files titled 'fillowers_{elite}.csv'
  3. build a network of elites and their followers, split the network up into LEFT and RIGHT (remove overlapping/central nodes); store side for main analysis
  4. randomly sample 100,000 user_ids from LEFT and 100,000 user_ids from RIGHT network 
  5. collect 200 most recent tweets from each of the users in LEFT and RIGHT networks, saving into MongoDB database 
  6. filter the users in each sample by activity 
  7. apply POS tagging to find nouns, proper nouns etc. in Tweets; calculate noun proportions for main analysis 
  8. calculate network centrality values for all nodes; store values for main analysis 
  9. clean words in tweets (lowercase, drop 's etc.), find most frequently used ones and visualise
  10. run additional linguistic analyses - Noun proportions without Pronouns; length of tweets on LEFT vs. RIGHT, amount of Proper Noun pairs on LEFT vs. RIGHT
  11. repeat word analysis after excluding all pronouns, 'coronavirus' words and emoticons/emoji from both Common and Proper Noun tags 
  12. visualise words used most frequently in the profile descriptions of 100 most central users 
  
Then, analysis was performed on the resulting data in R - the code for this is available in the analysis_R_code folder. 
  
## Packages required: see package imports at the top of every file
