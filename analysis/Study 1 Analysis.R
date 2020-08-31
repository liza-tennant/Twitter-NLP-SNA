
library(ltm)
library(psych)
library(dplyr)
rm(list = ls())
setwd("/Users/lizakarmannaya/Desktop/CAMBRIDGE/Laidlaw_Data")

data = read.csv("study1_data.csv", stringsAsFactors=FALSE)
data_CLEAN<-data[3:350,20:197]
colnames(data_CLEAN)

names(data_CLEAN)<-c("control1","control2", #control stories
                     "story1","story2","story3","story4","story5","story6","story7","story8", #critical stories
                     "bio1","bio2","bio3","bio4","bio5","bio6","bio7", #essentialism scales - biological bias
                     "dis1","dis2","dis3","dis4","dis5","dis6","dis7","dis8", #essentialism scales - discreteness
                     "inf1","inf2","inf3","inf4","inf5","inf6","inf7", #essentialism scales - informativeness
                     "ipt1","ipt2","ipt3", #essentialism scales - implicit person theory
                     "mfHarm1","mfHarm2","mfHarm3","mfHarm4",
                     "mfFair1","mfFair2","mfFair3","mfFair4",
                     "mfLoyal1","mfLoyal2","mfLoyal3","mfLoyal4",
                     "mfAuth1","mfAuth2","mfAuth3","mfAuth4",
                     "mfPur1","mfPur2","mfPur3","mfPur4", #moral foundation scales
                     "sdo1","sdo2","sdo3","sdo4","sdo5","sdo6","sdo7","sdo8","sdo9","sdo10","sdo11","sdo12","sdo13","sdo14","sdo15","sdo16", #SDO scales
                     "rwa1","rwa2","rwa3","rwa4","rwa5", #RWA scales
                     "immigration1","immigration2","immigration3","immigration4",  #immigration scales
                     "econ1","econ2","econ3","econ4","econ5", #economic questions
                     "pattern1_uncom","pattern1_anxious","pattern1_annoyed",
                     "pattern2_uncom","pattern2_anxious","pattern2_annoyed",
                     "pattern3_uncom","pattern3_anxious","pattern3_annoyed",
                     "pattern4_uncom","pattern4_anxious","pattern4_annoyed",
                     "pattern5_uncom","pattern5_anxious","pattern5_annoyed",
                     "pattern6_uncom","pattern6_anxious","pattern6_annoyed",
                     "attention1","attentionNULL","attention2", #attention checks
                     "sesq1Char","sesq1Exter","sesq1Con",
                     "sesq2Char","sesq2Exter","sesq2Con",
                     "sesq3Char","sesq3Exter","sesq3Con",
                     "sesq4Char","sesq4Exter","sesq4Con",
                     "sesq5Char","sesq5Exter","sesq5Con",
                     "sesq6Char","sesq6Exter","sesq6Con",
                     "sesq7Char","sesq7Exter","sesq7Con",
                     "sesq8Char","sesq8Exter","sesq8Con",
                     "noun1", "noun2","noun3","noun4","noun5","noun6","noun7","noun8","noun9","noun10",
                     "ih1","ih2","ih3","ih4","ih5","ih6","ih7","ih8","ih9","ih10","ih11","ih12","ih13","ih14","ih15","ih16","ih17","ih18","ih19", #inherence heuristic
                     "ageNull","age","gender","ethnicity","edu","father_edu","mother_edu","resident","vote2015","vote2017","vote_now","brexit","brexit_now","ladder","income","asset","secure","secure_10", "Score"
)

colnames(data_CLEAN)
data_CLEAN<-subset(data_CLEAN, data_CLEAN$attention1==1)
data_CLEANYes<-subset(data_CLEAN, data_CLEAN$attention2=="Yes")
data_CLEANyes<-subset(data_CLEAN, data_CLEAN$attention2=="yes")
data_CLEAN_yes<-subset(data_CLEAN, data_CLEAN$attention2==" yes")
data_CLEANYES<-subset(data_CLEAN, data_CLEAN$attention2=="YES")
data_CLEAN<-rbind(data_CLEANYes, data_CLEANyes, data_CLEAN_yes, data_CLEANYES)

#exclude by age? 
which(data_CLEAN$age<18)
data_CLEAN[55,'age'] #15
data_CLEAN<-subset(data_CLEAN, data_CLEAN$age>=18) #moves it down from 326 to 324

for(i in 1:ncol(data_CLEAN)) {
  data_CLEAN[,i]<-as.numeric(data_CLEAN[,i])
}

