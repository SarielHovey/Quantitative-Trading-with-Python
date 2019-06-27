#                               ### Step 1: Data Preparation ###
exampleset <- c("AAPL", "AMD", "AMZN", "GOOG", "HP", "INTC", "IBM", "MSFT")
# Data from 2009-06-25 to 2019-06-24, sourced from Yahoo! Finance
setwd('D:/R_Quant/StockData')
library('data.table')
S <- sub('.csv', '', list.files())

DATA <- list()

for (i in S) {
		suppressWarnings(
		    DATA[[i]] <- fread(paste0(i, '.csv'), sep=','))
		DATA[[i]] <- (DATA[[i]])[order(DATA[[i]][["Date"]], decreasing = FALSE)]
		 }
# Import data from downloaded csvs to DATA
# DATA is a list, consist of 8 data.table object as elements
# DATA has 7 columns as 'Date', 'Open', etc.

library('zoo')
datetemp <- sort(unique(unlist(sapply(DATA, function(v) v[["Date"]]))))
datetemp <- unique(datetemp)
# datetemp is a vector with unique elements now, rising by date

datetemp <- data.frame(datetemp, stringsAsFactors = FALSE)
names(datetemp) <- "Date"

DATA <- lapply(DATA, function(v) unique(v[order(v$Date),]))
# Sort DATA, rising by date

DATA[["Open"]] <- DATA[["High"]] <- DATA[["Low"]] <-
  DATA[["Close"]] <- DATA[["Adj Close"]] <- DATA[["Volume"]] <- datetemp
# Add 6 data.frame as elements to DATA

for(s in S){
  for(i in rev(c("Open", "High", "Low", "Close", "Adj Close", "Volume"))){
    temp <- data.frame(cbind(DATA[[s]][["Date"]], DATA[[s]][[i]]),
                        stringsAsFactors = FALSE)
    names(temp) <- c("Date", s)
    temp[,2] <- as.numeric(temp[,2])
    # temp[,2] is used as medium to transfer values into DATA[[i]]

    if(!any(!DATA[[i]][["Date"]][(nrow(DATA[[i]]) - nrow(temp)+1):nrow(DATA[[i]])]
            == temp[,1])){
      temp <- rbind(t(matrix(nrow = 2, ncol = nrow(DATA[[i]]) - nrow(temp),
                              dimnames = list(names(temp)))), temp)
      DATA[[i]] <- cbind(DATA[[i]], temp[,2])
    } else {
      DATA[[i]] <- merge(DATA[[i]], temp, all.x = TRUE, by = "Date")
    }

    names(DATA[[i]]) <- c(names(DATA[[i]])[-(ncol(DATA[[i]]))], s)
  }
  DATA[[s]] <- NULL
}
# Data[['Volume']] ~ Data[['Open']] now have corresponding data for each date for each s in S
# elements %in% S in list DATA has been removed
# Caution: if not remove DATA[[S]], then 'strptime' will error

head(DATA[['Close']])
#        Date     AAPL  AMD  AMZN     GOOG    HP    IBM  INTC  MSFT
#1 2009-06-24 19.46000 3.66 79.27 203.3226 29.85 104.15 16.10 23.47
#2 2009-06-25 19.98000 3.64 82.20 206.5416 31.31 106.06 16.31 23.79
#3 2009-06-26 20.34857 3.62 83.88 211.2858 31.53 105.68 16.29 23.35
#4 2009-06-29 20.28143 3.72 83.03 210.6996 31.35 105.83 16.38 23.86
#5 2009-06-30 20.34714 3.87 83.66 209.4328 30.87 104.42 16.55 23.77
#6 2009-07-01 20.40429 3.91 81.60 208.1412 30.61 104.84 17.04 24.04

DATA <- lapply(DATA, function(v) zoo(v[,2:ncol(v)], strptime(v[,1], "%Y-%m-%d")))
# change elements in DATA from data.frame to zoo object



#                               ### Step 2: Data Cleaning ###
# Test if NA included in DATA
anyNA(DATA)

# Use Forward Replacement for NA in DATA if exists
if anyNA(DATA) {

}

# Adjust for splits & dividents for ATS
MULT <- DATA[["Adj Close"]] / DATA[["Close"]]

# Save unadjusted Close&Open
DATA[["Price"]] <- DATA[["Close"]]
DATA[["OpenPrice"]] <- DATA[["Open"]]

DATA[["Open"]] <- DATA[["Open"]] * MULT
DATA[["High"]] <- DATA[["High"]] * MULT
DATA[["Low"]] <- DATA[["Low"]] * MULT
DATA[["Close"]] <- DATA[["Adj Close"]]
DATA[["Adj Close"]] <- NULL


# Compute Return Matrix
NAPAD <- zoo(matrix(NA, nrow = 1, ncol = ncol(DATA[["Close"]])),
            order.by = index(DATA[["Close"]])[1])

names(NAPAD) <- names(DATA[["Close"]])
NAPAD
#            AAPL AMD AMZN GOOG HP IBM INTC MSFT
#2009-06-24   NA  NA   NA   NA NA  NA   NA   NA

RETURN <- rbind(NAPAD, (DATA[['Close']] / lag(DATA[['Close']], k = -1) - 1) )
head(RETURN)
#                   AAPL          AMD         AMZN         GOOG           HP          IBM         INTC         MSFT
#2009-06-24           NA           NA           NA           NA           NA           NA           NA           NA
#2009-06-25  0.026721680 -0.005464481  0.036962282  0.015832255  0.048911188  0.018338886  0.013043182  0.013634210
#2009-06-26  0.018446884 -0.005494505  0.020437957  0.022969489  0.007026748 -0.003583094 -0.001226134 -0.018495271
#2009-06-29 -0.003299612  0.027624309 -0.010133501 -0.002774427 -0.005709052  0.001419780  0.005524546  0.021841889
#2009-06-30  0.003240166  0.040322581  0.007587679 -0.006012133 -0.015310926 -0.013323353  0.010378439 -0.003772332
#2009-07-01  0.002808629  0.010335917 -0.024623547 -0.006167184 -0.008422647  0.004022439  0.029607394  0.011358939

OVERRETURN <- rbind(NAPAD, (DATA[['Open']] / lag(DATA[['Close']], k = -1) - 1) )

# Set 6-core computation in R
library(doParallel)
workers <- 6
registerDoParallel( cores = workers )

