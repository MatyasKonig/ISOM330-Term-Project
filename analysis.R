library(leaps)

df = read.csv('cleaned_unnormalized_data.csv')
predictVars = c('murders','murdPerPop','rapes','rapesPerPop','robberies',
                'robbbPerPop','assaults','assaultPerPop','burglaries',
                'burglPerPop','larcenies','larcPerPop','autoTheft','autoTheftPerPop',
                'arsons','arsonsPerPop','ViolentCrimesPerPop','nonViolPerPop')

df_ViolentCrimesPerPop = df[, -which(names(df) %in% c(predictVars,'ViolentCrimesPerPop'))]
  
regit.bwd = regsubsets(ViolentCrimesPerPop~.-state-communityname-fold-state_abv,data=df,nvmax=100,method='backward')
summary(regit.bwd)

bestmodel = which.max(summary(regit.bwd)$adjr2)
summary_bestmodel = summary(regit.bwd)$which[bestmodel,]
summary_bestmodel

bestVars = names(summary_bestmodel[summary_bestmodel == TRUE])
bestVars

df.lm = df[, which(names(df) %in% c(bestVars,'state_abv','ViolentCrimesPerPop'))]
df.lm

lm.fit = lm(ViolentCrimesPerPop~.-state,data=df.lm)
summary(lm.fit)

