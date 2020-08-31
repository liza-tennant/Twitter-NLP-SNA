#Checking noun-social conservatism correlation 

library(ltm)
library(psych)
library(dplyr)
library(data.table)
rm(list = ls())
setwd("/Users/lizakarmannaya/Desktop/CAMBRIDGE/Research Project/Questionnaire Study")

#### read in prolific data #### 
prolific1 = read.csv("study3_prolific_10_Left.csv", stringsAsFactors=FALSE)
prolific2 = read.csv("study3_prolific_10_Right.csv", stringsAsFactors=FALSE)
prolific_20 = rbind(prolific1, prolific2) 
#NB pre-screening for nationality and first language was only added after this step - so I will need to manually exclude 2 participants who don't fit this criteria from the first 20
which(prolific_20$Country.of.Birth == "Switzerland") #6
prolific[6, 'participant_id'] #5ba2cd9ee671c60001236628
which(prolific_20$Country.of.Birth == "South Africa") #15
prolific[15, 'participant_id'] #5eebe4eda3634e3c4054bfc4

#now read in the rest of the data
prolific3 = read.csv("study3_prolific_200_Left.csv", stringsAsFactors=FALSE)
prolific4 = read.csv("study3_prolific_279_Right.csv", stringsAsFactors=FALSE)
prolific = rbind(prolific3, prolific4, prolific_20) 
#make sure the 'status' for user 5e0a51337832252dbdd5e876 is 'APPROVED' - this user was paid manually due to time-out on Prolific 
colnames(prolific)
which(prolific$participant_id == "5e0a51337832252dbdd5e876") #422
prolific[422, 'status'] #yes, this says 'APPROVED
#now, only keep those whose 'status' column has the value 'APPROVED'
prolific<-subset(prolific, prolific$status=='APPROVED') #this changes it from 506 observations to 499

#now exclude two participants with not suitable country of birth 
prolific<-subset(prolific, prolific$participant_id!='5ba2cd9ee671c60001236628') 
prolific<-subset(prolific, prolific$participant_id!='5eebe4eda3634e3c4054bfc4') #now 497 observations 

#now exclude one participant whow did not pass the attention cheeck (based on id found in data_CLEAN  below)
prolific<-subset(prolific, prolific$participant_id!='5d52ff633f2d2500193185cd') #now 496 observations 

#now exclude one participant who completed survey in under 3 mins
prolific<-subset(prolific, prolific$participant_id!='5ee0ea4b6f43d80a4e57435d')
#now 494 observations - there were 2 records for this 

#one who said 'no' on consent form is already excluded through the 'APPROVED' filtering above 

## demographics:
colnames(prolific)
describe(prolific$age)
prolific %>% group_by(Sex) %>% summarise(n())


#### now read in the main data ####
data = read.csv("study3_data_500.csv", stringsAsFactors=FALSE)
colnames(data)
#str(data)
#delete first 2 rows from Qualtrics, and the irrelevant columns
data_CLEAN<-data[3:502,  ] #500 observations, 91 (will become 74) variables
which(data_CLEAN$Q99=="")
#manually put in value '2' for the attention check for the first 20 participants (the question wasn't there when these were collected)
#data_CLEAN$Q99[data_CLEAN$Q99==""] #for some reason, there are 120 of these - likely because this wasn't a 'forced response' question for the first 320 users... 
data_CLEAN$Q99[data_CLEAN$Q99==""] <- 2
#get their prolific id so they can be excluded from the prolific df 
which(data_CLEAN$Q99 != "2") #463
data_CLEAN[463, 'T1'] #this is the prolific id column
#prolific[, 'Prolific_ID']

#then exclude those who didn't pass attention check
data_CLEAN <-subset(data_CLEAN, data_CLEAN$Q99==2) #now 499 observations 

#exclude anyone who said 'no' on the consent form 
data_CLEAN <-subset(data_CLEAN, data_CLEAN$C1==4) #this brings it down to 498 

#exclude those who took under 3 mins 
which(as.numeric(data_CLEAN$Duration..in.seconds.) <= 3*60) 
data_CLEAN[101, 'T1'] #prolific id : 5ee0ea4b6f43d80a4e57435d
data_CLEAN <-subset(data_CLEAN, as.numeric(data_CLEAN$Duration..in.seconds.) > 3*60) #this brings it down to 497

#exclude irrelevant columns 
colnames(data_CLEAN)
data_CLEAN <- data_CLEAN[, 18:91]

