rm(list=ls())
setwd('C:/Users/Tariq/Dropbox (MIT)/Projects/3. ITS/Tweet Topics-Demographics Corr/')

demog = read.csv('AGG_AGE_GENDER.csv')
demog$total = rowSums(demog[,-c(53,54)])
demog2 = demog[,-c(53,54,55)]/demog[,55] * 100
demog2$HAY_ID = demog$HAY_ID
demog2$SUB_MUNICIPALITY = demog$SUB_MUNICIPALITY
demog2$total = rowSums(demog2[,-c(53,54)])
sapply(demog2[!is.na(demog2$total),],range)
sapply(demog2[!is.na(demog2$total),],IQR)
sapply(demog2[!is.na(demog2$total),],var)
sapply(demog2[!is.na(demog2$total),],sd)


edu = read.csv('AGG_EDUCATION_LEVEL.csv')
edu$total = rowSums(edu[,-c(1,18)])
edu2 = edu[,-c(1,18,19)] / edu[,19] * 100
edu2$HAY_ID = edu$HAY_ID
edu2$SUB_MUNICIPALITY = edu$SUB_MUNICIPALITY
edu2$total = rowSums(edu2[,-c(17,18)])
sapply(edu2[!is.na(edu2$total),],range)
sapply(edu2[!is.na(edu2$total),],IQR)
sapply(edu2[!is.na(edu2$total),],var)
sapply(edu2[!is.na(edu2$total),],sd)


emp = read.csv('AGG_EMP_STATUS.csv')
emp$total = rowSums(emp[,-c(1,16)])
emp2 = emp[,-c(1,16,17)] / emp[,17] * 100
emp2$HAY_ID = emp$HAY_ID
emp2$SUB_MUNICIPALITY = emp$SUB_MUNICIPALITY
emp2$total = rowSums(emp2[,-c(15,16)])
sapply(emp2[!is.na(emp2$total),],range)
sapply(emp2[!is.na(emp2$total),],IQR)
sapply(emp2[!is.na(emp2$total),],var)
sapply(emp2[!is.na(emp2$total),],sd)


family = read.csv('AGG_FAMILY_TYPE.csv')
family$total = rowSums(family[,-c(1,12)])
family2 = family[,-c(1,12,13)] / family[,13] * 100
family2$HAY_ID = family$HAY_ID
family2$SUB_MUNICIPALITY = family$SUB_MUNICIPALITY
family2$total = rowSums(family2[,-c(11,12)])
sapply(family2[!is.na(family2$total),],range)
sapply(family2[!is.na(family2$total),],IQR)
sapply(family2[!is.na(family2$total),],var)
sapply(family2[!is.na(family2$total),],sd)


income = read.csv('AGG_INCOME_LEVEL.csv')
income$total = rowSums(income[,-c(1,48)])
income2 = income[,-c(1,48,49)] / income[,49] * 100
income2$HAY_ID = income$HAY_ID
income2$SUB_MUNICIPALITY = income$SUB_MUNICIPALITY
income2$total = rowSums(income2[,-c(47,48)])
sapply(income2[!is.na(income2$total),],range)
sapply(income2[!is.na(income2$total),],IQR)
sapply(income2[!is.na(income2$total),],var)
sapply(income2[!is.na(income2$total),],sd)



nei = read.csv('neighborhoods_IDs.csv', colClasses=c("numeric","character","numeric") )
nei = nei[order(nei$NEIGHBORH1),]
nei = nei[23:193,]
nei_topics = read.csv('nei_topic.csv',  colClasses=c(rep("numeric",100),"character") )
nei_topics = nei_topics[order(nei_topics$neighborhood),]

setdiff(nei$NEIGHBORH1,nei_topics$neighborhood)     # find neighborhoods in nei_topics dataset
nei = nei[-c(18,68,108),]                           # remove rows 18, 68, 108
nei_topics$Hay_ID = nei$Hay_ID
nei_topics = nei_topics[order(nei_topics$Hay_ID),]
nei_topics = nei_topics[11:167,]                    # get neighborhoods with IDs available in demographics datasets

