directory = "/Users/danielgallegos/Documents/Stanford/JunFall/cs229/project/cs229"
setwd(directory)

x.aapl = read.csv("aapl/x.csv")
y.aapl = read.csv("aapl/y.csv")
x.msft = read.csv("msft/x.csv")
y.msft = read.csv("msft/y.csv")
x.tsla = read.csv("tsla/x.csv")
y.tsla = read.csv("tsla/y.csv")
x.amzn = read.csv("amzn/x.csv")
y.amzn = read.csv("amzn/y.csv")

library(e1071)

train = x.aapl
train$price_change = y.aapl$price_change
train$price_change = (train$price_change > 0)*2 - 1

test = x.amzn
test$price_change = y.amzn$price_change
test$price_change = (test$price_change > 0)*2 - 1


svm.fit = svm(price_change~., data = train, kernel = "linear", scale = FALSE)
summary(svm.fit)
preds = predict(svm.fit, test)

mean(test$price_change != preds)