describe(data_CLEAN$age)
data_CLEAN %>% group_by(gender) %>% summarize(num=n()) #154 male, 169 female

#descriptives

######## Check Consistency of RWA Items #####
colnames(data_CLEAN[, 72:76])
cronbach.alpha(data_CLEAN[, 72:76], standardized = FALSE, CI = FALSE, 
               probs = c(0.025, 0.975), B = 1000, na.rm = FALSE)
# Alpha level is 0.775, so checking factor structure





RWAFA_1<-fa(data_CLEAN[, c(72:76)], 1)
print(RWAFA_1$loadings)

RWAFA_2<-fa(data_CLEAN[, c(72:76)], 2)
print(RWAFA_2$loadings)

RWAFA_3<-fa(data_CLEAN[, c(72:76)], 3)
print(RWAFA_3$loadings)

# Factor structure with 1 factor looks sensible, this is a standard scale, and alpha is only just below 0.8, so taking the average
data_CLEAN$RWA<-rowMeans(data_CLEAN[, c(72:76)])

#the below is not done as we create our own, z-scored mean version of RWA 
#data_CLEAN$RWA=6-data_CLEAN$RWA #reversing as seems more intiutive that high scores mean high RWA

## RWA now scored as higher = more authoritarian 

#RWA also to z-score these (scale) 
colnames(data_CLEAN[, 72:76])
data_CLEAN$RWAZSMean<-((scale(data_CLEAN[, 72]) + scale(data_CLEAN[, 73]) + scale(data_CLEAN[, 74]) + scale(data_CLEAN[, 75]) + scale(data_CLEAN[, 76]))/5)
#reverse score by *(-1)
data_CLEAN$RWAZSMean=(-1)*data_CLEAN$RWAZSMean #reversing 
range(data_CLEAN$RWAZSMean) # -2.093377 to 1.346758
describe(data_CLEAN$RWAZSMean) #Mean=0, SD=0.73, Median=0.05, Skew=-0.47, Kurtosis=-0.11, Range= -2.093377 to 1.346758


########################## Check Consistency of Immigration Items ######
colnames(data_CLEAN[, 77:80])
cronbach.alpha(data_CLEAN[, c( 77:80)], standardized = FALSE, CI = FALSE, 
               probs = c(0.025, 0.975), B = 1000, na.rm = FALSE)
#alpha=0.885

## NB Immigration is currently scored as low scores = anti-immigration --> need to reverse-score later


###1. z-scoring ####

#z-scoring imigration items - because they were measured on different scales
data_CLEAN$ImmigrationZSMean<-((scale(data_CLEAN[, 77]) + scale(data_CLEAN[, 78]) + scale(data_CLEAN[, 79])+ scale(data_CLEAN[, 80]))/4)
#now also multiply all ImmigrationZSMean scores by -1 to make it higher score = more anti-immigration
data_CLEAN$ImmigrationZSMean=(-1)*data_CLEAN$ImmigrationZSMean #reversing 
describe(data_CLEAN$ImmigrationZSMean) #Mean=0, SD=0.89, Median=-0.04, Skew=0.18, Kurtosis=-0.61, Range=-1.85 to 1.76


########################## Check Consistency of RWA + Immigration  ######

#data_CLEAN$temp<-((scale(data_CLEAN[, 72]) + scale(data_CLEAN[, 73]) + scale(data_CLEAN[, 74]) + scale(data_CLEAN[, 75]) + scale(data_CLEAN[, 76]) + scale(data_CLEAN[, 77]) + scale(data_CLEAN[, 78]) + scale(data_CLEAN[, 79])+ scale(data_CLEAN[, 80]))/9)
#data_CLEAN$temp<-(-1)*data_CLEAN$temp
cronbach.alpha(data_CLEAN[, c(72:80)], standardized = FALSE, CI = FALSE, 
               probs = c(0.025, 0.975), B = 1000, na.rm = FALSE)
#alpha=0.879 


#then average RWA and Immigration to reflect social politics 
colnames(data_CLEAN[, 180:181])
data_CLEAN$RWAImmg<-rowMeans(data_CLEAN[, c(180:181)])
cronbach.alpha(data_CLEAN[, c( 180:181)], standardized = FALSE, CI = FALSE, 
               probs = c(0.025, 0.975), B = 1000, na.rm = FALSE)
#alpha for the averages = 0.773 

describe(data_CLEAN$RWAImm)


