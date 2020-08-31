
library(plyr)
library(dplyr)
#library(lmtest)
library(ggplot2)
#library(hrbrthemes)
#library(viridis)
library(jtools)
library(lsr) #for cohensD
library(psych)
library(mousetrap)
library(diptest)
library(tidyr)
library("ggpubr")
library(car)





#read in results - from home directory

#1. read in new df - without hubs/authorities scores 
df <- read.csv('study2_RESULTS_df_multiverse_6.csv', stringsAsFactors = FALSE)
colnames(df)
#drop first column 'X'
df <- subset(df, select = -c(1))
colnames(df)
#df is a daaframe with 34284 observations of 9 variables 

#check null values in entire df 
indx <- apply(df, 2, function(x) any(is.na(x) | is.infinite(x)))
indx #there are some missing values in hubs - drop these: 
#library(tidyr)
df <- df %>% drop_na(hubs)
#now df is a dataframe with 33958 observations of 9 variables 

describe(df)



######################################
######## Split hubs scores into 2 groups ########
LEFT$hubs_group <- ifelse(LEFT$hubs < mean(LEFT$hubs), "Low_centr", "High_centr")
RIGHT$hubs_group <- ifelse(RIGHT$hubs < mean(RIGHT$hubs), "Low_centr", "High_centr")	
df_final <- rbind(LEFT, RIGHT) #33958 observartions of 10 variables


#new sample size: 
table(df_final$hubs_group, df_final$side)

summary(df_final)

#if we plot it now, high_centr will come before low_centr on the graph
#create new variable identical to hubs_group but in ascending centrality
df_final$hubs_group_asc = reorder(df_final$hubs_group, desc(df_final$hubs_group))
levels(df_final$hubs_group_asc) # "Low_centr"  "High_centr"
# = c('Less_political','More_political')



#### randomly sample 5 times & run the section below ####
df_original_final <- df_final


set.seed(42) #sample1
new_df <- df_original_final %>% filter(hubs_group_asc == "High_centr") %>% group_by(side) %>% sample_n(4271)
new_df2 <- df_original_final %>% filter(hubs_group_asc == "Low_centr") %>% group_by(side) %>% sample_n(4271)
sample1 <- rbind(new_df, new_df2) #17084 obs of 11 variables 
df_final <- sample1

set.seed(43) #sample2
new_df <- df_original_final %>% filter(hubs_group_asc == "High_centr") %>% group_by(side) %>% sample_n(4271)
new_df2 <- df_original_final %>% filter(hubs_group_asc == "Low_centr") %>% group_by(side) %>% sample_n(4271)
sample2 <- rbind(new_df, new_df2) #17084 obs of 11 variables 
df_final <- sample2

set.seed(44) #sample3
new_df <- df_original_final %>% filter(hubs_group_asc == "High_centr") %>% group_by(side) %>% sample_n(4271)
new_df2 <- df_original_final %>% filter(hubs_group_asc == "Low_centr") %>% group_by(side) %>% sample_n(4271)
sample3 <- rbind(new_df, new_df2) #17084 obs of 11 variables 
df_final <- sample3

set.seed(45) #sample4
new_df <- df_original_final %>% filter(hubs_group_asc == "High_centr") %>% group_by(side) %>% sample_n(4271)
new_df2 <- df_original_final %>% filter(hubs_group_asc == "Low_centr") %>% group_by(side) %>% sample_n(4271)
sample4 <- rbind(new_df, new_df2) #17084 obs of 11 variables 
df_final <- sample4

set.seed(46) #sample5
new_df <- df_original_final %>% filter(hubs_group_asc == "High_centr") %>% group_by(side) %>% sample_n(4271)
new_df2 <- df_original_final %>% filter(hubs_group_asc == "Low_centr") %>% group_by(side) %>% sample_n(4271)
sample5 <- rbind(new_df, new_df2) #17084 obs of 11 variables 
df_final <- sample5


sample_size_hubs = df_final %>% group_by(hubs_group_asc, side) %>% summarize(num=n())
sample_size_hubs

colnames(df_final)

chisq.test(df_final$hubs_group_asc, df_final$side) #for all 5 samples: X-squared = 0, df = 1, p-value = 1
#--> assumption of independence is no longer violated 


#example descriptive stats for one of the samples - reported for sample 3 
library(psych)
describeBy(df_final$mean_N_nopronouns_open_proportion, group = df_final$hubs_group_asc)
describeBy(df_final$mean_N_nopronouns_proportion_filtered, group = df_final$hubs_group_asc)
describeBy(df_final$mean_N_nopronouns_proportion, group = df_final$hubs_group_asc)
describeBy(df_final$mean_PN_open_proportion, group = df_final$hubs_group_asc)
describeBy(df_final$mean_PN_proportion_filtered, group = df_final$hubs_group_asc)
describeBy(df_final$mean_PN_proportion, group = df_final$hubs_group_asc)



#### Build ANOVA model ####

