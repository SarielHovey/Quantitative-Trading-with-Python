#          ### Get Data from Yahoo! Finance via 'Quantmod' ###
library('quantmod')

# Get GLD & GDX data from 2017-06-18
getSymbols(c("GLD"), from = '2017-06-18')
getSymbols(c("GDX"), from = '2017-06-18')
# Data in 'xts' format






#	 ### Get Data from Quantdl ###
install.packages("Quandl")
library(Quandl)
Quandl.api_key('Quandl_API_Key')

# Example API Request for csv
# GET "https://www.quandl.com/api/v3/datasets/WIKI/FB/data.csv?api_key=YOURAPIKEY"
# curl "https://www.quandl.com/api/v3/datasets/WIKI/FB.csv?column_index=4&start_date=2014-01-01&end_date=2014-12-31&collapse=monthly&transform=rdiff&api_key=YOURAPIKEY
# Details for this on 'https://docs.quandl.com/docs/in-depth-usage'







			             ### Load Data via package 'data.table' ###
setwd('WhereYouPutYourData')
library('data.table')
S <- sub('.csv', '', list.files())		

# Use data.table::fread(), sort DATA in date-ascending order
DATA <- list()
for (i in S) {
		suppressWarnings(
		    DATA[[i]] <- fread(paste0(i, '.csv'), sep=','))
		DATA[[i]] <- (DATA[[i]])[order(DATA[[i]][["Date"]], decreasing = FALSE)]
		 }

				      ### Organize Data as Date-uniform for 'zoo'###
# Codes from 'Automated Trading with R: Quantitative Research and Platform Development'

library('zoo')
# Compute the date template as a column of a data.frame for merging                  
# Considers date are strings in YYYY-MM-DD format                  
datetemp <- sort(unique(unlist(sapply(DATA, function(v) v[["Date"]]))))
datetemp <- data.frame(datetemp, stringsAsFactors = FALSE)
names(datetemp) <- "Date"

# Double-check that our data is unique and in ascending-date order                  
DATA <- lapply(DATA, function(v) unique(v[order(v$Date),]))

# Create 6 new objects that will hold our re-organized data                  
DATA[["Open"]] <- DATA[["High"]] <- DATA[["Low"]] <-
  DATA[["Close"]] <- DATA[["Adj Close"]] <- DATA[["Volume"]] <- datetemp

# This loop will sequentially append the columns of each symbol                  
# to the appropriate Open, High, Low, etc. object                  
for(s in S){
  for(i in rev(c("Open", "High", "Low", "Close", "Adj Close", "Volume"))){
    temp <- data.frame(cbind(DATA[[s]][["Date"]], DATA[[s]][[i]]),
                        stringsAsFactors = FALSE)
    names(temp) <- c("Date", s)
    temp[,2] <- as.numeric(temp[,2])

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

  # Update user on progress            
  if( which( S == s ) %% 25 == 0 ){
    cat( paste0(round(100 * which( S == s ) / length(S), 1), "% Complete\n") )
  }

}

# Declare them as zoo objects for use with time-series functions                  
DATA <- lapply(DATA, function(v) zoo(v[,2:ncol(v)], strptime(v[,1], "%Y-%m-%d")))
# Remove extra variables                  
rm(list = setdiff(ls(), c("DATA", "datadir", "functiondir", "rootdir")))
