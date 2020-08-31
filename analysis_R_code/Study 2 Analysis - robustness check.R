
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
df <- read.csv('study2_RESULTS_df_robustnesscheck_full.csv', stringsAsFactors = FALSE)
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



#### Descriptive Statisitcs ####

LEFT <- subset(df, side == 'LEFT')
RIGHT <- subset(df, side == 'RIGHT')

#summary(df$mean_N_nopronouns_proportion)
describe(df$mean_PN_open_proportion)
median(LEFT$mean_N_nopronouns_open_proportion)
sd(df$mean_PN_open_proportion)
#summary(df$mean_N_proportion_filtered)
#summary(df)

describe(LEFT$mean_N_nopronouns_proportion)
#summary(LEFT$mean_N_nopronouns_proportion_filtered)
describe(RIGHT$mean_N_nopronouns_proportion)
#summary(RIGHT$mean_N_nopronouns_proportion_filtered)

describe(LEFT$mean_PN_open_proportion)
describe(RIGHT$mean_PN_open_proportion)
#summary(LEFT$mean_PN_proportion)
#summary(RIGHT$mean_PN_proportion_filtered)

#sample size by group
sample_size = df %>% group_by(side) %>% summarize(num=n())
sample_size 
#1 LEFT  17788
#2 RIGHT 16170 (instead of 16496)



#plot histograms of different noun proportions
df %>%
  ggplot( aes(x=mean_N_PN_open_proportion, fill=side)) +
  geom_histogram( color="#e9ecef", alpha=0.6, position = 'identity', bins = 100) +
  scale_fill_manual(values=c("red3", "blue3"))


#violin plots 
# sample size
sample_size = df %>% group_by(side) %>% summarize(num=n())
# Plot
df %>%
  left_join(sample_size) %>%
  mutate(myaxis = paste0(side, "\n", "n=", num)) %>%
  ggplot( aes(x=myaxis, y=mean_Propernoun_proportion, fill=side)) +
  geom_violin(width=0.5) +
  geom_boxplot(width=0.1, color="grey", alpha=0.2) +
  scale_fill_manual(values=c("red", "blue")) +
  theme(
    legend.position="none",
    plot.title = element_text(size=11)
  ) +
  ggtitle("A Violin wrapping a boxplot") +
  xlab("")



#### find SD and other descriptives for my data
library(psych)
describeBy(df$mean_PN_proportion, group = df$side)
describeBy(df$mean_PN_proportion_filtered, group = df$side)
describeBy(df$mean_PN_open_proportion, group = df$side)

describeBy(df$mean_N_nopronouns_proportion, group = df$side)
describeBy(df$mean_N_nopronouns_proportion_filtered, group = df$side)
describeBy(df$mean_N_nopronouns_open_proportion, group = df$side)


describeBy(df$hubs, group = df$side) #this belongs to the continuous approach below 

describeBy(df$mean_N_nopronouns_proportion_filtered, group = df_final$hubs_group_asc)

df_final %>% group_by(hubs_group_asc) %>% summarise(mean(mean_N_nopronouns_proportion_filtered), sd(mean_N_nopronouns_proportion_filtered))

######################################
######## Split hubs scores into 2 groups, my the mean ########
LEFT$hubs_group <- ifelse(LEFT$hubs < mean(LEFT$hubs), "Low_centr", "High_centr")
RIGHT$hubs_group <- ifelse(RIGHT$hubs < mean(RIGHT$hubs), "Low_centr", "High_centr")	
df_final <- rbind(LEFT, RIGHT) #33958 observartions of 10 variables


#new sample size: 
table(df_final$hubs_group, df_final$side)

summary(df_final)

#if we plot it now, high_centr will come before low_centr on the graph


df_final$hubs_group_asc = df_final$hubs_group
str(df_final$hubs_group_asc) # "Low_centr"  "High_centr"

df_final$hubs_group_asc = reorder(df_final$hubs_group, desc(df_final$hubs_group))
levels(df_final$hubs_group_asc) # "Low_centr"  "High_centr"
# = c('Less_political','More_political')



#### Build ANOVA model ####

##check assumptions for ANOVAs
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



#print out means by group 
#model.tables(model1, type="means", se = TRUE)

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
    mean = mean(mean_PN_open_proportion, na.rm = TRUE),
    sd = sd(mean_PN_open_proportion, na.rm = TRUE)
  )



## model1 as an imbalanced design 
model1 <- lm(mean_PN_open_proportion ~ side * hubs_group_asc, data = df_final)
Anova(model1, type='III')
## effect size for model1
#library(lsr)
etaSquared(model1, type = 3, anova = TRUE )
format(1.562090e-04 , scientific=FALSE)

