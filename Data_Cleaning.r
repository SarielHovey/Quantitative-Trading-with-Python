### Eliminating Pre-S&P Data ###
# Codes from 'Automated Trading with R: Quantitative Research and Platform Development'
# Remember to renew the list for S&P 500 to latest in the same format

if ( "SPdates.R" %in% list.files() ) {source("SPdates.R")} else {
+     url <- "http://trading.chrisconlan.com/SPdates.csv" 
+     S <- read.csv(url, header = FALSE, stringsAsFactors = FALSE) 
+     dump(list = "S", "SPdates.R")}

head(S)
#    V1         V2
#1    A   6/2/2000	#Date in format '%m/%d/%Y'
#2  AAL  3/23/2015
#3  AAP   7/9/2015
#4 AAPL 11/30/1982
#5 ABBV 12/31/2012
#6  ABC  8/29/2001

### Use DATA from 'Date Preparation'
names(S) <- c("Symbol", "Date")
S$Date <- strptime(S$Date, "%m/%d/%Y")
for(s in names(DATA[["Close"]])){
  for(i in c("Open", "High", "Low", "Close", "Adj Close", "Volume")){
+   Sindex <- which(S[,1] == s)
+   if(S[Sindex, "Date"] != "1900-01-01 EST" &
+      S[Sindex, "Date"] >= "2000-01-01 EST"){
+         DATA[[i]][index(DATA[[i]]) <= S[Sindex, "Date"], s] <- NA
+      }
+ }}
# Date in 'S' is the date for a symbel to be added to S&P500
# Set Pre-S&P500 data to be 'NA'

#					### Deal with Global Holidays ###
# For globally diversified portfolios, stocks may have different transaction days
# Hypothesis: Missing data for 'KORS' on 2015-11-26, 2015-11-28, 2015-11-29
temp <- c(DATA[["Close"]][index(DATA[["Close"]]) %in% c("2015-11-23",
                                                        "2015-11-24",
                                                        "2015-11-25"), "KORS"],
+        zoo(NA, order.by = strptime("2015-11-26", "%Y-%m-%d")) ,
+        DATA[["Close"]][index(DATA[["Close"]]) %in% c("2015-11-27"), "KORS"],
+        zoo(NA, order.by = strptime(c("2015-11-28", "2015-11-29"), "%Y-%m-%d")),
+        DATA[["Close"]][index(DATA[["Close"]]) %in% c("2015-11-30",
+                                                       "2015-12-01",
+                                                       "2015-12-02"), "KORS"])
# Missing data are set to 'NA'

# Caution: Smoothing method below will place downward bias on Volatility
# Caution: Variance Metrics are used in Indicators and Performance metrics
# e.g. Indicators like Bollinger Bands and Rolling SR

#	# Forward Replacement--Replace 'NA' with the most previous non-NA value
forwardfun <- function(v, n) {
+ if(is.na(v[n])){
+   return(v[max(which(!is.na(v)))])
+ } else {
+   return(v[n])
+ }
+}

maxconsec <- 3
# Caution: 'maxconsec' = (max consecutive NA number +1)

# We pass maxconsec to rollapply() in "width = "                    
# and pass it again to forwardfun() in "n = "                    
forwardrep <- rollapply(temp,
+          width = maxconsec,
+          FUN = forwardfun,
+          n = maxconsec,
+          by.column = TRUE,
+          align = "right")



#	# Linearly Smoothed Replacement Function                    
linearfun <- function(v, n){
+ m <- (n + 1)/2
+ if(is.na(v[m])){
+   a <- max(which(!is.na(v) & seq(1:n) < m))
+   b <- min(which(!is.na(v) & seq(1:n) > m))
+   return(((b - m)/(b - a)) * v[a] +
+           ((m - a)/(b - a)) * v[b])
+ } else {
+   return(v[m])
+ }}

maxconsec <- 5
# Caution: 'maxconsec' >= (max consecutive NA number +2) & (is odd)

linearrep <- rollapply(temp,
+         width = maxconsec,
+         FUN = linearfun,
+         n = maxconsec,
+         by.column = TRUE,
+	  align = "center")



