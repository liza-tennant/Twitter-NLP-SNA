
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
df <- read.csv('study2_data.csv', stringsAsFactors = FALSE)
colnames(df)
#drop first column 'X'
df <- subset(df, select = -c(1))
colnames(df)
#df is a daaframe with 34284 observations of 20 variables 

#check null values in entire df 
indx <- apply(df, 2, function(x) any(is.na(x) | is.infinite(x)))
indx #there are some missing values in hubs and authorities 
missing <- subset(df, is.na(df$hubs))
as.list(missing$user_id_str)
# drop the rows with missing centrality calculations: 
#library(tidyr)
df <- df %>% drop_na(hubs, authorities)
#now df is a dataframe with 33958 observations of 20 variables 

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



######################################
#### check hubs scores from the small graph ####
#1. read in new df - without hubs/authorities scores 
df1 <- read.csv('study2_RESULTS_df_multiverse_5.csv', stringsAsFactors = FALSE)
colnames(df1)
#drop first column 'X
df1 <- subset(df1, select = -c(1))
colnames(df1)

df<-df1 #34284 obs. of 19 variables

#sample size by group
sample_size = df %>% group_by(side) %>% summarize(num=n())
sample_size 
#1 LEFT  17788
#2 RIGHT 16496

t.test(df$hubs_small ~ df$side)

#visualise hubs_small
df %>%
  ggplot( aes(x=hubs_small, fill=side)) +
  geom_histogram( color="#e9ecef", alpha=0.6, position = 'identity', bins = 50) +
  scale_fill_manual(values=c("red3", "blue3")) +
  theme_classic(base_size = 20) +
  labs(x = "Hubs Centrality, from small graphs") + 
  labs(y = "Count") + 
  labs(fill = "Side")

df %>%
  left_join(sample_size) %>%
  mutate(myaxis = paste0(side, "\n", "n=", num)) %>%
  ggplot( aes(x=myaxis, y=hubs_small, fill=side)) +
  geom_violin(width=0.5) +
  geom_boxplot(width=0.1, color="grey", alpha=0.2) +
  scale_fill_manual(values=c("red", "blue")) +
  theme_classic(base_size = 20) +
  #theme(legend.position="none", plot.title = element_text(size=11) ) +
  ggtitle("A Violin wrapping a boxplot") +
  xlab("")



#describe distributions of hubs scores
describe(LEFT$hubs_small)#comes up with lots of 0s
describe(RIGHT$hubs_small)
ddply(RIGHT, c('side'), summarise, 
      mean=mean(hubs_small), 
      sd=sd(hubs_small), 
      max=max(hubs_small), 
      min=min(hubs_small))
df %>%
  ggplot( aes(x=hubs_small, fill=side)) +
  geom_histogram( color="#e9ecef", alpha=0.6, position = 'identity', bins = 50) +
  scale_fill_manual(values=c("red3", "blue3"))

df %>%
  group_by(hubs_small) %>%
  summarise_at(vars(mean_PN_open_proportion), funs(mean(., na.rm=TRUE)))



# preparation for analysis #
#check for multicollinearity: side ~ centrality

#hubs ~ side 
t.test(df$hubs_small ~ df$side)
cohensD(hubs_small ~ side, data = df)


library(psych)
describeBy(df$mean_N_nopronouns_open_proportion, group = df$side)
describeBy(df$mean_N_nopronouns_proportion_filtered, group = df$side)
describeBy(df$mean_N_nopronouns_proportion, group = df$side)
describeBy(df$mean_PN_open_proportion, group = df$side)
describeBy(df$mean_PN_proportion_filtered, group = df$side)
describeBy(df$mean_PN_proportion, group = df$side)







######################################
#### Create Group variable from Hubs centrality #### 
#1. re-imported df as at the top of document (from 'RESULTS_df_multiverse_6.csv')

#2. bimodality coefficient - for 17K + 16K 
#library(modes) #no longer available 
#library(mousetrap)
bimodality_coefficient(df$hubs) #0.6738521
bimodality_coefficient(LEFT$hubs) #0.8636465
bimodality_coefficient(RIGHT$hubs) #0.7784462

#library(diptest)
dip.test(df$hubs) #sig --> non-unimodal, os at least bimodal 
dip.test(LEFT$hubs) #sig --> non-unimodal, os at least bimodal 
dip.test(RIGHT$hubs) #sig --> non-unimodal, os at least bimodal 

describe(df$hubs)
describe(LEFT$hubs)
describe(RIGHT$hubs)