group_by(df_final, side) %>%
  summarise(
    count = n(),
    mean = mean(mean_PN_open_proportion, na.rm = TRUE),
    sd = sd(mean_PN_open_proportion, na.rm = TRUE), 
    median = median(mean_PN_open_proportion, na.rm=TRUE)
  )

#plot results of above model 1
ggplot(df_final, aes(x=reorder(hubs_group, desc(hubs_group)), y=mean_PN_open_proportion, fill=side)) + 
  geom_boxplot() +
  scale_fill_manual(values=c("red", "blue"))


df_final %>%
  left_join(sample_size_hubs) %>%
  mutate(myaxis = paste0(hubs_group, "\n", "n=", num)) %>%
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
model2 <- lm(mean_PN_proportion_filtered ~ side * hubs_group_asc, data = df_final)
Anova(model2, type='III')
## effect size for model1
#library(lsr)
etaSquared(model2, type = 3, anova = TRUE )
format(6.923302e-03 , scientific=FALSE)


# marginal means- the simple way 
group_by(df_final, side) %>%
  summarise(
    count = n(),
    mean = mean(mean_PN_proportion_filtered, na.rm = TRUE),
    sd = sd(mean_PN_proportion_filtered, na.rm = TRUE), 
    median = median(mean_PN_proportion_filtered, na.rm=TRUE)
  )


ggplot(df_final, aes(x=hubs_group_asc, y=mean_PN_proportion_filtered, fill=side)) + 
  geom_boxplot() +
  scale_fill_manual(values=c("red", "blue"))#model5



#model3
model3 <- lm(mean_PN_proportion ~ side * hubs_group_asc, data = df_final)
Anova(model3, type='III')
etaSquared(model3, type = 3, anova = TRUE )
format(6.757913e-05 , scientific=FALSE)

## marginal means- the simple way 
group_by(df_final, hubs_group_asc) %>%
  summarise(
    count = n(),
    mean = mean(mean_PN_proportion, na.rm = TRUE),
    sd = sd(mean_PN_proportion, na.rm = TRUE)
  )

#by group
group_by(df_final, hubs_group_asc, side) %>%
  summarise(
    count = n(),
    mean = mean(mean_PN_proportion, na.rm = TRUE),
    sd = sd(mean_PN_proportion, na.rm = TRUE)
  )

ggplot(df_final, aes(x=hubs_group_asc, y=mean_PN_proportion, fill=side)) + 
  geom_boxplot() +
  scale_fill_manual(values=c("red", "blue"))#model6




### Nouns 
## model 4 - nouns ~ hubs_centrality * side 
model4 <- lm(mean_N_nopronouns_open_proportion ~ side * hubs_group_asc, data = df_final)
Anova(model4, type='III')
etaSquared(model4, type = 3, anova = TRUE )
format(5.934e-05 , scientific=FALSE)




## marginal means- the simple way 
group_by(df_final, hubs_group_asc) %>%
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
model5 <- lm(mean_N_nopronouns_proportion_filtered ~ side * hubs_group_asc, data = df_final)
Anova(model5, type='III')
etaSquared(model5, type = 3, anova = TRUE )
format(1.445156e-04 , scientific=FALSE)

## marginal means- the simple way 
group_by(df_final, side, hubs_group_asc) %>%
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
model6 <- lm(mean_N_nopronouns_proportion ~ side * hubs_group_asc, data = df_final)
Anova(model6, type='III')
etaSquared(model6, type = 3, anova = TRUE )
format(1.870936e-04, scientific=FALSE)

## marginal means- the simple way 
group_by(df_final, hubs_group_asc, side) %>%
  summarise(
    count = n(),
    mean = mean(mean_N_nopronouns_proportion, na.rm = TRUE),
    sd = sd(mean_N_nopronouns_proportion, na.rm = TRUE)
  )

#visualise model6
ggplot(df_final, aes(x=hubs_group_asc, y=mean_N_nopronouns_proportion, fill=side)) + 
  geom_boxplot() +
  scale_fill_manual(values=c("red", "blue"))



#### correct ANOVA p-values for multiple comparisons, order: 3 for common nouns and 3 for proper nouns 
unadjusted=c(0.00006, .856, 2.438e-16, 2e-16, 2e-16, 2e-16 ) #Side
unadjusted=c(0.0014, .027, .399, .021, .130, .095 ) #Centrality 
unadjusted=c(.716, .770, .011, .959, .804, .596) #Interactions

#unadjusted=c(.738, .773, .011, .893, .689, .756) #Interaction from type I 
adjusted <- p.adjust(unadjusted, method = "holm")
p.table<-cbind(adjusted, unadjusted)
p.table

format(1.20e-04, scientific=FALSE)



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



