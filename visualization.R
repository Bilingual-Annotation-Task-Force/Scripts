library(ggplot2)
library(reshape2)

#Span Plot
#x-axis: token
#y-axis: corresponding language tag
text <- c("Anyway,", "al", "taxista", "right", "away", "le", "noté", "un", "acentito,", "not", "too", "specific.")
language <- c("Eng", "Spn", "Spn", "Eng", "Eng", "Spn", "Spn", "Spn", "Spn", "Eng", "Eng", "Eng")
mydata1 <- data.frame(text, language)   #data frame needs to be in this format: token | tag
ggplot(data = mydata1, 
       aes(x = factor(text, levels = text), 
           y = factor(language), group = 1)) + 
  geom_line() + 
  geom_point() +
  xlab("Text") +            #change x-axis title
  ylab("Language") +        #change y-axis title
  theme(panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(),
        panel.background = element_blank(), 
        panel.border = element_rect(fill = NA, 
                                    colour = "black")) +
  theme(axis.ticks.length = unit(-0.15, "cm"), 
        axis.text.x = element_text(margin = margin(10,10,10,5,"pt")),
        axis.text.y = element_text(margin = margin(10,10,10,5,"pt")),
        axis.text=element_text(size=11, colour = "black"),
        axis.title=element_text(size=14,face="bold"))

#Span Distribution
#x-axis: span length
#y-axis: span frequency
sspan <- factor(rpois(1000,4), ordered = TRUE)
espan <- factor(rpois(1000,4), ordered = TRUE)
mydata2 <- data.frame(sspan, espan)
freq <- table(col(mydata2), as.matrix(mydata2))
freq <- freq[,as.character(0:12)]
Names <- as.character(c(0:12))
data <- data.frame(t(cbind(freq)), Names) #data frame need to be in this format: 
data.m <- melt(data, id.vars = 'Names')   #span length | lang1's span frequency | lang2's span frequency

ggplot(data = data.m, 
       aes(x = Names, 
           y = value)) + 
  geom_bar(aes(fill = variable), 
           stat = "identity", 
           position = "dodge",
           color = "black") +
  scale_fill_manual(values = c("black", "white"),
                    breaks=c("X1", "X2"),
                    labels=c("English", "Spanish")) +  #change legend level
  theme(legend.position = c(0.9,0.7),
        legend.background = element_rect(colour ="black"),
        legend.title=element_blank()) +
  theme(panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(),
        panel.background = element_blank(), 
        panel.border = element_rect(fill = NA, 
                                    colour = "black")) +
  theme(axis.ticks.x = element_blank(),
        axis.ticks.length = unit(-0.15, "cm"), 
        axis.text.x = element_text(margin = margin(10,1,1,1,"pt")),
        axis.text.y = element_text(margin = margin(1,5,1,1,"pt")),
        axis.text=element_text(size=11, colour = "black"),
        axis.title=element_text(size=14,face="bold")) +
  xlab("Span Length") +       #change x-axis title
  ylab("Span Frequency")      #change y-axis title


