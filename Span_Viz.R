library(readr)

# Read in span data
S7_Spans <- read_delim("~/Documents/BATs/Switch Regression/Spans/S7_Spans.tsv", 
                       "\t", escape_double = FALSE, trim_ws = TRUE)
KC_Spans <- read_delim("~/Documents/BATs/Switch Regression/Spans/KC_ARIS_Spans.tsv",
                       "\t", escape_double = FALSE, trim_ws = TRUE)
M_Spans <- read_delim("~/Documents/BATs/Switch Regression/Miami_SpanData.tsv", 
                       "\t", escape_double = FALSE, trim_ws = TRUE)

# Drop tokens and keep span length and language
S7 <- S7_Spans[ -c(1) ]
KC <- KC_Spans[ -c(1) ]
M <- M_Spans[ -c(1, 4:6) ]

# Drop Num from KC
KC <- KC[KC$Language != "Num", ]

# Isolate Maria40 from Miami and remove corpus column
M40 <- M[M$Corpus == "maria40", ]
M40 <- M40[ -c(3) ]
M40 <- M40[1:(dim(M40)[1] - 1), ]

# Define reference language
ref <- "Eng"
langs = c("English", "Spanish")

# Isolate Eng vs Spn
KC_Eng <- KC[KC$Language == ref, ]
KC_Spn <- KC[KC$Language != ref, ]

S7_Eng <- S7[S7$Language == ref, ]
S7_Spn <- S7[S7$Language != ref, ]

M40_Eng <- M40[M40$Language == ref, ]
M40_Spn <- M40[M40$Language != ref, ]

# Comparison histograms
hist(KC_Eng$Length, xlim = c(0, 30), ylim = c(0, 250), breaks = 15, 
     main = "KC Eng Span Lengths", xlab = "Span Length")
hist(KC_Spn$Length, xlim = c(0, 30), ylim = c(0, 250), breaks = 15,
     main = "KC Spn Span Lengths", xlab = "Span Length")

hist(S7_Eng$Length, xlim = c(0, 80), ylim = c(0, 200), breaks = 50, 
     main = "S7 Eng Span Lengths", xlab = "Span Length")
hist(S7_Spn$Length, xlim = c(0, 80), ylim = c(0, 200), breaks = 12,
     main = "S7 Spn Span Lengths", xlab = "Span Length")

hist(M40_Eng$Length, xlim = c(0, 80), ylim = c(0, 300), breaks = 20, 
     main = "M40 Eng Span Lengths", xlab = "Span Length")
hist(M40_Spn$Length, xlim = c(0, 80), ylim = c(0, 300), breaks = 40,
     main = "M40 Spn Span Lengths", xlab = "Span Length")

# Find cutoff for maximum span length
max_span_length <- max(KC_Eng$Length, KC_Spn$Length)

# Combine both languages into one vector
kc_eng <- data.frame(table(factor(KC_Eng$Length, levels = 1:max_span_length)))
kc_spn <- data.frame(table(factor(KC_Spn$Length, levels = 1:max_span_length)))
kc_counts <- rbind(kc_eng[, 2], kc_spn[, 2])

s7_eng <- data.frame(table(factor(S7_Eng$Length, levels = 1:max_span_length)))
s7_spn <- data.frame(table(factor(S7_Spn$Length, levels = 1:max_span_length)))
s7_counts <- rbind(s7_eng[, 2], s7_spn[, 2])

m40_eng <- data.frame(table(factor(M40_Eng$Length, levels = 1:max_span_length)))
m40_spn <- data.frame(table(factor(M40_Spn$Length, levels = 1:max_span_length)))
m40_counts <- rbind(m40_eng[, 2], m40_spn[, 2])

# Plot side-by-side
barplot(kc_counts, beside = TRUE, names.arg = 1:max_span_length, xlab = "Span Length", 
        ylab = "Span Frequency", legend.text = langs, 
        main = "KC Span Distribution")

barplot(s7_counts, beside = TRUE, names.arg = 1:max_span_length, xlab = "Span Length", 
        ylab = "Span Frequency", legend.text = langs, 
        main = "S7 Span Distribution")

barplot(m40_counts, beside = TRUE, names.arg = 1:max_span_length, xlab = "Span Length", 
        ylab = "Span Frequency", legend.text = langs, 
        main = "M40 Span Distribution")


# Convert to single axis
KC$Length <- ifelse(KC$Language == ref, KC$Length, KC$Length * -1)
S7$Length <- ifelse(S7$Language == ref, S7$Length, S7$Length * -1)
M40$Length <- ifelse(M40$Language == ref, M40$Length, M40$Length * -1)

# Chronological plots
plot(KC$Length, type="h", col=factor(KC$Language), main = "KC Span Length by Span Index", 
     ylab = "Span Length", xlab = "Span Index")
legend(-30, 36, col = c("black", "red"), legend = c("English", "Spanish"), lty = c(1, 1))

plot(S7$Length, type="h", col=factor(S7$Language), main = "S7 Span Length by Span Index", 
     ylab = "Span Length", xlab = "Span Index")
legend(365, 330, col = c("black", "red"), legend = c("English", "Spanish"), lty = c(1, 1))

plot(M40$Length, type="h", col=factor(M40$Language), main = "M40 Span Length by Span Index", 
     ylab = "Span Length", xlab = "Span Index")
legend(560, -160, col = c("black", "red"), legend = c("English", "Spanish"), lty = c(1, 1))

# Violin Plots