#drop the two non-Biritish participants 
data_CLEAN <- subset(data_CLEAN, T1 != "5ba2cd9ee671c60001236628") #496
data_CLEAN <- subset(data_CLEAN, T1 != "5eebe4eda3634e3c4054bfc4") #495


#make all data numeric 
colnames(data_CLEAN)
data_CLEAN <- subset(data_CLEAN, select = -c(T6)) #drop column T6, which is text
for(i in 3:ncol(data_CLEAN)) {data_CLEAN[,i]<-as.numeric(data_CLEAN[,i])}
#another way, but this gets confused by the first two columns
#temp <- data.frame(apply(data_CLEAN, 2, function(x) as.numeric(x)))

colnames(data_CLEAN)
#change names of columns to be more meaningful
names(data_CLEAN)<-c("consent","Prolific_ID", 
                     "noun1", "noun2","noun3","noun4","noun5","noun6","noun7","noun8","noun9","noun10",
                     "pngeneral1", "pngeneral2", "pngeneral3", "pngeneral4", "pngeneral5", #proper noun general
                     "pntemporal1", "pntemporal2", "pntemporal3", "pntemporal4", "pntemporal5", #proper noun termporal
                     "pnchar1", "pnchar2", "pnchar3", "pnchar4", "pnchar5", #proper noun characteristics
                     "pnnames1", "pnnames2", "pnnames3", "pnnames4", "pnnames5", #proper noun names
                     "rwa1", "rwa2", "rwa3", "rwa4", "rwa5", #right-wing authoritarianism 
                     "immigration1", "immigration2", "immigration3", "immigration4",  #immigration scales
                     "ipt1", "ipt2", "ipt3", #essentialism scales - implicit person theory
                     "dis1", "dis2", "dis3", "dis4", "dis5", "dis6", "dis7", "dis8", #essentialism scales - discreteness
                     "decisive1", "decisive2", "decisive3", "decisive4", "decisive5", "decisive6", #decisiveness scale
                     "attention_check", 
                     "overall_cons", "social_cons", "econ_cons", #explicit conservatism scales
                     "SC1", "SC2", "SC3", "SC4", "SC5", "SC6", "SC7", "SC8", "SC9", "SC10", "SC11")


#check distribution of Explicit Social Conservatism from Qualtrics 
hist(data_CLEAN$social_cons)

#check proper noun distributions
hist(rowSums(data_CLEAN[, 3:12])) # noun items - approx normal, slight left skew 
hist(rowSums(data_CLEAN[, 13:17])) # proper noun general items - right skew 
hist(rowSums(data_CLEAN[, 18:22])) # proper noun temporal items - strong left skew 
hist(rowSums(data_CLEAN[, 23:27])) # proper noun characteristics items - approx normal, but left-skew
hist(rowSums(data_CLEAN[, 28:32])) # proper noun characteristics items - approx normal



#### Prolific ####
#check distributions of demographic variables from Prolific 
hist(prolific$age)
prolific %>% group_by(Political.Affiliation..UK.) %>% summarize(num=n()) #208 Left, 289 Right, 2 Centre
median(prolific$time_taken)/60 #8.14 mins 
#hist of age by political side 
hist(prolific$age[prolific$Political.Affiliation..UK. == 'Left'])
hist(prolific$age[prolific$Political.Affiliation..UK. == 'Right'])







#### Check Consistency of RWA Items ####
colnames(data_CLEAN[, 33:37])
cronbach.alpha(data_CLEAN[, 33:37], standardized = FALSE, CI = FALSE, 
               probs = c(0.025, 0.975), B = 1000, na.rm = FALSE)
# Alpha level is 0.767


data_CLEAN$RWA<-rowMeans(data_CLEAN[, c(33:37)])
## RWA scored as higher = more authoritarianism
describe(data_CLEAN$RWA) #Mean=3.14, SD=0.9

#z-score this so we can average it with the immigration items later 
data_CLEAN$RWAZSMean<-((scale(data_CLEAN[, 33]) + scale(data_CLEAN[, 34]) + scale(data_CLEAN[, 35]) + scale(data_CLEAN[, 36]) + scale(data_CLEAN[, 37]))/5)
range(data_CLEAN$RWAZSMean) #-1.773 to 1.492



#### Check Consistency of Immigration Items ####
colnames(data_CLEAN[, 38:41])
cronbach.alpha(data_CLEAN[, c( 38:41)], standardized = FALSE, CI = FALSE, 
               probs = c(0.025, 0.975), B = 1000, na.rm = FALSE)
