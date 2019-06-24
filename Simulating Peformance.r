equNA <- function(v){
   o <- which(!is.na(v))[1]
   return(ifelse(is.na(o), length(v)+1, o))
}       # Return the Order Number of 1st non-NA value
# equNA dynamically enforced maxLookback on stocks that start their S&P tenure in the middle of OPEN and CLOSE

simulate <- function(OPEN, CLOSE,
                     ENTRY, EXIT, FAVOR,
                     maxLookback, maxAssets, startingCash,
                     slipFactor, spreadAdjust, flatCommission, perShareCommission,
                     verbose = FALSE, failThresh = 0,
                     initP = NULL, initp = NULL){
# Take minimal Input outside function to balance Speed and Flexibility

# Step 1
# Check ENTRY, EXIT, FAVOR matches DATA[['Close']]
# OPEN usually is DATA[['Open']]. This is the price we trade, as close price comes after market close
# CLOSE usually is DATA[['Close']]
# ENTRY is a zoo object with same dimensions as DATA[['Close']]
# ENTRY specifies stocks to enter. 0 means no action; 1 means long; -1 means short
# ENTRY triggered stocks will have $\prep{C}{K-k}$ dollars allocated to long or short
# ENTRY triggered stocks >= K then pick first K stocks based on FAVOR
if( any( dim(ENTRY) != dim(EXIT) ) |
    any( dim(EXIT) != dim(FAVOR) ) |
    any( dim(FAVOR) != dim(CLOSE) ) |
    any( dim(CLOSE) != dim(OPEN)) )
  stop( "Mismatching dimensions in ENTRY, EXIT, FAVOR, CLOSE, or OPEN.")
# Confirm equal dimension

# Exit is a zoo object with same dimensions as DATA[['Close']]
# Exit specifies stocks to exit. 0 means no action; 1 means exit a long; -1 means exit a short;
# Exit value of 999 corresponds to exiting any position
# Exit can be all 0 for strategies only require ENTRY and FAVOR
if( any( names(ENTRY) != names(EXIT)) |
  any( names(EXIT) != names(FAVOR) ) |
  any( names(FAVOR) != names(CLOSE) ) |
  any( names(CLOSE) != names(OPEN) ) |
  is.null(names(ENTRY)) | is.null(names(EXIT)) |
  is.null(names(FAVOR)) | is.null(names(CLOSE)) |
  is.null(names(OPEN)) )
  stop( "Mismatching or missing column names in ENTRY, EXIT, FAVOR, CLOSE, or OPEN.")
# Confirm same column name

# FAVOR is a zoo object with the same dimensions as DATA[['Close']]
# FAVOR specifies the favorability of a given stock at any given time
# FAVOR is required when ENTRY needs >=K stocks to enter; existing positions to exit th keep K
  ## A higher value of FAVOR indicates a desirable long position and an undesirable short position
  ## A lower or more negative value of FAVOR indicates a desirable short position or an undesirable long position
FAVOR <- zoo(t(apply(FAVOR, 1, function(v) ifelse(is.nan(v) | is.na(v), 0, v) )),
             order.by = index(CLOSE))
# Change NAN and NA in FAVOR to 0
# FAVOR could be defaulted to be Mean Return or Rolling SR

# Step 2
# K is the maximum number of asset held at given time
K <- maxAssets
k <- 0
C <- rep(startingCash, times = nrow(CLOSE))     # Cash Vector
S <- names(CLOSE)       # Equity Component in DATA

P <- p <- zoo( matrix(0, ncol=ncol(CLOSE), nrow=nrow(CLOSE)),
               order.by = index(CLOSE) )
# P -- share count matrix; p -- entry price matrix

# maxLookback is the greatest number of periods any indicator looks back in time plus one
# maxLookback is used to avoid matrices being processed when containing all NA values or incomplete computations due to na.rm=TRUE
if( !is.null( initP ) & !is.null( initp ) ){
  P[1:maxLookback,] <- matrix(initP, ncol=length(initP), nrow=maxLookback, byrow = TRUE)
  p[1:maxLookback,] <- matrix(initp, ncol=length(initp), nrow=maxLookback, byrow = TRUE)
}
names(P) <- names(p) <- S                                                
# initP and initp are used during cross validation to pass position and account information across strategy simulations

equity <- rep(NA, nrow(CLOSE))
# Equity Curve Vector

rmNA <- pmax(unlist(lapply(FAVOR, equNA)),
     unlist(lapply(ENTRY, equNA)),
     unlist(lapply(EXIT, equNA)))
# Get the order number of 1st non-NA value for FAVOR,ENTRY,EXIT

for( j in 1:ncol(ENTRY) ){
  toRm <- rmNA[j]
  if( toRm > (maxLookback + 1) &
      toRm < nrow(ENTRY) ){
    FAVOR[1:(toRm-1),j] <- NA
    ENTRY[1:(toRm-1),j] <- NA
    EXIT[1:(toRm-1),j] <- NA
  }
}

# Step 3   
# Optimization begins. Repeat Step 4 to 12 daily               
for( i in maxLookback:(nrow(CLOSE)-1) ){

  # Step 4 
  # Carry over Cash and Position from last period           
  C[i+1] <- C[i]
  P[i+1,] <- as.numeric(P[i,])
  p[i+1,] <- as.numeric(p[i,])

  longS <- S[which(P[i,] > 0)]
  shortS <- S[which(P[i,] < 0)]
  k <- length(longS) + length(shortS)

  # Step 5
  # Based on ENTRY, determine stocks to enter            
  longTrigger <- setdiff(S[which(ENTRY[i,] == 1)], longS)
  shortTrigger <- setdiff(S[which(ENTRY[i,] == -1)], shortS)
  trigger <- c(longTrigger, shortTrigger)

  # If more than K, prioterize entering based on FAVOR
  if( length(trigger) > K ) {

    keepTrigger <- trigger[order(c(as.numeric(FAVOR[i,longTrigger]),
                                   -as.numeric(FAVOR[i,shortTrigger])),
                                 decreasing = TRUE)][1:K]
    # Order decreasingly, Keep the first K triggers

    longTrigger <- longTrigger[longTrigger %in% keepTrigger]
    shortTrigger <- shortTrigger[shortTrigger %in% keepTrigger]
    trigger <- c(longTrigger, shortTrigger)                                                                                     

  }

  triggerType <- c(rep(1, length(longTrigger)), rep(-1, length(shortTrigger)))

  # Step 6
  # Determine stocks to exit based on EXIT     
  longExitTrigger <- longS[longS %in%
                             S[which(EXIT[i,] == 1 | EXIT[i,] == 999)]]

  shortExitTrigger <- shortS[shortS %in%
                               S[which(EXIT[i,] == -1 | EXIT[i,] == 999)]]

  exitTrigger <- c(longExitTrigger, shortExitTrigger)

  # Step 7
  # Determine if more stocks must be exited to respect K, with 'max'  
  needToExit <- max( (length(trigger) - length(exitTrigger)) - (K - k), 0)

  if( needToExit > 0 ){

    toExitLongS <- setdiff(longS, exitTrigger)
    toExitShortS <- setdiff(shortS, exitTrigger)

    toExit <- character(0)

    # Determine which stocks to exit based on FAVOR
    for( counter in 1:needToExit ){
      if( length(toExitLongS) > 0 & length(toExitShortS) > 0 ){
        if( min(FAVOR[i,toExitLongS]) < min(-FAVOR[i,toExitShortS]) ){
          pullMin <- which.min(FAVOR[i,toExitLongS])
          toExit <- c(toExit, toExitLongS[pullMin])
          toExitLongS <- toExitLongS[-pullMin]
        } else {
          pullMin <- which.min(-FAVOR[i,toExitShortS])
          toExit <- c(toExit, toExitShortS[pullMin])
          toExitShortS <- toExitShortS[-pullMin]
        }
      } else if( length(toExitLongS) > 0 & length(toExitShortS) == 0 ){
        pullMin <- which.min(FAVOR[i,toExitLongS])
        toExit <- c(toExit, toExitLongS[pullMin])
        toExitLongS <- toExitLongS[-pullMin]
      } else if( length(toExitLongS) == 0 & length(toExitShortS) > 0 ){
        pullMin <- which.min(-FAVOR[i,toExitShortS])
        toExit <- c(toExit, toExitShortS[pullMin])
        toExitShortS <- toExitShortS[-pullMin]
      }
    }

    longExitTrigger <- c(longExitTrigger, longS[longS %in% toExit])
    shortExitTrigger <- c(shortExitTrigger, shortS[shortS %in% toExit])

  }

  # Step 8
  # Finalize the vector of stocks to exit         
  exitTrigger <- c(longExitTrigger, shortExitTrigger)
  exitTriggerType <- c(rep(1, length(longExitTrigger)),
                       rep(-1, length(shortExitTrigger)))

  # Step 9
  # Exit all stocks marked for exit          
  if( length(exitTrigger) > 0 ){
    for( j in 1:length(exitTrigger) ){

      exitPrice <- as.numeric(OPEN[i+1,exitTrigger[j]])

      # slipFactor is a percentage of slippage to be added to each trade
      # Slippage is defined as the difference between the price in data and the price in execution not accounting for spreads
        ## For this input, 0.001 corresponds to a 0.1 percent handicap in each entry and exit
      effectivePrice <- exitPrice * (1 - exitTriggerType[j] * slipFactor) -
        exitTriggerType[j] * (perShareCommission + spreadAdjust)
        # spreadAdjust is the dollar value to handicap each trade, used to adjust for paying the spread in market orders
          # A value of 0.01 corresponds to a one-cent handicap

      if( exitTriggerType[j] == 1 ){

        C[i+1] <- C[i+1] +
          ( as.numeric( P[i,exitTrigger[j]] ) * effectivePrice )
        - flatCommission
        # flatCommission is the dollar value of a commission for a single trade of any size, incorporated at both entry and exit
          # If your brokerage offers a $7 flat commission at only the entry, a value of 3.50 will simulate this properly

      } else {

        C[i+1] <- C[i+1] -
          ( as.numeric( P[i,exitTrigger[j]] ) *
              ( 2 * as.numeric(p[i, exitTrigger[j]]) - effectivePrice ) )
        - flatCommission
      }

      P[i+1, exitTrigger[j]] <- 0
      p[i+1, exitTrigger[j]] <- 0

      k <- k - 1
    }
  }

  # Step 10
  # Enter all stocks marked for entry          
  if( length(trigger) > 0 ){
    for( j in 1:length(trigger) ){

      entryPrice <- as.numeric(OPEN[i+1,trigger[j]])

      effectivePrice <- entryPrice * (1 + triggerType[j] * slipFactor) +
        triggerType[j] * (perShareCommission + spreadAdjust)
        # perShareCommission is the dollar value to handicap the price of each share to simulate the effects of commissions charged on a per-share basis
          # If the per-share commission is one-half of a cent each way, the proper value is 0.005

      P[i+1,trigger[j]] <- triggerType[j] *
        floor( ( (C[i+1] - flatCommission) / (K - k) ) / effectivePrice )

      p[i+1,trigger[j]] <- effectivePrice

      C[i+1] <- C[i+1] -
        ( triggerType[j] * as.numeric(P[i+1,trigger[j]]) * effectivePrice )
      - flatCommission

      k <- k + 1

    }
  }

  # Step 11
  # Loop through active positions to determine equity for the period       
  equity[i] <- C[i+1]
  for( s in S[which(P[i+1,] > 0)] ){
    equity[i] <- equity[i] +
      as.numeric(P[i+1,s]) *
      as.numeric(OPEN[i+1,s])                                                                                     
  }

  for( s in S[which(P[i+1,] < 0)] ){
    equity[i] <- equity[i] -
      as.numeric(P[i+1,s]) *
      ( 2 * as.numeric(p[i+1,s]) - as.numeric(OPEN[i+1,s]) )
  }

  # failThresh is the dollar value of the equity curve at which to halt the process
  if( equity[i] < failThresh ){
    warning("\n*** Failure Threshold Breached ***\n")
    break
  }

  # Step 12
  # If verbose=TRUE then output optimization diagnostics every 21 trading days
  # verbose is a logical flag indicating whether to output performance information as the function walks through time
  if( verbose ){
    if( i %% 21 == 0 ){
      cat(paste0("################################## ",
                 round(100 * (i - maxLookback) /
                         (nrow(CLOSE) - 1 - maxLookback), 1), "%",
                " ##################################\n"))
      cat(paste("Date:\t",as.character(index(CLOSE)[i])), "\n")
      cat(paste0("Equity:\t", " $", signif(equity[i], 5), "\n"))
      cat(paste0("CAGR:\t ",
                 round(100 * ((equity[i] / (equity[maxLookback]))^
                                (252/(i - maxLookback + 1)) - 1), 2),
                 "%"))
      cat("\n")
      cat("Assets:\t", S[P[i+1,] != 0])
      cat("\n\n")
    }
  }

}

# Step 13
# Return equity curve, cash vector, share count matrix, and entry price matrix                  
return(list(equity = equity, C = C, P = P, p = p))

}