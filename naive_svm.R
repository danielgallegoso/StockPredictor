directory = "/Users/danielgallegos/Documents/Stanford/JunFall/cs229/project/cs229"
setwd(directory)
trim = function(train,flag) {
  if(flag){train$date = NULL}
  train$pos = train$pos/train$total
  train$neg = train$pos/train$total
  train$pos_neighbors = train$pos_neighbors/train$total
  train$neg_neighbors = train$neg_neighbors/train$total
  train$name_mentioned = train$name_mentioned/train$total
  train$total = NULL
  return(train)
}
trim2 = function(train,flag) {
  if (flag){
    train$date = NULL
  }
  train$pos0 = train$pos0/train$total0
  train$neg0 = train$pos0/train$total0
  train$pos_neighbors0 = train$pos_neighbors0/train$total0
  train$neg_neighbors0 = train$neg_neighbors0/train$total0
  train$name_mentioned0 = train$name_mentioned0/train$total0
  train$total0 = NULL
  train$pos1 = train$pos1/train$total1
  train$neg1 = train$pos1/train$total1
  train$pos_neighbors1 = train$pos_neighbors1/train$total1
  train$neg_neighbors1 = train$neg_neighbors1/train$total1
  train$name_mentioned1 = train$name_mentioned1/train$total1
  train$total1 = NULL
  train$pos2 = train$pos2/train$total2
  train$neg2 = train$pos2/train$total2
  train$pos_neighbors2 = train$pos_neighbors2/train$total2
  train$neg_neighbors2 = train$neg_neighbors2/train$total2
  train$name_mentioned2 = train$name_mentioned2/train$total2
  train$total2 = NULL
  return(train)
}
trim1 = function(train,flag) {
  if (flag){
    train$date = NULL
  }
  train$pos0 = train$pos0/train$total0
  train$neg0 = train$pos0/train$total0
  train$pos_neighbors0 = train$pos_neighbors0/train$total0
  train$neg_neighbors0 = train$neg_neighbors0/train$total0
  train$name_mentioned0 = train$name_mentioned0/train$total0
  train$total0 = NULL
  train$pos1 = train$pos1/train$total1
  train$neg1 = train$pos1/train$total1
  train$pos_neighbors1 = train$pos_neighbors1/train$total1
  train$neg_neighbors1 = train$neg_neighbors1/train$total1
  train$name_mentioned1 = train$name_mentioned1/train$total1
  train$total1 = NULL
  return(train)
}



# Initializes the train and test data frames based on dictionaries
x.aapl = read.csv("aapl/x.csv")
y.aapl = read.csv("aapl/y.csv")
x.msft = read.csv("msft/x.csv")
y.msft = read.csv("msft/y.csv")
x.tsla = read.csv("tsla/x.csv")
y.tsla = read.csv("tsla/y.csv")
x.amzn = read.csv("amzn/x.csv")
y.amzn = read.csv("amzn/y.csv")
train = rbind(x.aapl, x.msft, x.tsla)
train$price_change = rbind(y.aapl, y.msft, y.tsla)$price_change
test = x.amzn
test$price_change = y.amzn$price_change
run.svm(train,test,FALSE,"linear")
run.svm(train,test,FALSE,"polynomial")
run.log(train,test)

# Initialize train and test based on ratios
sent.aapl = read.csv("aapl/sentiment.csv")
sent.msft = read.csv("msft/sentiment.csv")
sent.tsla = read.csv("tsla/sentiment.csv")
sent.amzn = read.csv("amzn/sentiment.csv")
train = rbind(sent.aapl, sent.msft, sent.tsla)
test = sent.amzn
train = trim(train)
test = trim(test)
run.svm(train,test,TRUE,"linear")
run.svm(train,test,TRUE,"polynomial")
run.log(train,test)


