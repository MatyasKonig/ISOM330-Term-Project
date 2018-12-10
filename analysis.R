library(leaps)
library(car)
library(corrplot)
library(caret)
df = read.csv('Data/cleaned_unnormalized_data.csv')

predictVars = c('murders','murdPerPop','rapes','rapesPerPop','robberies',
                'robbbPerPop','assaults','assaultPerPop','burglaries',
                'burglPerPop','larcenies','larcPerPop','autoTheft','autoTheftPerPop',
                'arsons','arsonsPerPop','nonViolPerPop')

#exclude other predictive variables
df_ViolentCrimesPerPop = df[, -which(names(df) %in% c(predictVars,'fold'))]
df_ViolentCrimesPerPop_num = df_ViolentCrimesPerPop[, unlist(lapply(df_ViolentCrimesPerPop,is.numeric))]
#df_ViolentCrimesPerPop_num = df_ViolentCrimesPerPop_num[, -which(names(df_ViolentCrimesPerPop_num) == 'population')]
### DETECT MULTICOLINARITY
cor = cor(df_ViolentCrimesPerPop_num)
corrplot(cor,tl.cex=0.4,order='hclust')

highCorr = findCorrelation(cor, cutoff=0.75,names=FALSE)
highCorr

#create rate for highly correlated variables
df_ViolentCrimesPerPop_num$pctInShelters = df_ViolentCrimesPerPop_num$NumInShelters/df_ViolentCrimesPerPop_num$population

#var to keep
var_to_keep = c('population','PctPopUnderPov',"PctNotHSGrad","PctEmploy",'PctKidsBornNeverMar','state')

#take out vars highly correlated
df_ViolentCrimesPerPop_num=df_ViolentCrimesPerPop_num[-highCorr]
cor1 = cor(df_ViolentCrimesPerPop_num)
corrplot(cor1,tl.cex=0.4,order='hclust')

#add back in vars we care about 
df_ViolentCrimesPerPop_num = cbind(df_ViolentCrimesPerPop_num,df_ViolentCrimesPerPop[,which(names(df_ViolentCrimesPerPop) %in% var_to_keep)]) 
df_ViolentCrimesPerPop = df_ViolentCrimesPerPop_num

# best selection
regfit.full = regsubsets(ViolentCrimesPerPop ~ . -state, data = df_ViolentCrimesPerPop, nvmax = 49)
reg.summary = summary(regfit.full)
bestmodel = which.max(reg.summary$adjr2)
summart_bestmodel = reg.summary$which[bestmodel,]
summart_bestmodel

df_ViolentCrimesPerPop[reg.summary$adjr2[which.max(reg.summary$adjr2)],]

#backward selection of data
regit.bwd = regsubsets(ViolentCrimesPerPop~.-state,data=df_ViolentCrimesPerPop,nvmax=49,method='backward')
summary(regit.bwd)

bestmodel = which.max(summary(regit.bwd)$adjr2)
summary_bestmodel = summary(regit.bwd)$which[bestmodel,]
summary_bestmodel

bestVars = names(summary_bestmodel[summary_bestmodel == TRUE])
bestVars

df.lm = df[, which(names(df) %in% c(bestVars,'state','ViolentCrimesPerPop'))]
df.lm

lm.fit = lm(ViolentCrimesPerPop~.,data=df.lm)
summary(lm.fit)

