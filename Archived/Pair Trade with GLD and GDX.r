# Download data for GLD and GDX from 'Yahoo! Finance' from date 2017-06-15 to 2019-06-16
# Import data into R

GDX$Date <- as.Date(GDX$Date)
GLD$Date <- as.Date(GLD$Date)

Trainset <- data.frame(Date = GDX$Date[1:252], GDX = GDX$Adj.Close[1:252], GLD = GLD$Adj.Close[1:252])
Testset <- data.frame(Date = GDX$Date[253:504], GDX = GDX$Adj.Close[253:504], GLD = GLD$Adj.Close[253:504])
# Divide half of the samples into Trainset

HedgeRatio <- lm(Trainset$GLD ~ Trainset$GDX)    #Hedge GDX against GLD for pair trade
HedgeRatio

#Call:
#lm(formula = Trainset$GLD ~ Trainset$GDX)

#Coefficients:
 #(Intercept)  Trainset$GDX  
     # 83.906         1.742  

Trainset$HRto <- HedgeRatio$coefficients[2]

Trainset$Spread <- Trainset$GLD - Trainset$HRto * Trainset$GDX
Testset$Spread <- Testset$GLD - Trainset$HRto * Testset$GDX

Trainset$MeanSPD <- mean(Trainset$Spread)
Trainset$StdSPD <- sd(Trainset$Spread)

Trainset$Zscore <- (Trainset$Spread - Trainset$MeanSPD) / Trainset$StdSPD
# If Zscore <= -2 then Long spread; If Zscore >= 2 then Short spread; If abs(Zscore) <= 1 then Exit
Trainset$Position <- rep(NA, 252)
# Initialize Position

for (i in 1:252) {if (Trainset$Zscore[i] <= -2) {Trainset$Position[i] <- 'Long'}}
for (i in 1:252) {if (Trainset$Zscore[i] >= 2) {Trainset$Position[i] <- 'Short'}}
for (i in 1:252) {if (abs(Trainset$Zscore[i]) <= 1) {Trainset$Position[i] <- 'Exit'}}
for (i in 1:252) {if (abs(Trainset$Zscore[i]) > 1 & abs(Trainset$Zscore[i]) < 2) {Trainset$Position[i] <- 'Hold'}}

P.GLD <- rep(NA, 252)
P.GDX <- rep(NA, 252)
for (i in 1:252) {if (Trainset$Position[i] == 'Exit') {P.GLD[i] <- 0}}
for (i in 1:252) {if (Trainset$Position[i] == 'Exit') {P.GDX[i] <- 0}}
for (i in 1:252) {if (Trainset$Position[i] == 'Long') {P.GLD[i] <- 1}}
for (i in 1:252) {if (Trainset$Position[i] == 'Long') {P.GDX[i] <- -1}}
for (i in 1:252) {if (Trainset$Position[i] == 'Short') {P.GLD[i] <- -1}}
for (i in 1:252) {if (Trainset$Position[i] == 'Short') {P.GDX[i] <- 1}}
for (i in 2:252) {if (Trainset$Position[i] == 'Hold') {P.GLD[i] <- P.GLD[i-1]}}
for (i in 2:252) {if (Trainset$Position[i] == 'Hold') {P.GDX[i] <- P.GDX[i-1]}}

# Assume Mean Reverting for Spread. When too small with Zscore <= -2, the spread tends to rise, with GLD rising and GDX decreasing

Posi <- data.frame(GLD=P.GLD, GDX=P.GDX)