df %>% summarise(count = n(),
                         mean = mean(hubs, na.rm = TRUE),
                         sd = sd(hubs, na.rm = TRUE),
                 range = range(hubs, na.rm = TRUE)
)

df %>%
  ggplot( aes(x=hubs, fill=side)) +
  geom_histogram( color="#e9ecef", alpha=0.6, position = 'identity', bins = 50) +
  scale_fill_manual(values=c("red3", "blue3")) +
  theme_classic(base_size = 20) +
  labs(x = "Hubs Centrality, N=35K") + 
  labs(y = "Count") + 
  labs(fill = "Side")



#2.1 -checking bimodality for different sub-samples

## 2.1.1 are hubs bimodally distributed in the overall sample of 800K and 1.5mln? 

LEFT_hubs <- read.csv('RESULTS/hubs_scores/LEFT_hubs_noelites.csv', stringsAsFactors = FALSE, col.names=c('user_id', 'hubs'))
RIGHT_hubs <- read.csv('RESULTS/hubs_scores/RIGHT_hubs_noelites.csv', stringsAsFactors = FALSE, col.names=c('user_id', 'hubs'))

nrow(LEFT_hubs) #822752
nrow(RIGHT_hubs) #1542221

LEFT_hubs$side='LEFT'
RIGHT_hubs$side='RIGHT'
Hubs_total <- rbind(LEFT_hubs, RIGHT_hubs) #2364973 observartions 

nrow(Hubs_total) #2364973


bimodality_coefficient(LEFT_hubs$hubs) #0.8881855
bimodality_coefficient(RIGHT_hubs$hubs) #0.7649071
bimodality_coefficient(Hubs_total$hubs) #0.6163565

dip.test(LEFT_hubs$hubs) #D = 0.16535, p-value < 2.2e-16
dip.test(RIGHT_hubs$hubs) #D = 0.12286, p-value < 2.2e-16
dip.test(Hubs_total$hubs) #D = 0.10609, p-value < 2.2e-16

describe(LEFT_hubs$hubs) 
describe(RIGHT_hubs$hubs)
#sub in different data frames into this to get very small values for mean and sd
range(RIGHT_hubs$hubs)
RIGHT_hubs %>% summarise(count = n(),
                         mean = mean(hubs, na.rm = TRUE),
                         sd = sd(hubs, na.rm = TRUE)
                         )

Hubs_total %>%
  ggplot( aes(x=hubs, fill=side)) +
  geom_histogram( color="#e9ecef", alpha=0.6, position = 'identity', bins = 50) +
  scale_fill_manual(values=c("red3", "blue3")) +
  theme_classic(base_size = 20) +
  labs(x = "Hubs Centrality, N=2.3mln") + 
  labs(y = "Count") + 
  labs(fill = "Side")


Hubs_total %>%
  ggplot( aes(x=hubs, fill=side)) +
  geom_histogram( color="#e9ecef", alpha=0.6, position = 'identity', bins = 50) + 
  scale_fill_manual(values=c("red3", "blue3"))


## 2.1.2 are hubs bimodally distributed in my sample of 100K + 100K too?
sample1_LEFT <- read.csv('RESULTS/hubs_scores/sample1_LEFT_copy.csv', header=FALSE, stringsAsFactors=FALSE, col.names='user_id')
sample1_RIGHT <- read.csv('RESULTS/hubs_scores/sample1_RIGHT_copy.csv', header=FALSE, stringsAsFactors=FALSE, col.names='user_id')

nrow(sample1_LEFT) #100000
nrow(sample1_RIGHT) #100000



#now check for the users whose user_id is in the sample1_... df 
LEFT_hubs_sample <- LEFT_hubs %>% filter(user_id %in% sample1_LEFT$user_id) #99996 observations

RIGHT_hubs_sample <- RIGHT_hubs %>% filter(user_id %in% sample1_RIGHT$user_id) #98542 observations 

#create combined df for all hubs scores + side 
LEFT_hubs_sample$side='LEFT'
RIGHT_hubs_sample$side='RIGHT'
Hubs_sample <- rbind(LEFT_hubs_sample, RIGHT_hubs_sample) #198538 observartions 


bimodality_coefficient(LEFT_hubs_sample$hubs) #0.8882788
bimodality_coefficient(RIGHT_hubs_sample$hubs) #0.7655606
bimodality_coefficient(Hubs_sample$hubs) #0.6781012