#	# Volume-Weighted Smoothed Replacement Function  
voltemp <- c(DATA[["Volume"]][index(DATA[["Close"]]) %in% c(index(temp)[1:3]), "KORS"],
+     zoo(NA, order.by = index(temp)[4]),
+     DATA[["Volume"]][index(DATA[["Close"]]) %in% c(index(temp)[5]), "KORS"],
+     zoo(NA, order.by = index(temp)[6:7]),
+     DATA[["Volume"]][index(DATA[["Close"]]) %in% c(index(temp[8:10])), "KORS"])
                  
volfun <- function(v, n, vol){
+ m <- (n + 1)/2
+ if(is.na(v[m])){
+   a <- max(which(!is.na(v) & seq(1:n) < m))
+   b <- min(which(!is.na(v) & seq(1:n) > m))
+   return(((v[a] + ((m-a-1)/(b-a)) * (v[b] - v[a])) * vol[a] +
+           (v[a] + ((m-a+1)/(b-a)) * (v[b] - v[a])) * vol[b]) /
+             (vol[a] + vol[b]))
+ } else {
+   return(v[m])
+ }
+}

maxconsec <- 5
# Caution: 'maxconsec' >= (max consecutive NA number +2) & (is odd)

volrep <- rollapply(cbind(temp, voltemp),
+         width = maxconsec,
+         FUN = function(v) volfun(v[,1], n = maxconsec, v[,2]),
+         by.column = FALSE,
+         align = "center")



					
#					### Adjust for Dividents & Splits ###
# Declare new zoo data frame of adjustment factors                    
MULT <- DATA[["Adj Close"]] / DATA[["Close"]]

# Store Close and Open Prices in new variable "Price" and "OpenPrice"                    
DATA[["Price"]] <- DATA[["Close"]]
# DATA[['Price']] is Unadjusted Close
DATA[["OpenPrice"]] <- DATA[["Open"]]
# DATA[['OpenPrice']] is Unadjusted Open
# Unadjusted Close & Unadjusted Open are saved for Order Execution, Account Management, Performance Assessment

# Adjust Open, High, and Low                    
DATA[["Open"]] <- DATA[["Open"]] * MULT
DATA[["High"]] <- DATA[["High"]] * MULT
DATA[["Low"]] <- DATA[["Low"]] * MULT
# Copy Adjusted Close to Close                    
DATA[["Close"]] <- DATA[["Adj Close"]]
# Get Adjusted Open, Adjusted High, Adjusted Low, Adjusted Close
                 
DATA[["Adj Close"]] <- NULL


#					### Inactive Symbols -- by Forward Replacement ###
# Inactive Symbol usually caused by Merger & Acquisition, then Value for 'Close' is 'NA' AFTERWARDS
for( s in names(DATA[["Close"]]) ){
+ if(is.na(DATA[["Close"]][nrow(DATA[["Close"]]), s])){
# 'maxInd' is the Place that all Value = NA afterwards
+   maxInd <- max(which(!is.na(DATA[["Close"]][,s])))
# Change Adjusted CLose,Open,High,Low after 'maxInd' to the last valid Adjusted Close
+   for( i in c("Close", "Open", "High", "Low")){
+    DATA[[i]][(maxInd+1):nrow(DATA[["Close"]]),s] <- DATA[["Close"]][maxInd,s]
+   }
# Change UnAdjusted Close,Open after 'maxInd' to the last valid UnAdjusted Close
+   for( i in c("Price", "OpenPrice") ){
+     DATA[[i]][(maxInd+1):nrow(DATA[["Close"]]),s] <- DATA[["Price"]][maxInd,s]
+   }
# Change Volume after 'maxInd' to 0 (No more transactions, of course)
+   DATA[["Volume"]][(maxInd+1):nrow(DATA[["Close"]]),s] <- 0
+ }
+}


#					### Compute Return Matrix ###
# Pad with NAs to preserve dimension equality
# Initialize a Matrix for all Instruments in DATA and order by Date increaseingly
NAPAD <- zoo(matrix(NA, nrow = 1, ncol = ncol(DATA[["Close"]])),
+            order.by = index(DATA[["Close"]])[1])
names(NAPAD) <- names(DATA[["Close"]])

# Compute Daily (Close-to-Close Returns)
# Use Adjusted Close          
RETURN <- rbind( NAPAD, ( DATA[["Close"]] / lag(DATA[["Close"]], k = -1) ) - 1 )

# Compute Overnight Returns (Close-to-Open)
# Use Adjusted Open & Adjusted Close            
OVERNIGHT <- rbind( NAPAD, ( DATA[["Open"]] / lag(DATA[["Close"]], k = -1) ) - 1 )