###2. calculating noun sum score####
#calculate noun score
colnames(data_CLEAN[, 131:140]) #noun columns
#need to reverse-score questions 136, 137, 138, 139, 142, 143 = noun1,2,3,, since now adjective = 2, noun = 1. Straight away make adj=0, noun=1
#since initially noun=1, adj=2, I just need to replace all 2 with -1
data_CLEAN$noun1[data_CLEAN$noun1 == 2] <- 0
data_CLEAN$noun2[data_CLEAN$noun2 == 2] <- 0
data_CLEAN$noun3[data_CLEAN$noun3 == 2] <- 0
data_CLEAN$noun4[data_CLEAN$noun4 == 2] <- 0
data_CLEAN$noun7[data_CLEAN$noun7 == 2] <- 0
data_CLEAN$noun8[data_CLEAN$noun8 == 2] <- 0

#for the remaining columns - noun5,6,9,10, re-code adj=1 to 0, noun=2 to 1 on all of them 
data_CLEAN$noun5[data_CLEAN$noun5 == 1] <- 0
data_CLEAN$noun5[data_CLEAN$noun5 == 2] <- 1
data_CLEAN$noun6[data_CLEAN$noun6 == 1] <- 0
data_CLEAN$noun6[data_CLEAN$noun6 == 2] <- 1
data_CLEAN$noun9[data_CLEAN$noun9 == 1] <- 0
data_CLEAN$noun9[data_CLEAN$noun9 == 2] <- 1
data_CLEAN$noun10[data_CLEAN$noun10 == 1] <- 0
data_CLEAN$noun10[data_CLEAN$noun10 == 2] <- 1
#now all adj=0, nouns=1, so we can calculate the sum (higher = more nouns)

#now I can create a sum score, which will reflect how many more nouns than adjectives a participant used 
colnames(data_CLEAN[, 131:140])
data_CLEAN$noun_sum = rowSums(data_CLEAN[, 131:140])
range(data_CLEAN$noun_sum) #ranges from 0 to 8
describe(data_CLEAN$noun_sum) #Mean=3.13, SD=1.85, Median=3, Skew=0.15, Kurtosis=-0.63

range(data_CLEAN$ImmigrationZSMean) #ranges from-1.85 to 1.76 
range(data_CLEAN$RWAZSMean) #ranges from -2.09 to 1.35
range(data_CLEAN$RWAImmg) #ranges from -1.97 to 1.55

####descriptive stats####
describe(data_CLEAN$noun_sum) #Mean=3.13, SD=1.85, Median=3, Skew=0.15, Kurtosis=-0.63

describe(data_CLEAN$RWA)
describe(data_CLEAN$ImmigrationZSMean)



#####pairwise correlations#####
#against overall social conservatism 
cor.test(data_CLEAN$noun_sum, data_CLEAN$RWAImmg) #p = .005, r = 0.154
plot(data_CLEAN$noun_sum, data_CLEAN$RWAImmg)


#then look at separate RWA-nouns and immigration-nouns correlations
cor.test(data_CLEAN$noun_sum, data_CLEAN$ImmigrationZSMean) #sig (p=.037), r = .115
plot(data_CLEAN$noun_sum, data_CLEAN$ImmigrationZSMean)

cor.test(data_CLEAN$noun_sum, data_CLEAN$RWAZSMean) #sig (p=.002), r = .169
plot(data_CLEAN$noun_sum, data_CLEAN$RWAZSMean)


#### histograms of noun scores and RWAImm etc. scores #### 
hist(data_CLEAN$noun_sum) # left skew
hist(data_CLEAN$ImmigrationZSMean) 
hist(data_CLEAN$RWAZSMean) #right-skew
hist(data_CLEAN$RWAImm)


#### correlations against essentialism 

colnames(data_CLEAN[, 18:25]) #8 Discreteness items
#to make it high score = more essentialist, need to re-score items dis1,2,4,6
data_CLEAN$dis1 = 6-data_CLEAN$dis1
data_CLEAN$dis2 = 6-data_CLEAN$dis2
data_CLEAN$dis4 = 6-data_CLEAN$dis4
data_CLEAN$dis6 = 6-data_CLEAN$dis6
#now the scale for all dis items is higher = more essentialist 
data_CLEAN$Discreteness<-((scale(data_CLEAN[, 18]) + scale(data_CLEAN[, 19]) + scale(data_CLEAN[, 20]) + scale(data_CLEAN[, 21]) + scale(data_CLEAN[, 22])  + scale(data_CLEAN[, 23]) + scale(data_CLEAN[, 24]) + scale(data_CLEAN[, 25]))/8)

describe(data_CLEAN$Discreteness) #Mean=0, SD=0.63, Median=0.05, Skew=-0.05, Kurtosis=-0.36, Range=-1.16 to 1.72