dip.test(LEFT_hubs_sample$hubs) #D = 0.16483, p-value < 2.2e-16
dip.test(RIGHT_hubs_sample$hubs) #D = 0.12223, p-value < 2.2e-16
dip.test(Hubs_sample$hubs) #D = 0.112, p-value < 2.2e-16

describe(LEFT_hubs_sample$hubs) 
describe(RIGHT_hubs_sample$hubs)
describe(Hubs_sample$hubs)
#sub in different data frames into this to get very small values for mean and sd
range(Hubs_sample$hubs)
Hubs_sample %>% summarise(count = n(),
                         mean = mean(hubs, na.rm = TRUE),
                         sd = sd(hubs, na.rm = TRUE)
                         )


Hubs_sample %>%
  ggplot( aes(x=hubs, fill=side)) +
  geom_histogram( color="#e9ecef", alpha=0.6, position = 'identity', bins = 50) +
  scale_fill_manual(values=c("red3", "blue3")) +
  theme_classic(base_size = 20) +
  labs(x = "Hubs Centrality, N=200K") + 
  labs(y = "Count") + 
  labs(fill = "Side")

Hubs_sample %>%
  ggplot( aes(x=hubs, fill=side)) +
  geom_histogram( color="#e9ecef", alpha=0.6, position = 'identity', bins = 50) + 
  scale_fill_manual(values=c("red3", "blue3"))




#3. median split? 
median(LEFT$hubs) #4.034178e-07
median(RIGHT$hubs) #8.342319e-07
#plot hist with median lines 
h<-df %>%
  ggplot( aes(x=hubs, fill=side)) +
  geom_histogram( color="#e9ecef", alpha=0.6, position = 'identity', bins = 50) +
  scale_fill_manual(values=c("red3", "blue3")) +
  theme_classic(base_size = 20) +
  labs(x = "Hubs Centrality") + 
  labs(y = "Count") + 
  labs(fill = "Side") +
  geom_vline(aes(xintercept=median(LEFT$hubs)), linetype="dotted", col="red", size=2) +
  geom_vline(aes(xintercept=median(RIGHT$hubs)), linetype="dotted", col="blue", size=2)
h

#4. mean split? 
mean(LEFT$hubs) #1.058345e-06
mean(RIGHT$hubs) #6.941358e-07
#plot hist with mean lines 
h<-df %>%
  ggplot( aes(x=hubs, fill=side)) +
  geom_histogram( color="#e9ecef", alpha=0.6, position = 'identity', bins = 50) +
  scale_fill_manual(values=c("red3", "blue3")) +
  theme_classic(base_size = 20) +
  labs(x = "Hubs Centrality") + 
  labs(y = "Count") + 
  labs(fill = "Side") +
  geom_vline(aes(xintercept=mean(LEFT$hubs)), linetype="dotted", col="red", size=2) +
  geom_vline(aes(xintercept=mean(RIGHT$hubs)), linetype="dotted", col="blue", size=2)
h



######## Split hubs scores into 2 groups ########
LEFT$hubs_group <- ifelse(LEFT$hubs < mean(LEFT$hubs), "Low_centr", "High_centr")
RIGHT$hubs_group <- ifelse(RIGHT$hubs < mean(RIGHT$hubs), "Low_centr", "High_centr")	
df_final <- rbind(LEFT, RIGHT) #33958 observartions of 21 variables

#new sample size: 
table(df_final$hubs_group, df_final$side)

summary(df_final)

#if we plot it now, high_centr will come before low_centr on the graph
#hence create new variable identical to hubs_group but in ascending centrality
df_final$hubs_group_asc = df_final$hubs_group
str(df_final$hubs_group_asc) # "Low_centr"  "High_centr"

df_final$hubs_group_asc = reorder(df_final$hubs_group, desc(df_final$hubs_group))
levels(df_final$hubs_group_asc) # "Low_centr"  "High_centr"
# equivalent to c('Less_political','More_political')



#### Build ANOVA models ####

##check assumptions for ANOVAs
library(car)
leveneTest(mean_PN_open_proportion ~ side*hubs_group, data=df_final)
leveneTest(mean_PN_proportion_filtered ~ side*hubs_group, data=df_final)
leveneTest(mean_PN_proportion ~ side*hubs_group, data=df_final)

leveneTest(mean_N_nopronouns_open_proportion ~ side*hubs_group, data=df_final)
leveneTest(mean_N_nopronouns_proportion_filtered ~ side*hubs_group, data=df_final)
leveneTest(mean_N_nopronouns_proportion ~ side*hubs_group, data=df_final)
#Levene's test sig. for all 6 tests 

