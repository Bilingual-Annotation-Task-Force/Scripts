# Density Plot for Interspeech Paper
library("dplyr")
library("gtools")

setwd("/Users/wallyguzman/Documents/BATs/Spans")

BCBC_raw <- read.table("BCBC_Spans.txt", sep="\t", header = T)
YYB_raw <- read.table("YYB_Spans.txt", sep="\t", header = T)
KC_raw <- read.table("KC_Spans_2.txt", sep="\t", header = T)
SpinTX_raw <- read.table("SpinTX_Spans.txt", sep="\t", header = T)
S7_raw <- read.table("S7_Spans.txt", sep="\t", header = T)

# Combine language span counts
BCBC_raw <- BCBC_raw %>% group_by(`SpanLength`) %>% summarize(Sum = sum(`SpanFreq`))
YYB_raw <- YYB_raw %>% group_by(`SpanLength`) %>% summarize(Sum = sum(`SpanFreq`))
KC_raw <- KC_raw %>% group_by(`SpanLength`) %>% summarize(Sum = sum(`SpanFreq`))
SpinTX_raw <- SpinTX_raw %>% group_by(`SpanLength`) %>% summarize(Sum = sum(`SpanFreq`))
S7_raw <- S7_raw %>% group_by(`SpanLength`) %>% summarize(Sum = sum(`SpanFreq`))

# Repeat span counts
BCBC_raw <- data.frame(with(BCBC_raw, rep(`SpanLength`, times = Sum)))
YYB_raw <- data.frame(with(YYB_raw, rep(`SpanLength`, times = Sum)))
KC_raw <- data.frame(with(KC_raw, rep(`SpanLength`, times = Sum)))
SpinTX_raw <- data.frame(with(SpinTX_raw, rep(`SpanLength`, times = Sum)))
S7_raw <- data.frame(with(S7_raw, rep(`SpanLength`, times = Sum)))

BCBC_raw$Dataset <- "BCBC"
YYB_raw$Dataset <- "YYB"
KC_raw$Dataset <- "KC"
SpinTX_raw$Dataset <- "SpinTX"
S7_raw$Dataset <- "S7"

# Rename Columns
colnames(BCBC_raw)[1] <- "SpanFreq"
colnames(YYB_raw)[1] <- "SpanFreq"
colnames(KC_raw)[1] <- "SpanFreq"
colnames(SpinTX_raw)[1] <- "SpanFreq"
colnames(S7_raw)[1] <- "SpanFreq"

# Density plot
BCBC_density <- density(BCBC_raw$SpanFreq, from=-1, to=20)
YYB_density <- density(YYB_raw$SpanFreq, from=-1, to=20)
KC_density <- density(KC_raw$SpanFreq, from=-1, to=20)
SpinTX_density <- density(SpinTX_raw$SpanFreq, from=-1, to=20)
S7_density <- density(S7_raw$SpanFreq, from=-1, to=20)

plot(KC_density, col="blue", lwd=c(2.5,2.5), main="", xlab="Spans Between Switch Points")
lines(BCBC_density, col="green", lwd=c(2.5,2.5))
lines(YYB_density, col="red", lwd=c(2.5,2.5))
lines(SpinTX_density, col="orange", lwd=c(2.5,2.5))
lines(S7_density, col="cyan", lwd=c(2.5,2.5))

legend(15,0.24, lty=c(1, 1), lwd=c(2.5,2.5), c("KC", "BCBC", "YYB", "SpinTX", "S7"), col=c("blue", "green", "red", "orange", "cyan"))