inBoth = intersect(demog2$HAY_ID,nei_topics$Hay_ID)
demog2 = subset(demog2, HAY_ID %in% inBoth)
edu2 = subset(edu2, HAY_ID %in% inBoth)
emp2 = subset(emp2, HAY_ID %in% inBoth)
family2 = subset(family2, HAY_ID %in% inBoth)
income2 = subset(income2, HAY_ID %in% inBoth)


#---------------- AGGREGATION BEFORE CORRELATION------------------------
demog2$SAUDI_MALE_0_20 = demog2$SAUDI_MALE_0_5 + demog2$SAUDI_MALE_5_10 + demog2$SAUDI_MALE_10_15 + demog2$SAUDI_MALE_15_20
demog2$SAUDI_FEMALE_0_20 = demog2$SAUDI_FEMALE_0_5 + demog2$SAUDI_FEMALE_5_10 + demog2$SAUDI_FEMALE_10_15 + demog2$SAUDI_FEMALE_15_20
demog2$NON_SAUDI_MALE_0_20 = demog2$NON_SAUDI_MALE_0_5 + demog2$NON_SAUDI_MALE_5_10 + demog2$NON_SAUDI_MALE_10_15 + demog2$NON_SAUDI_MALE_15_20
demog2$NON_SAUDI_FEMALE_0_20 = demog2$NON_SAUDI_FEMALE_0_5 + demog2$NON_SAUDI_FEMALE_5_10 + demog2$NON_SAUDI_FEMALE_10_15 + demog2$NON_SAUDI_FEMALE_15_20

demog2$SAUDI_MALE_20_40 = demog2$SAUDI_MALE_20_25 + demog2$SAUDI_MALE_25_30 + demog2$SAUDI_MALE_30_35 + demog2$SAUDI_MALE_35_40
demog2$SAUDI_FEMALE_20_40 = demog2$SAUDI_FEMALE_20_25 + demog2$SAUDI_FEMALE_25_30 + demog2$SAUDI_FEMALE_30_35 + demog2$SAUDI_FEMALE_35_40
demog2$NON_SAUDI_MALE_20_40 = demog2$NON_SAUDI_MALE_20_25 + demog2$NON_SAUDI_MALE_25_30 + demog2$NON_SAUDI_MALE_30_35 + demog2$NON_SAUDI_MALE_35_40
demog2$NON_SAUDI_FEMALE_20_40 = demog2$NON_SAUDI_FEMALE_20_25 + demog2$NON_SAUDI_FEMALE_25_30 + demog2$NON_SAUDI_FEMALE_30_35 + demog2$NON_SAUDI_FEMALE_35_40

demog2$SAUDI_MALE_OVER_40 = demog2$SAUDI_MALE_40_45 + demog2$SAUDI_MALE_45_50 + demog2$SAUDI_MALE_50_55 + demog2$SAUDI_MALE_55_60 + demog2$SAUDI_MALE_OVER_60
demog2$SAUDI_FEMALE_OVER_40 = demog2$SAUDI_FEMALE_40_45 + demog2$SAUDI_FEMALE_45_50 + demog2$SAUDI_FEMALE_50_55 + demog2$SAUDI_FEMALE_55_60 + demog2$SAUDI_FEMALE_OVER_60
demog2$NON_SAUDI_MALE_OVER_40 = demog2$NON_SAUDI_MALE_40_45 + demog2$NON_SAUDI_MALE_45_50 + demog2$NON_SAUDI_MALE_50_55 + demog2$NON_SAUDI_MALE_55_60 + demog2$NON_SAUDI_MALE_OVER_60
demog2$NON_SAUDI_FEMALE_OVER_40 = demog2$NON_SAUDI_FEMALE_40_45 + demog2$NON_SAUDI_FEMALE_45_50 + demog2$NON_SAUDI_FEMALE_50_55 + demog2$NON_SAUDI_FEMALE_55_60 + demog2$NON_SAUDI_FEMALE_OVER_60


