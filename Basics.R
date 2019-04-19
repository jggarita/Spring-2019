rm(list = ls())
setwd("/Users/jggarita/Spring-2019")

loadhou = read.csv('/Users/jggarita/Spring-2019/ECO395M/data/loadhou.csv')

library("dplyr")
# plot the data
ggplot(data = loadhou) + 
  geom_point(mapping = aes(x = KHOU, y = COAST), color='darkgrey') + 
  ylim(7000, 20000)

# Make a train-test split
N = nrow(loadhou)
N_train = floor(0.8*N) 
N_test = N - N_train


#####
# Train/test split
#####

# randomly sample a set of data points to include in the training set
train_ind = sample.int(N, N_train, replace=FALSE)

# Define the training and testing set
D_train = loadhou[train_ind,]
D_test = loadhou[-train_ind,]

# optional book-keeping step:
# reorder the rows of the testing set by the KHOU (temperature) variable
# this isn't necessary, but it will allow us to make a pretty plot later
D_test = arrange(D_test, KHOU)
head(D_test)