##check assumptions for ANOVAs ####
library(car)
leveneTest(mean_PN_open_proportion ~ side*hubs_group, data=df_final)
leveneTest(mean_PN_proportion_filtered ~ side*hubs_group, data=df_final)
leveneTest(mean_PN_proportion ~ side*hubs_group, data=df_final)

leveneTest(mean_N_nopronouns_open_proportion ~ side*hubs_group, data=df_final)
leveneTest(mean_N_nopronouns_proportion_filtered ~ side*hubs_group, data=df_final)
leveneTest(mean_N_nopronouns_proportion ~ side*hubs_group, data=df_final)
#Levene's test still sig. for all 6 tests 

bartlett.test(mean_PN_open_proportion ~ interaction(side,hubs_group_asc), data=df_final) #sig
bartlett.test(mean_PN_proportion_filtered ~ interaction(side,hubs_group_asc), data=df_final) #sig
bartlett.test(mean_PN_proportion ~ interaction(side,hubs_group_asc), data=df_final) #sig

bartlett.test(mean_N_nopronouns_open_proportion ~ interaction(side,hubs_group_asc), data=df_final) #sig
bartlett.test(mean_N_nopronouns_proportion_filtered ~ interaction(side,hubs_group_asc), data=df_final) #sig
bartlett.test(mean_N_nopronouns_proportion ~ interaction(side,hubs_group_asc), data=df_final) #sig
#all sig. 




#### ANOVAs for Proper Nouns ####

## model1 
summary(aov(mean_PN_open_proportion ~ side*hubs_group_asc, data=df_final))
etaSquared(aov(mean_PN_open_proportion ~ side*hubs_group_asc, data=df_final))


  
group_by(df_final, hubs_group_asc) %>%
  summarise(
    count = n(),
    mean = mean(mean_PN_open_proportion, na.rm = TRUE),
    sd = sd(mean_PN_open_proportion, na.rm = TRUE)
  )

group_by(df_final, side) %>%
  summarise(
    count = n(),
    mean = mean(mean_PN_open_proportion, na.rm = TRUE),
    sd = sd(mean_PN_open_proportion, na.rm = TRUE)
  )

group_by(df_final, hubs_group_asc, side) %>%
  summarise(
    count = n(),
    mean = mean(mean_PN_open_proportion, na.rm = TRUE),
    sd = sd(mean_PN_open_proportion, na.rm = TRUE)
  )


#plot results of above model 1
ggplot(df_final, aes(x=reorder(hubs_group, desc(hubs_group)), y=mean_PN_open_proportion, fill=side)) + 
  geom_boxplot() +
  scale_fill_manual(values=c("red", "blue"))


sample_size_hubs = df_final %>% group_by(hubs_group_asc) %>% summarize(num=n())

df_final %>%
  left_join(sample_size_hubs) %>%
  mutate(myaxis = paste0(hubs_group_asc, "\n", "n=", num)) %>%
  ggplot( aes(x=myaxis, y=mean_PN_open_proportion, fill=side)) +
  geom_violin(width=0.5) +
  geom_boxplot(width=0.5, color="grey", alpha=0.2) +
  scale_fill_manual(values=c("red", "blue")) +
  theme(
    plot.title = element_text(size=11)
  ) +
  ggtitle("A Violin wrapping a boxplot") +
  xlab("")


#model2 
summary(aov(mean_PN_proportion_filtered ~ side*hubs_group_asc, data=df_final))
etaSquared(aov(mean_PN_proportion_filtered ~ side*hubs_group_asc, data=df_final))


# marginal means- the simple way 
group_by(df_final, side) %>%
  summarise(
    count = n(),
    mean = mean(mean_PN_open_proportion, na.rm = TRUE),
    sd = sd(mean_PN_open_proportion, na.rm = TRUE)
  )

group_by(df_final, hubs_group_asc) %>%
  summarise(
    count = n(),
    mean = mean(mean_PN_open_proportion, na.rm = TRUE),
    sd = sd(mean_PN_open_proportion, na.rm = TRUE)
  )

group_by(df_final, hubs_group_asc, side) %>%
  summarise(
    count = n(),
    mean = mean(mean_PN_proportion_filtered, na.rm = TRUE),
    sd = sd(mean_PN_proportion_filtered, na.rm = TRUE)
  )


ggplot(df_final, aes(x=hubs_group_asc, y=mean_PN_proportion_filtered, fill=side)) + 
  geom_boxplot() +
  scale_fill_manual(values=c("red", "blue"))#model5



#model3
summary(aov(mean_PN_proportion ~ side*hubs_group_asc, data=df_final))
etaSquared(aov(mean_PN_proportion ~ side*hubs_group_asc, data=df_final))

## marginal means- the simple way 
group_by(df_final, side) %>%
  summarise(
    count = n(),
    mean = mean(mean_PN_proportion, na.rm = TRUE),
    sd = sd(mean_PN_proportion, na.rm = TRUE)
  )

