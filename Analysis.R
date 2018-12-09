library(leaps)

data = read.csv('cleaned_data.csv', sep = ",", na.strings = '?')

summary(data)
str(data)

# forward selection
regfit.fwd = regsubsets(ViolentCrimesPerPop ~ . - communityname, data  = data, nvmax = 10, method = "forward")
summary(regfit.fwd)