#non-z-scored version of RWA for reporting descriptive stats 
describe(rowMeans(data_CLEAN[, 18:25])) #Mean=2.82, SD=0.6, Median 2.88, Skew=-0.05, Kurtosis=-0.4, Range=1.25-4.5


colnames(data_CLEAN[, 33:35]) #3 IPT items
data_CLEAN$IPT<-((scale(data_CLEAN[, 33]) + scale(data_CLEAN[, 34]) + scale(data_CLEAN[, 35]))/3)
#currently scores as low = less essentialist --> re-score
data_CLEAN$IPT=(-1)*data_CLEAN$IPT #reversing 

describe(data_CLEAN$IPT) #Mean=0, SD=0.86, Median=-0.05, Skew=-0.17, Kurtosis=-0.91, Range=-2.06 to 1.92
#for descriptive stats, manually re-score
data_CLEAN$ipt1 = 6-data_CLEAN$ipt1
data_CLEAN$ipt2 = 6-data_CLEAN$ipt2
data_CLEAN$ipt3 = 6-data_CLEAN$ipt3
describe((rowMeans(data_CLEAN[, 33:35]))) #Mean=3.07, SD=0.87, Median=3, Skew=-0.16, Kurtosis=-0.91, Range=1-5


#now compute correlations of noun_sum against Discreteness and IPT 
cor.test(data_CLEAN$noun_sum, data_CLEAN$Discreteness) #p=.001, r= 0.182
cor.test(data_CLEAN$noun_sum, data_CLEAN$IPT) #p=.011, r= 0.141

#### adjust Study 1 p-values for essentialsim 
unadjusted=c(.001, .011) #Nouns ~ Essentialism 
unadjusted=c(.001, .001) #Implicit Social Conservatism ~ Essentialism
adjusted <- p.adjust(unadjusted, method = "holm")
p.table<-cbind(adjusted, unadjusted)
p.table 
#.002, .011 for Nouns ~ Essentialism 
#.002, .002 for Implicit Social Conservatism ~ Essentialism



#what about essentialism against politics? 
cor.test(data_CLEAN$ImmigrationZSMean, data_CLEAN$Discreteness) #p = 1.77e-06, r=0.262
cor.test(data_CLEAN$RWAZSMean, data_CLEAN$Discreteness) #p=1.833e-08, r=0.306
cor.test(data_CLEAN$RWAImmg, data_CLEAN$Discreteness) #p=1.113e-089, r=0.311
#plot
plot(data_CLEAN$RWAZSMean, data_CLEAN$Discreteness)


cor.test(data_CLEAN$ImmigrationZSMean, data_CLEAN$IPT) #p=0.0005074, r=0.192
cor.test(data_CLEAN$RWAZSMean, data_CLEAN$IPT) #p=1.57e-05, r=0.237
cor.test(data_CLEAN$RWAImmg, data_CLEAN$IPT) #p=2.047e-05, r=0.234

#what about 2 essentialism scales against one another? 
cor.test(data_CLEAN$IPT, data_CLEAN$Discreteness) #p=1.089e-15, r=.426



#cronbach's alpha for Essentialism items 
colnames(data_CLEAN)

#for discreteness
library(ltm)
cronbach.alpha(data_CLEAN[,18:25]) #0.78

#for IPT
cronbach.alpha(data_CLEAN[,33:35]) #0.83

#for average 
cronbach.alpha(data_CLEAN[, c(18:25, 33:35)]) #0.503
cronbach.alpha(data_CLEAN[, c(18:25, 33:35)], standardized = FALSE, CI = FALSE, 
               probs = c(0.025, 0.975), B = 1000, na.rm = FALSE)


#### Mediation analyses ####
library(lavaan)
library(tidyverse)
library(psych)
data_CLEAN %>% 
  select(noun_sum, RWAImmg, Discreteness, IPT) %>% 
  pairs.panels()

mod1 <- "# direct effect
          noun_sum ~ c * RWAImmg

          # mediator
          noun_sum ~ a * Discreteness
          Discreteness ~ b * RWAImmg

         # indirect and total effects
         ab := a * b
         total := c + (a*b)"

set.seed(1234)
fsem1 <- sem(mod1, data = data_CLEAN)
summary(fsem1, standardized = TRUE)


mod2 <- "# direct effect
          noun_sum ~ c * RWAImmg

        # mediator
        noun_sum ~ a * IPT
        IPT ~ b * RWAImmg
        
        # indirect and total effects
        ab := a * b
        total := c + (a*b)"

set.seed(1234)
fsem2 <- sem(mod2, data = data_CLEAN)
summary(fsem2, standardized = TRUE)




                            