#install.packages("heplots")
library(heplots)
summary(boxM(formula=(mean_N_nopronouns_open_proportion ~ side : hubs_group_asc), data=df_final))

library(rstatix)
box_m(df_final[, "mean_N_nopronouns_open_proportion", drop = FALSE], df_final$hubs_group_asc, df_final$side)

library(tidyr); library(dplyr)
#Box's M
data_wide <- df_final %>% spread(hubs_group_asc, mean_N_nopronouns_open_proportion)
library(heplots)
BoxResult<-boxM(data_wide$mean_N_nopronouns_open_proportion,data_wide$Group)
BoxResult$cov
BoxResult

bartlett.test(mean_PN_open_proportion ~ interaction(side,hubs_group_asc), data=df_final) #sig
bartlett.test(mean_PN_proportion_filtered ~ interaction(side,hubs_group_asc), data=df_final) #sig
bartlett.test(mean_PN_proportion ~ interaction(side,hubs_group_asc), data=df_final) #sig

bartlett.test(mean_N_nopronouns_open_proportion ~ interaction(side,hubs_group_asc), data=df_final) #sig
bartlett.test(mean_N_nopronouns_proportion_filtered ~ interaction(side,hubs_group_asc), data=df_final) #sig
bartlett.test(mean_N_nopronouns_proportion ~ interaction(side,hubs_group_asc), data=df_final) #sig


shapiro.test(df_final$mean_PN_open_proportion) #sample size too large 

#independence - comes up as sig. due to imbalanced group sizes 
chisq.test(df_final$hubs_group_asc, df_final$side) #X-squared = 3092.5, df = 1, p-value < 2.2e-16


##model1
#using car package 
library(car)
model1 <- lm(mean_PN_open_proportion ~ side * hubs_group_asc, data = df_final)
Anova(model1, type='III')
## effect size for model1
#library(lsr)
etaSquared(model1, type = 3, anova = TRUE )
format(1.533836e-04, scientific=FALSE)

plot(model1)

#print out means by group 
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

#print interaction plot to interpret direction - in the paper, the version reported in the later section was used 
interaction.plot(x.factor = df_final$hubs_group_asc, trace.factor = df_final$side, 
                 response = df_final$mean_PN_open_proportion, fun = mean, 
                 type = "b", legend = TRUE, 
                 xlab = "Hubs group", ylab="mean_PN_open_proportion ",
                 pch=c(1,19), col = c("red", "blue"))


#check that residuals are normally distributed - Shapiro-wilk test 
aov_residuals <- residuals(object = model1)
shapiro.test(x = aov_residuals ) #doesn't work as sample too large 



## marginal means- the simple way 
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



#plot results of above model1
ggplot(df_final, aes(x=reorder(hubs_group, desc(hubs_group)), y=mean_PN_open_proportion, fill=side)) + 
  geom_boxplot() +
  scale_fill_manual(values=c("red", "blue"))

ggplot(df_final, aes(x=reorder(hubs_group, desc(hubs_group)), y=mean_PN_open_proportion)) + 
  geom_boxplot() +
  geom_jitter(height=0, width=0.1)+
  facet_grid(~side)


sample_size_hubs = df_final %>% group_by(hubs_group) %>% summarize(num=n())

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

ggplot2.violinplot(data=df_final, xName='hubs_group',yName='mean_PN_open_proportion', 
                   groupName='side',
                   groupColors=c('red','blue'))
geom_violin()

df_final %>% ggplot( aes(x=hubs_centrality, y=mean_PN_open_proportion)) +
  geom_violin(width=0.5) +
  geom_boxplot(width=0.1, color="grey", alpha=0.2) 

df_final %>% ggplot( aes(x=hubs_centrality, y=mean_PN_open_proportion, fill=side)) +
  geom_violin(width=0.5) +
  geom_boxplot(width=0.1, color="grey", alpha=0.2) +
  scale_fill_manual(values=c("red", "blue"))


colnames(df_final)
#violinBy(df_final, var=c(11, 17, 21), grp="side")




#model2 
model2<- lm(mean_PN_proportion_filtered ~ side * hubs_group_asc, data=df_final)
Anova(model2, type = "III")

etaSquared(model2, type = 3, anova = TRUE )
format(6.627728e-05, scientific=FALSE)

plot(model2)


# marginal means- the simple way 
group_by(df_final, hubs_group_asc) %>%
  summarise(
    count = n(),
    mean = mean(mean_PN_proportion_filtered, na.rm = TRUE),
    sd = sd(mean_PN_proportion_filtered, na.rm = TRUE)
  )


