# Read in data
args = commandArgs(trailingOnly=TRUE)
#df = read.csv(args[2])
df = read.csv("sample.csv")

# Set up a panel of 2 charts: histogram and density plot of
# interamount times.
par(mfrow=c(1,2))
hist(df$interamountTime, 
     main="Histogram of inter-event times", 
     xlab="Inter-event time",
     freq=TRUE)
plot(density(df$interamountTime),
     main="Density function of inter-event times")

# Burstiness is defined as ...
burstiness = (sd(df$interamountTime)-mean(df$interamountTime))/(sd(df$interamountTime)+mean(df$interamountTime))
print(paste("Burstiness coefficient: ",burstiness))

times = df$interamountTime
m_1 = mean(times[1:length(df$times)-1])
sd_1 = sd(times[1:length(df$times)-1])
m_2 = mean(times[2:length(df$times)])
sd_2 = sd(times[2:length(df$times)])

# Memory is defined as ...
# (TODO: vectorize this, for loops are slow in R)
summation = 0
for (i in 1:(length(times)-1)) 
{
    k = ((times[i]-m_1)*(times[i+1]-m_2))/(sd_1*sd_2)
    summation = summation + k
}
memory = summation/(length(times)-1)
print(paste("Memory coefficient: ", memory))

