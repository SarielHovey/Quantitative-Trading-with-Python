# Code from 'Chris Conlan, Automated Trading with R, 10.1007/978-1-4842-2178-5_5'
# Set 'exampleset' from list of S&P500
exampleset <- c("AAPL", "GOOGL", "YHOO", "HP", "KORS", "COH", "TIF")


#                               ### Simple Mean Average ###
n <- 20
# An example for SMA(20)
meanseries <- rollapply(DATA[["Close"]][,exampleset],
          width = n,
          FUN = mean,
          by.column = TRUE,
          fill = NA,
          align = "right"
)



#                               ### Moving Average Convergence Divergence Osillator (MACD) ###
n1 <- 5
n2 <- 34
# An example for MACD(5, 34)
# Formular: $MACD_{t,n_1,n_2} = SMA_{t,n_1} - SMA_{t,n_2}$, and $n_1 < n_2$
MACDseries <-
rollapply(DATA[["Close"]][,exampleset],
 # 'rollapply' to columns in 'exampleset' in DATA[['Close']]
         width = n2,
         FUN = function(v) mean(v[(n2 - n1 + 1):n2]) - mean(v),
         by.column = TRUE,
         fill = NA,
         align = "right"
)



#                               ### Bollinger Bands (BOLL)###
# Formular: $Middle_{t,n} = SMA_{t,n}$
# Formular: $Upper_{t,n} = Middle_{t,n} + 2\sigma_{t,n}$
# Formular: $Middle_{t,n} = Middle_{t,n} - 2\sigma_{t,n}$
# Formular: $\sigma_{t,n}^2 = \prep{\Sigma_{i=0}^{n-2}(y_{t-i} - SMA_{t,n-1})^2}{n-1}$
n <- 20
# 'rollsd' is 20-day Sample Std, $\sigma_{t,n}$
rollsd <- rollapply(DATA[["Close"]][,exampleset],
         width = n,
         FUN = sd,
         by.column = TRUE,
         fill = NA,
         align = "right"
)

upperseries <- meanseries + 2 * rollsd
lowerseries <- meanseries + 2 * rollsd



#                               ###Chaikin Money Flow (CMF)###
# Formular: Money Flow Volumn(MFV): $MFV_t = \prep{2y_t - h_t - l_t}{h_t - l_t} V_t$
# Formular: $CMF_{t,n} = \prep{\Sigma_{i=0}^{n-1}MFV_{t-i}}{\Sigma_{i=0}^{n-1} v_{t-i}$
CMFfunc <- function(close, high, low, volume){
  apply(((2 * close - high - low) / (high - low)) * volume,
        MARGIN = 2,
        # 'Margin = 2' sets the 'apply' for columns in List
        FUN = sum) /
  apply(volume,
        MARGIN = 2,
        FUN = sum)
}

n <- 20
k <- length(exampleset)
CMFseries <- rollapply(cbind(DATA[["Close"]][,exampleset],
                 DATA[["High"]][,exampleset],
                 DATA[["Low"]][,exampleset],
                 DATA[["Volume"]][,exampleset]),
                 # Copy Close, High, Low, Volume from left to right, k columns each
          FUN = function(v) CMFfunc(v[,(1:k)],
                                    v[,(k+1):(2*k)],
                                    v[,(2*k + 1):(3*k)],
                                    v[,(3*k + 1):(4*k)]),
          by.column = FALSE,
          width = n,
          fill = NA,
          align = "right"
)
names(CMFseries) <- exampleset