ggplot(df_final, aes(x=hubs_group_asc, y=mean_PN_proportion_filtered, fill=side)) + 
  geom_boxplot() +
  scale_fill_manual(values=c("red", "blue"))#model5



#model3
model3<- lm(mean_PN_proportion ~ side * hubs_group_asc, data=df_final)
Anova(model3, type = "III")

etaSquared(model3, type = 3, anova = TRUE )
format(8.063068e-05, scientific=FALSE)

plot(model3)

ggplot(df_final, aes(x=hubs_group_asc, y=mean_PN_proportion, fill=side)) + 
  geom_boxplot() +
  scale_fill_manual(values=c("red", "blue"))#model6

## marginal means- the simple way 
group_by(df_final, side) %>%
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





### Nouns 
## model 4 - nouns ~ side * hubs_centrality
model4<- lm(mean_N_nopronouns_open_proportion ~ side * hubs_group_asc, data=df_final)
Anova(model4, type="III")
#library(lsr)
etaSquared(model4, type = 3, anova = TRUE)
format(4.739879e-04, scientific=FALSE)

plot(model4)

#visualise model4
#library(ggplot2)
ggplot(df_final, aes(x=hubs_group_asc, y=mean_N_nopronouns_open_proportion, fill=side)) + 
  geom_boxplot() +
  scale_fill_manual(values=c("red", "blue"))

## marginal means- the simple way 
group_by(df_final, hubs_group_asc) %>%
  summarise(
    count = n(),
    mean = mean(mean_N_nopronouns_open_proportion, na.rm = TRUE),
    sd = sd(mean_N_nopronouns_open_proportion, na.rm = TRUE)
  )



## model 5 - nouns filtered ~ side * hubs_centrality
model5 <- lm(mean_N_nopronouns_proportion_filtered ~ side * hubs_group_asc, data=df_final)
Anova(model5, type="III")

plot(model5)

etaSquared(model5, type = 3, anova = TRUE )
format(9.705782e-07, scientific=FALSE)

#visualise model5
ggplot(df_final, aes(x=hubs_group_asc, y=mean_N_nopronouns_proportion_filtered, fill=side)) + 
  geom_boxplot() +
  scale_fill_manual(values=c("red", "blue"))

## marginal means- the simple way 
group_by(df_final, hubs_group_asc) %>%
  summarise(
    count = n(),
    mean = mean(mean_N_nopronouns_proportion_filtered, na.rm = TRUE),
    sd = sd(mean_N_nopronouns_proportion_filtered, na.rm = TRUE)
  )




## model 6 - nouns ~ hubs_centrality * side 
model6 <- lm(mean_N_nopronouns_proportion ~ side * hubs_group_asc, data=df_final)
Anova(model6, type="III")
etaSquared(model6, type = 3, anova = TRUE )
format(1.870936e-04, scientific=FALSE)

plot(model6)

#visualise model6
ggplot(df_final, aes(x=hubs_group_asc, y=mean_N_nopronouns_proportion, fill=side)) + 
  geom_boxplot() +
  scale_fill_manual(values=c("red", "blue"))

#example interaction plot - not used 
interaction.plot(x.factor     = df_final$hubs_group_asc,
                 trace.factor = df_final$side,
                 response     = df_final$mean_N_nopronouns_proportion,
                 fun = mean,
                 type="b",
                 col=c("red","blue"),  ### Colors for levels of trace var.
                 pch=c(19, 17),        ### Symbols for levels of trace var.
                 fixed=TRUE,           ### Order by factor order in data
                 leg.bty = "o")


## marginal means- the simple way 
group_by(df_final, hubs_group_asc) %>%
  summarise(
    count = n(),
    mean = mean(mean_N_nopronouns_proportion, na.rm = TRUE),
    sd = sd(mean_N_nopronouns_proportion, na.rm = TRUE)
  )



#### correct ANOVA p-values for multiple comparisons####
unadjusted=c(2e-16, .856, 2.438e-16, 2e-16, 2e-16, 2e-16) #Side
unadjusted=c(.00145, .027, .399, .021, .130, .095) #Cenatrality 
unadjusted=c(.716, .770, .011, .960, .804, .596) #Interaction
adjusted <- p.adjust(unadjusted, method = "holm")
p.table<-cbind(adjusted, unadjusted)
p.table

format(8.56e-01, scientific=FALSE)




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




