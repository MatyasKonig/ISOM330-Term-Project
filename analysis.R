library(leaps)
library(car)
library(corrplot)
library(caret)
library(MASS)
library(ISLR)

df = read.csv('Data/cleaned_unnormalized_data.csv')

predictVars = c('murders','murdPerPop','rapes','rapesPerPop','robberies',
                'robbbPerPop','assaults','assaultPerPop','burglaries',
                'burglPerPop','larcenies','larcPerPop','autoTheft','autoTheftPerPop',
                'arsons','arsonsPerPop','nonViolPerPop')

#exclude other predictive variables
df_ViolentCrimesPerPop = df[, -which(names(df) %in% c(predictVars,'fold'))]
df_ViolentCrimesPerPop_num = df_ViolentCrimesPerPop[, unlist(lapply(df_ViolentCrimesPerPop,is.numeric))]

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
#-----
#divide data into training and testing sets
library(caTools)
set.seed(13)
sample=sample.split(df.lm,SplitRatio = .75)
train=subset(df.lm,sample==TRUE)
test=subset(df.lm,sample==FALSE)

#run linear model for training data
lm.fit = lm(ViolentCrimesPerPop~.,data=train)
summary(lm.fit)
train_MSE = mean(summary(lm.fit)$residuals)^2
train_MSE

#cook distance
cd = cooks.distance(lm.fit)
plot(cd,pch='*',main='Outliers by Cook"s Distance')
abline(h=1,col='red')

#run model on test data
lm.pred = predict(lm.fit,test)
test_MSE = mean(lm.pred-test$ViolentCrimesPerPop)^2
test_MSE 
#___

#classification model
quantile = quantile(df_ViolentCrimesPerPop$ViolentCrimesPerPop,.70)
quantile

#classify neighborhoods that are in the top 95 quartile of violent crimes per pop as dangerous
dangerous_neighborhood = df.lm$ViolentCrimesPerPop > quantile
df.lm[dangerous_neighborhood,]
df.lm$dangerous_neighborhood = rep(FALSE,1901)
df.lm$dangerous_neighborhood[dangerous_neighborhood] = TRUE

sampleClassification = sample.split(df.lm,SplitRatio = .75)
trainClassification = subset(df.lm,sample==TRUE)
testClassification = subset(df.lm,sample==FALSE)

#try a logistic model
glm.fits = glm(dangerous_neighborhood~.-ViolentCrimesPerPop,data=trainClassification,family=binomial)
summary(glm.fits)
#get result for training data
glm.probs_train=predict(glm.fits,type='response')
glm.pred_train=rep(FALSE,1393)
glm.pred_train[glm.probs_train>.5]=TRUE

#get result for testing data
glm.probs_test=predict(glm.fits,testClassification,type='response')
glm.pred_test=rep(FALSE,508)
glm.pred_test[glm.probs_test>.5]=TRUE

#get confusion table for training data
train_cm = table(glm.pred_train,trainClassification$dangerous_neighborhood)
train_cm
train_error_rate = (train_cm[1,2] + train_cm[2,1])/sum(train_cm)*100
train_error_rate

#get confusion table for test data
test_cm = table(glm.pred_test,testClassification$dangerous_neighborhood)
test_cm
test_error_rate = (test_cm[1,2] + test_cm[2,1])/sum(test_cm)*100
test_error_rate


#try a lda model
lda.fit = lda(dangerous_neighborhood~.-ViolentCrimesPerPop,data=train)
lda.fit

#try a KNN model
df.lm.num = df.lm[, unlist(lapply(df.lm,is.numeric))]
scale(df.lm.num)

library(class)
set.seed(13)
sampleKNN=sample.split(df.lm.num,SplitRatio = .75)
trainKNN=subset(df.lm.num,sampleKNN==TRUE)
testKNN=subset(df.lm.num,sampleKNN==FALSE)
trainKNN.dangerous_neighborhood = df.lm$dangerous_neighborhood[sampleKNN]
testKNN.dangerous_neighborhood = df.lm$dangerous_neighborhood[!sampleKNN]
knn.pred = knn(trainKNN,testKNN,trainKNN.dangerous_neighborhood,k=4)
table(knn.pred,testKNN.dangerous_neighborhood)

error.tr=c()
error.ts=c()
for (k in seq(1,10)) {
  set.seed(13)
  knntr=knn(trainKNN,trainKNN,trainKNN.dangerous_neighborhood,k=k)
  knnts=knn(trainKNN,testKNN,trainKNN.dangerous_neighborhood,k=k)
  error.tr = c(error.tr,mean(knntr!=trainKNN.dangerous_neighborhood))
  error.ts = c(error.ts,mean(knnts!=testKNN.dangerous_neighborhood))
  print(table(knnts,testKNN.dangerous_neighborhood))
}
error.tr
error.ts