#alpha=0.922


##NB Immigration is currently scored as low scores = anti-immigration --> need to reverse-score
data_CLEAN$immigration1 <- 6 - data_CLEAN$immigration1 #5 answer options  
data_CLEAN$immigration2 <- 8 - data_CLEAN$immigration2 #7 answer options  
data_CLEAN$immigration3 <- 8 - data_CLEAN$immigration3 #7 answer options  
data_CLEAN$immigration4 <- 8 - data_CLEAN$immigration4 #7 answer options  


#1. z-scoring imigration items - because they were measured on different scales
data_CLEAN$ImmigrationZSMean<-((scale(data_CLEAN[, 38]) + scale(data_CLEAN[, 39]) + scale(data_CLEAN[, 40])+ scale(data_CLEAN[, 41]))/4)

describe(data_CLEAN$ImmigrationZSMean)

#### check consistency of RWA + Immigration ####
colnames(data_CLEAN[, c(33:41)])
cronbach.alpha(data_CLEAN[, c(33:41)], standardized = FALSE, CI = FALSE, 
probs = c(0.025, 0.975), B = 1000, na.rm = FALSE)
#alpha=.892

#consistency of the ZSMean scores for the two scales? 
colnames(data_CLEAN)
cronbach.alpha(data_CLEAN[, c(74:75)], standardized = FALSE, CI = FALSE, 
               probs = c(0.025, 0.975), B = 1000, na.rm = FALSE)
#alpha=.771

plot(data_CLEAN$ImmigrationZSMean, data_CLEAN$RWAZSMean)

#### create combined Implicit Social Conservatism score #### 
# average RWA and Immigration 
colnames(data_CLEAN[, 74:75])
data_CLEAN$RWAImmg<-rowMeans(data_CLEAN[, c(74:75)])
hist(data_CLEAN$RWAImmg) #approximately normal, only slight right-skew 


#### check consistency of Essentialism scales ####
colnames(data_CLEAN)
colnames(data_CLEAN[, c(42:52)])
cronbach.alpha(data_CLEAN[, c(42:52)], standardized = FALSE, CI = FALSE, 
               probs = c(0.025, 0.975), B = 1000, na.rm = FALSE)
#alpha=.616

###2. calculating noun sum score ####
colnames(data_CLEAN[, 3:12]) #noun columns
#now I can create a sum score, which will reflect how many nouns a participant used in total, out of 10
data_CLEAN$noun_sum = rowSums(data_CLEAN[, 3:12])

#### descriptive stats ####
range(data_CLEAN$noun_sum) #ranges from 0 to 10
describe(data_CLEAN$noun_sum) #Mean=4.09, SD=1.93, median=4, skew=0.34, kurtosis=-0.16
range(data_CLEAN$RWAImmg) #ranges from -1.681 to 1.634
describe(data_CLEAN$RWAImmg) #Mean=0, SD=0.74, median=-0.03, skew=0.04, jurtosis=-0.69
range(data_CLEAN$social_cons) #1 to 7 
describe(data_CLEAN$social_cons) #Mean=3.75, SD=1.92, Median=4, Skew=0.09, Kurtosis=-1.31


#####corrtest with Nouns #####

#against Implicit social conservatism 
cor.test(data_CLEAN$noun_sum, data_CLEAN$RWAImmg) #p = .0038, r = 0.126
cor.test(data_CLEAN$noun_sum, data_CLEAN$RWAImmg, method='kendall') #p = .005, tau=.090
plot(data_CLEAN$noun_sum, data_CLEAN$RWAImmg)

#against Explicit social conservatism 
cor.test(data_CLEAN$noun_sum, data_CLEAN$social_cons) #p = 0.621 
cor.test(data_CLEAN$noun_sum, data_CLEAN$social_cons, method='kendall') #p=0.5721


#against Essentialism 
colnames(data_CLEAN[,45:52]) #8 Discreteness items
#now the scale for all dis items is higher = more essentialist 
data_CLEAN$Discreteness<-((scale(data_CLEAN[, 45]) + scale(data_CLEAN[, 46]) + scale(data_CLEAN[, 47]) + scale(data_CLEAN[, 48]) + scale(data_CLEAN[, 49])  + scale(data_CLEAN[, 50]) + scale(data_CLEAN[, 51]) + scale(data_CLEAN[, 52]))/8)
describe(data_CLEAN$Discreteness) #Mean=0, SD=0.42, Median=0.01, Skew=-0.16, Kurtosis=1.66, Range = -2.17 to 3.72
#non-z-scored version for reporting descriptive stats 
data_CLEAN$Discreteness2<-rowMeans(data_CLEAN[, c(45:52)])
describe(data_CLEAN$Discreteness2)