#by group
group_by(df_final, hubs_group_asc) %>%
  summarise(
    count = n(),
    mean = mean(mean_PN_proportion, na.rm = TRUE),
    sd = sd(mean_PN_proportion, na.rm = TRUE)
  )

ggplot(df_final, aes(x=hubs_group_asc, y=mean_PN_proportion, fill=side)) + 
  geom_boxplot() +
  scale_fill_manual(values=c("red", "blue"))#model6




### ANOVAs for Common Nouns ####
## model 4 - nouns ~ side*hubs_group_asc 
summary(aov(mean_N_nopronouns_open_proportion ~ side*hubs_group_asc, data=df_final))
etaSquared(aov(mean_N_nopronouns_open_proportion ~ side*hubs_group_asc, data=df_final))

## marginal means- the simple way 
group_by(df_final, side) %>%
  summarise(
    count = n(),
    mean = mean(mean_N_nopronouns_open_proportion, na.rm = TRUE),
    sd = sd(mean_N_nopronouns_open_proportion, na.rm = TRUE)
  )

#visualise model4
ggplot(df_final, aes(x=hubs_group_asc, y=mean_N_nopronouns_open_proportion, fill=side)) + 
  geom_boxplot() +
  scale_fill_manual(values=c("red", "blue"))



## model 5 - nouns filtered ~ hubs_centrality * side 
summary(aov(mean_N_nopronouns_proportion_filtered ~ side*hubs_group_asc, data=df_final))
etaSquared(aov(mean_N_nopronouns_proportion_filtered ~ side*hubs_group_asc, data=df_final))


## marginal means- the simple way 
group_by(df_final, hubs_group_asc) %>%
  summarise(
    count = n(),
    mean = mean(mean_N_nopronouns_proportion_filtered, na.rm = TRUE),
    sd = sd(mean_N_nopronouns_proportion_filtered, na.rm = TRUE)
  )


#visualise model5
ggplot(df_final, aes(x=hubs_group_asc, y=mean_N_nopronouns_proportion_filtered, fill=side)) + 
  geom_boxplot() +
  scale_fill_manual(values=c("red", "blue"))




## model 6 - nouns ~ hubs_centrality * side 
summary(aov(mean_N_nopronouns_proportion ~ side*hubs_group_asc, data=df_final))
etaSquared(aov(mean_N_nopronouns_proportion ~ side*hubs_group_asc, data=df_final))

## marginal means- the simple way 
group_by(df_final, side) %>%
  summarise(
    count = n(),
    mean = mean(mean_N_nopronouns_proportion, na.rm = TRUE),
    sd = sd(mean_N_nopronouns_proportion, na.rm = TRUE)
  )

#visualise model6
ggplot(df_final, aes(x=hubs_group_asc, y=mean_N_nopronouns_proportion, fill=side)) + 
  geom_boxplot() +
  scale_fill_manual(values=c("red", "blue"))



#### correct ANOVA p-values for multiple comparisons ####
#order: 3 for common nouns and 3 for proper nouns 
unadjusted=c(2.19e-09, 0.511, 1.04e-59, 2.01e-133, 3.31e-138, 5.84e-117) #Side
unadjusted=c(1.11e-04, 0.008, 2.98e-01, 2.00e-03, 7.60e-02, 8.00e-03) #Cenatrality 
unadjusted=c(1.58e-06, 0.000413, 9.52e-01, 2.45e-04, 1.70e-02, 5.00e-03) #Cenatrality, type 2, white.adjust=TRUE
unadjusted=c(2.78e-04, 0.013, 1.50e-02, 1.00e-02, 1.02e-01, 4.00e-03) #Cenatrality, type 3, white.adjust=TRUE

#unadjusted=c(.738, .773, .011, .893, .689, .756) #Interaction from type I 
adjusted <- p.adjust(unadjusted, method = "holm")
p.table<-cbind(adjusted, unadjusted)
p.table



#### plot interaction plots for models ####
library(Rmisc)
#do this 6 times for each ANOVA, chaning y-axis limits every time using scale_y_continuous
temp <- summarySE(na.omit(df_final), measurevar="mean_PN_open_proportion", groupvars=c("hubs_group_asc", "side"))
temp
#as.factor 
p = ggplot(temp, aes(x=hubs_group_asc, y=mean_PN_open_proportion, group=side, colour=side)) +
  geom_errorbar(aes(ymin=mean_PN_open_proportion-se, ymax=mean_PN_open_proportion+se), width=.1) + 
  geom_line() + 
  theme_classic(base_size = 17) + 
  labs(x = 'Hubs Centrality') + 
  labs(y = 'Mean Proper Noun open_proportion') + 
  labs(color = "Side") + 
  scale_colour_manual(values=c("red", "blue")) + 
  scale_y_continuous(labels = scales::percent_format(accuracy = 1), limits=c(0.06, 0.14)) + 
  scale_x_discrete(breaks=c("Low_centr", "High_centr"),
                   labels=c("Less central", "More central"))
p