edu2$NOT_EDUCATED_SAUDI = edu2$ILLETERATE_SAUDI + edu2$READ_ONLY_SAUDI + edu2$READ_WRITE_SAUDI
edu2$HALF_EDUCATED_SAUDI = edu2$PRIMARY_SAUDI + edu2$INTERMEDIATE_SAUDI + edu2$SECONDARY_SAUDI
edu2$EDUCATED_SAUDI = edu2$UNIVERSITY_SAUDI + edu2$POST_GRADUATE_SAUDI
edu2$NOT_EDUCATED_NON_SAUDI = edu2$ILLETERATE_NON_SAUDI + edu2$READ_ONLY_NON_SAUDI + edu2$READ_WRITE_NON_SAUDI
edu2$HALF_EDUCATED_NON_SAUDI = edu2$PRIMARY_NON_SAUDI + edu2$INTERMEDIATE_NON_SAUDI + edu2$SECONDARY_NON_SAUDI
edu2$EDUCATED_NON_SAUDI = edu2$UNIVERSITY_NON_SAUDI + edu2$POST_GRADUATE_NON_SAUDI

income2$INCSR_SAUDI_UNDER_3000 = income2$INCSR__SAUDI_UNDER_1000 + income2$INCSR_SAUDI_1000_1999 + income2$INCSR_SAUDI_2000_2999
income2$INCSR_NON_SAUDI_UNDER_3000 = income2$INCSR__NON_SAUDI_UNDER_1000 + income2$INCSR_NON_SAUDI_1000_1999 + income2$INCSR_NON_SAUDI_2000_2999
income2$INCSR_SAUDI_3000_9999 = rowSums(income2[,c(7,9,11,13,15)])
income2$INCSR_NON_SAUDI_3000_9999 = rowSums(income2[,c(8,10,12,14,16)])
income2$INCSR_SAUDI_OVER_10000 = rowSums(income2[,c(17,19,21,23,25,27,29,31,33,35,37,39,41,43,45)])
income2$INCSR_NON_SAUDI_OVER_10000 = rowSums(income2[,c(18,20,22,24,25,26,28,30,32,34,36,38,40,42,44,46)])

emp2$WORK_UNABLE_SAUDI <- NULL
emp2$WORK_UNABLE_NON_SAUDI <- NULL
emp2$NOT_SEARCH_JOB_SAUDI <- NULL
emp2$NOT_SEARCH_JOB_NON_SAUDI <- NULL

family2$UNRELATED_INDIVID_SAUDI<- NULL
family2$UNRELATED_INDIVID_NON_SAUDI <- NULL
#-----------------------------------------------------------------------

# Merging all five neighborhood datasets with tweet_topics of neighborhoods to test correlations
#all = cbind(demog2[,-c(53,54,55)],edu2[,-c(17,18,19)],emp2[,-c(15,16,17)],family2[,-c(11,12,13)],income2[,-c(47,48,49)],nei_topics,family2[,12])
all = cbind(demog2[,56:67],edu2[,20:25],emp2[,-c(11,12,13)],family2[,-c(9,10,11)],income2[,50:55],nei_topics,family2[,10])

write.csv(all,'nei_tweets_demographics.csv')

library(Hmisc)
all_corr = rcorr(as.matrix(all[,1:238]))
demog_tweet_corr = all_corr$r[139:238,1:138]
demog_tweet_pvalue = all_corr$P[139:238,1:138]
#---- after aggregation
all_corr = rcorr(as.matrix(all[,1:142]))
demog_tweet_corr = all_corr$r[43:142,1:42]
demog_tweet_pvalue = all_corr$P[43:142,1:42]
#----
#Getting row and column names of significant correlations
significant = demog_tweet_pvalue[!is.na(demog_tweet_pvalue) & demog_tweet_pvalue < 0.05]
significant = unique(significant)
significant_df = data.frame(Topic='character', Demographic='character', Pvalue='character',
                                       Corr='character', stringsAsFactors=FALSE)
#row_index = as.integer(1)
#significant_df = c('1','1','1','1')
for (i in 1:length(significant)){
     k <- which(demog_tweet_pvalue == significant[i], arr.ind=TRUE)
     for (j in 1:(length(k)/2) ){
          row <- rownames(demog_tweet_pvalue)[k[,1]][j]
          col <- colnames(demog_tweet_pvalue)[k[,2]][j]
          new_row <- data.frame( Topic=row, Demographic=col, Pvalue=significant[i], Corr=demog_tweet_corr[row,col])
          significant_df = rbind(significant_df,new_row)
          #row_index = as.integer(row_index + 1)
     }
}

significant_df = significant_df[order(significant_df$Corr),]
Topic = as.integer(significant_df$Topic)
#------------which(demog_tweet_corr > 0.16, arr.ind=TRUE)


