#Download Data from 'Yahoo! Finance' for 'IGE' and 'SPY'.

#Import Data into R as 'IGE'

                                           ##  Calculate Sharpe Ratio ##

IGE$DailyRet <- repeat(NA, length(IGE$Date))
# This time the length is 1504, use 1504 in below for 'length(IGE$Date)'

length(IGE$Date)
# [1] 1504


IGE$DailyRet <- rep(NA, 1504)

for (i in 2:length(IGE$Adj.Close)) {IGE$DailyRet[i] <- (IGE$Adj.Close[i]-IGE$Adj.Close[i - 1])/IGE$Adj.Close[i-1]}
# 'Adj.Close' is the daily stock close price adjusted for Dividents and splits

IGE$EXDailyRet <- rep(NA, 1504)

IGE$EXDailyRet <- IGE$DailyRet - 0.04/252
# Assume 0.04 to be the yearly risk-free return during the period

IGE$SR <- sqrt(252) * mean(IGE$EXDailyRet, na.rm = TRUE) / sd(IGE$DailyRet, na.rm = TRUE)

                                   ## Calculate Drawdown and Max.Drawdown.Duration ##

IGE$DailyRetSPY <- rep(NA, 1504)
# Daily Return for 'SPY'

for (i in 2:1504) {IGE$DailyRetSPY[i] <- (AdjCloseSPY[i]-AdjCloseSPY[i-1])/AdjCloseSPY[i-1]}

IGE$EXDR.SPY <- IGE$DailyRetSPY - 0.04/252
# Again, assuem yearly risk-free return to be 0.04

IGE$CumRet <- rep(NA, 1504)

IGE$NetDR <- (IGE$DailyRetSPY - IGE$DailyRet) /(-2)
# In this example, we Long 'IGE' and Short 'SPY'. So for Net Return, we have 2 times the principle.

IGE$CumRet[1:2] <- IGE$NetDR[1:2]

for (i in 3:1504) {IGE$CumRet[i] <- (1+IGE$CumRet[i-1])*(1+IGE$NetDR[i])-1}
# 'CumRet' is the Cumlumative Return for this portfolio

IGE$HWaterMk <- rep(NA, 1504)
# 'HWaterMk' stands for High Water Mark

for (i in 2:1504) {IGE$HWaterMk[i] <- max(c(IGE$CumRet[i],IGE$HWaterMk[i-1]), na.rm = TRUE)}

IGE$DW <- rep(NA, 1504)
# 'DW' stands for Drawdown

for (i in 2:1504) {IGE$DW[i] <- ((1+IGE$CumRet[i])/(1+IGE$HWaterMk[i]))-1}

IGE$MaxDW.Dur <- rep(0, 1504)

for (i in 2:1504) {if (IGE$DW[i]==0) {IGE$MaxDW.Dur[i]<- 0} else {IGE$MaxDW.Dur[i] <- IGE$MaxDW.Dur[i-1] + 1} }

max(IGE$MaxDW.Dur)
# [1] 497
# This is the max Drawdown, 497 days.

                                      ### Build a Function in R for Max Drawdown ###
MD <- function(curve, n = 1){

time <- length(curve)
  v <- rep(NA, (time * (time - 1)) / 2)  # vector v is used to store all $curve[i] - curve[i-1]$
  k <- 1
  for(i in 1:(length(curve)-1)){
    for(j in (i+1):length(curve)){
      v[k] <- curve[i] - curve[j]
      k <- k + 1
    }
  }
  m <- rep(NA, length(n))
  for(i in 1:n){
    m[i] <- max(v)
    v[which.max(v)] <- -Inf  # Set previous max(v) to negative Inf, then get the next max(v)
  }
  return(m)
  
}


                                  ### Calculate NPMD and Burke Ratio ###
NPMD <- (Et[length(Et)] - Vt[1]) / MD(Et)  # NPMD stands for 'Net Profit to Max Drawdown Ratio'. 
# Et is Equity Curve, Vt is invested capital

Burke <- (Et[length(Et)] - Vt[1]) / sqrt((1/length(Et)) * sum(MD(Et, n = round(length(Et) / 20))^2))
# This is High Frequency Burke Ratio, set T=20

 
                                  ### Build a Function for Partial Moment ###
PM <- function(Rt, upper = FALSE, n = 2, Rb = 0){  # Rb is Benchmark Return, Rt is Return at time t. Default is LPM(n=2, Rb=0)
  if(n != 0){
    if(!upper) return(mean(pmax(Rb - Rt, 0, na.rm = TRUE)^n))
    if(upper) return(mean(pmax(Rt - Rb, 0, na.rm = TRUE)^n))
  } else {
    if(!upper) return(mean(Rb >= Rt))   # Probability Rb >= Rt for LPM
    if(upper) return(mean(Rt > Rb))     # Probability Rt > Rb for HPM
  }
}

LPM <- PM(Rt, n=2, Rb=0)    # Lower Partial Moment
HPM <- PM(Rt, upper=TRUE, n=2, Rb=0)    # Higher Partial Moment
# n = 1, PM is Mean of Partial Moment
# n = 2, PM is Upper or Lower Partial Semivariance for mean Rb
# n = 3, PM is Upper or Lower Partial Semiskewness for mean Rb

Omega <- mean(Rt, na.rm = TRUE) / PM(Rt)^0.5    # Generalized Omega, assuming Rb=0, n=2
UPR <- PM(Rt, upper = TRUE)^0.5 / PM(Rt)^0.5    # Upside Potential Ratio, assuming Rb=0, n=2

                                ### Calculate Jensen's Alpha with OLS ###
model <- lm(Rt ∼ Rb)    # Intercept as $\alpha$; b1 as $\beta$. $R_t = \alpha + \beta R_{t,b} + \epsilon_{i}$

                                ### Calculate Pure Profit Score ###
# $PPS = $\prep{E_T0 -V_0}{V_0} R^2$
# $\prep{E_t0}{V_t} = \alpha + \beta t + \epsilon_{i}$    #Get R Squared from the regression
y <- Et/Vt
ls1 <- lm(y ∼ t)                   
PPS <- ((Et[length(Et)] - Vt[1]) / Vt[1]) * summary(ls1)$r.squared


