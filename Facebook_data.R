data = read.csv('communities_cleaned.csv', sep = ",", na.strings = '?')

data = data[, colSums(is.na(data)) == 0]

lm.fit = lm(ViolentCrimesPerPop ~ ., data = data)
summary(lm.fit)