colnames(data_CLEAN[, 42:44]) #3 IPT items
data_CLEAN$IPT<-((scale(data_CLEAN[, 42]) + scale(data_CLEAN[, 43]) + scale(data_CLEAN[, 44]))/3)
describe(data_CLEAN$IPT) #Mean=0, SD=0.89, Median=0.03, Skew=-0.01, Kurtosis=-0.98, Range = -1.91 to 1.88
#non-z-scored version for reporting descriptive stats 
data_CLEAN$IPT2<-rowMeans(data_CLEAN[, c(42:54)])
describe(data_CLEAN$IPT2)


#now compute correlations of noun_sum against Discreteness and IPT 
cor.test(data_CLEAN$noun_sum, data_CLEAN$Discreteness2) #p=.099
cor.test(data_CLEAN$noun_sum, data_CLEAN$Discreteness2, method='kendall') #p=.094

cor.test(data_CLEAN$noun_sum, data_CLEAN$IPT2) #p=.009, r= 0.117
cor.test(data_CLEAN$noun_sum, data_CLEAN$IPT2, method='kendall') #p=.007, tau=0.089

#what about essentialism against politics? 
cor.test(data_CLEAN$RWAImmg, data_CLEAN$Discreteness2) #p=1.106e-06, r=0.217
cor.test(data_CLEAN$RWAImmg, data_CLEAN$Discreteness2, method='kendall') 
plot(data_CLEAN$RWAImmg, data_CLEAN$Discreteness2)

cor.test(data_CLEAN$social_cons, data_CLEAN$Discreteness2) #p=0.0002, r=0.166
cor.test(data_CLEAN$social_cons, data_CLEAN$Discreteness2, method='kendall')

plot(data_CLEAN$social_cons, data_CLEAN$Discreteness2)

cor.test(data_CLEAN$RWAImmg, data_CLEAN$IPT2) #p< 2.2e-16, r=0.387
cor.test(data_CLEAN$RWAImmg, data_CLEAN$IPT2, method='kendall') 
plot(data_CLEAN$RWAImmg, data_CLEAN$IPT2)

cor.test(data_CLEAN$social_cons, data_CLEAN$IPT2) #p=1.135e-10, r=0.285
cor.test(data_CLEAN$social_cons, data_CLEAN$IPT2, method='kendall') 
plot(data_CLEAN$social_cons, data_CLEAN$IPT2) 


#against Decisiveness
colnames(data_CLEAN[, 53:58])
data_CLEAN$Decisiveness<-((scale(data_CLEAN[, 53]) + scale(data_CLEAN[, 54]) + scale(data_CLEAN[, 55])  + scale(data_CLEAN[, 56])  + scale(data_CLEAN[, 57])  + scale(data_CLEAN[, 58]) )/6)
describe(data_CLEAN$Decisiveness) #Mean=0, SD=0.68, Median=0.04, Skew=-0.13, Kurtosis=-0.06, Range=-2.38 to 1.75
#non-z-scored version for reporting descriptive stats 
data_CLEAN$Decisiveness2<-rowMeans(data_CLEAN[, c(53:58)])
describe(data_CLEAN$Decisiveness2)

cor.test(data_CLEAN$noun_sum, data_CLEAN$Decisiveness2) #p=0.296
cor.test(data_CLEAN$noun_sum, data_CLEAN$Decisiveness2, method='kendall')




#### 3. calculating proper noun sum scores ####
colnames(data_CLEAN) #noun columns
#now I can create a sum score, which will reflect how many nouns a participant used in total, out of 10
data_CLEAN$pn_General = rowSums(data_CLEAN[, 13:17])
data_CLEAN$pn_Temporal = rowSums(data_CLEAN[, 18:22])
data_CLEAN$pn_Characteristics = rowSums(data_CLEAN[, 23:27])
data_CLEAN$pn_Names = rowSums(data_CLEAN[, 28:32])

