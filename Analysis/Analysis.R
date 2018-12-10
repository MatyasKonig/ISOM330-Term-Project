library(leaps)

data = read.csv('cleaned_data.csv', sep = ",", na.strings = '?')
data$state = as.factor(data$state)

summary(data)
str(data$state)

# forward selection
regfit.fwd = regsubsets(ViolentCrimesPerPop ~ . - communityname - state - fold - state_abv, data  = data, nvmax = 10, method = "forward")
summary(regfit.fwd)