# initialize train and test based on aggregation
agg.aapl = read.csv("aapl/aggregated.csv")
agg.msft = read.csv("msft/aggregated.csv")
agg.tsla = read.csv("tsla/aggregated.csv")
agg.amzn = read.csv("amzn/aggregated.csv")
train = rbind(agg.aapl, agg.msft, agg.tsla)
test = agg.amzn
train = trim(train,TRUE)
dates = test$date
test = trim(test,TRUE)
run.svm(train,test,TRUE,"linear")
run.svm(train,test,TRUE,"polynomial")
run.log(train,test)
x = run(train,test,dates)

# 1 initializes train and test based on better aggregation
bet.aapl.1 = read.csv("aapl/better1.csv")
bet.msft.1 = read.csv("msft/better1.csv")
bet.tsla.1 = read.csv("tsla/better1.csv")
bet.amzn.1 = read.csv("amzn/better1.csv")
train = rbind(bet.aapl.1, bet.msft.1, bet.tsla.1)
test = bet.amzn.1
train = trim1(train,TRUE)
dates = test$date
test = trim1(test,TRUE)
run.svm(train,test,TRUE,"linear")
run.svm(train,test,TRUE,"polynomial")
run.log(train,test)
x1 = run(train,test,dates)

# 2 initializes train and test based on better aggregation
bet.aapl.2 = read.csv("aapl/better2.csv")
bet.msft.2 = read.csv("msft/better2.csv")
bet.tsla.2 = read.csv("tsla/better2.csv")
bet.amzn.2 = read.csv("amzn/better2.csv")
train = rbind(bet.aapl.2, bet.msft.2, bet.tsla.2)
test = bet.amzn.2
dates = test$date
train = trim2(train,TRUE)
test = trim2(test,TRUE)
run.svm(train,test,TRUE,"linear")
run.svm(train,test,TRUE,"polynomial")
run.log(train,test)
x2 = run(train,test,dates)
# Calculates SVM Classifier 
run.svm = function(train, test, scaled, kernel) {
  library(e1071)
  train$price_change = (train$price_change > 0)*2 - 1
  test$price_change = (test$price_change > 0)*2 - 1
  svm.fit = svm(price_change~., data = train, kernel = kernel, scale = scaled, type = "C-classification")
  preds = predict(svm.fit, test)
  print(mean(test$price_change != preds))
}


run = function(train, test,dates) {
  train$price_change = (train$price_change > 0)*1
  test$price_change = (test$price_change > 0)*1
  log.fit = glm(price_change~.,family = binomial, data = train)
  preds = predict(log.fit,test,type = "response")
  preds = (preds > .5)*1
  return(data.frame(dates,test$price_change,preds))
}


for (cost in c(.001,.01,.1,1,1,5,10)) {
  print(run.svm(train,test,TRUE,"linear",cost))
}


# Calculates Logistic Regression
run.log = function(train,test) {
  train$price_change = (train$price_change > 0)*1
  test$price_change = (test$price_change > 0)*1
  log.fit = glm(price_change~.,family = binomial, data = train)
  preds = predict(log.fit,test,type = "response")
  preds = (preds > .5)*1
  print(mean(test$price_change != preds))
}


# linear plot
par(mfrow=c(2,3))
plot(train$pos,train$price_change, ylab = "Price Change", xlab = "Positive Words")
plot(train$neg,train$price_change, ylab = "Price Change", xlab = "Negative Words")
plot(train$name_mentioned,train$price_change, ylab = "Price Change", xlab = "Company Mentions")
plot(train$pos_neighbors,train$price_change,ylab = "Price Change", xlab = "Pos near Company Mentions")
plot(train$neg_neighbors,train$price_change, ylab = "Price Change", xlab = "Neg near Company Mentions")



# PCA Class plot
library(ggplot2)
#for dictionary based
df = rbind(x.aapl, x.msft, x.tsla)
groups = (rbind(y.aapl, y.msft, y.tsla) > 0)*1
#for ratio based or aggregation based
df = train
df$price_change = NULL
groups = as.matrix((train$price_change>0)*1)
#always execute
pr.out = prcomp(df, scale = TRUE, center = TRUE)
scores = data.frame(groups, pr.out$x[,1:2])
qplot(x=PC1, y=PC2, data=scores, colour = factor(groups), main = "PCA Graph: Sentiment Word Dictionary")