#### descriptive stats for proper nouns ####
describe(data_CLEAN$pn_General) #Mean=3.48, SD=1, Median=4, Skew= -0.55, Kurtosis=0.34, Range= 0 to 5
describe(data_CLEAN$pn_Temporal) #Mean=1.2, SD=1.1, Median=1, Skew=1.23, Kurtosis=1.75, Range=0 to 5
describe(data_CLEAN$pn_Characteristics) #Mean=2.22, SD=1.05, Median=2, Skew= -0.07, Kurtosis= -0.49, Range=0 to 5
describe(data_CLEAN$pn_Names) #Mean=2.83, SD=1.15, Median=3, Skew=0.02, Kurtosis= -0.44, Range=0 to 5

hist(data_CLEAN$pn_General)
hist(data_CLEAN$pn_Temporal)
hist(data_CLEAN$pn_Characteristics)
hist(data_CLEAN$pn_Names)

##### correlations for proper nouns ####
## 1. Proper Nouns ~ Implicit Social Conservatism
cor.test(data_CLEAN$pn_General, data_CLEAN$RWAImmg) #p=0.205
cor.test(data_CLEAN$pn_Temporal, data_CLEAN$RWAImmg) #p=0.513
cor.test(data_CLEAN$pn_Characteristics, data_CLEAN$RWAImmg) #p=0.076, r=0.07979993
cor.test(data_CLEAN$pn_Names, data_CLEAN$RWAImmg) #p=0.388

## 2. Proper Nouns ~ Explicit Social Conservatism
cor.test(data_CLEAN$pn_General, data_CLEAN$social_cons) #p=0.593
cor.test(data_CLEAN$pn_Temporal, data_CLEAN$social_cons) #p=0.3335
cor.test(data_CLEAN$pn_Characteristics, data_CLEAN$social_cons) #p=0.186
cor.test(data_CLEAN$pn_Names, data_CLEAN$social_cons) #p=0.8335

## 3. Proper Nouns ~ IPT
cor.test(data_CLEAN$pn_General, data_CLEAN$IPT2) #p=.933
cor.test(data_CLEAN$pn_Temporal, data_CLEAN$IPT2) #p=.312
cor.test(data_CLEAN$pn_Characteristics, data_CLEAN$IPT2) #p=.375
cor.test(data_CLEAN$pn_Names, data_CLEAN$IPT2) #p=.650

## 4. Proper Nouns ~ Discreteness
cor.test(data_CLEAN$pn_General, data_CLEAN$Discreteness2) #p=.921
cor.test(data_CLEAN$pn_Temporal, data_CLEAN$Discreteness2) #p=.539
cor.test(data_CLEAN$pn_Characteristics, data_CLEAN$Discreteness2) #p=.237
cor.test(data_CLEAN$pn_Names, data_CLEAN$Discreteness2) #p=.399

## 5. Proper Nouns ~ Decisiveness
cor.test(data_CLEAN$pn_General, data_CLEAN$Decisiveness2) #p=.209
cor.test(data_CLEAN$pn_Temporal, data_CLEAN$Decisiveness2) #p=.173
cor.test(data_CLEAN$pn_Characteristics, data_CLEAN$Decisiveness2) #p=.653
cor.test(data_CLEAN$pn_Names, data_CLEAN$Decisiveness2) #p=.757

## adjust p-values using Bonferroni-Holm method 
unadjusted_ImplicitSocialCons <- c(0.205, 0.513, 0.076, 0.388)
unadjusted_ExplicitSocialCons <- c(0.593, 0.334, 0.186, 0.834)
unadjusted_IPT <- c(.933, .312, .375, .650)
unadjusted_Discreteness <- c(.921, .593, .237, .399)
unadjusted_Decisiveness <- c(.209, .173, .653, .757)

adjusted <- p.adjust(unadjusted_Decisiveness, method = "holm")
p.table <- cbind(adjusted, unadjusted_Decisiveness)
p.table



#### Mediation analyses ####
colnames(data_CLEAN)
library(lavaan)
library(tidyverse)
library(psych)
colnames(data_CLEAN)
#rename IPT2 to IPT
data_CLEAN %>% 
  rename(
    IPT = IPT2
  ) %>% 
  select(noun_sum, RWAImmg, IPT) %>% 
  pairs.panels()

mod1 <- "# direct effect
noun_sum ~ c * RWAImmg

# mediator
noun_sum ~ a * IPT2
IPT2 ~ b * RWAImmg

# indirect and total effects
ab := a * b
total := c + (a*b)"

set.seed(1234)
fsem1 <- sem(mod1, data = data_CLEAN)
summary(fsem1, standardized = TRUE)

