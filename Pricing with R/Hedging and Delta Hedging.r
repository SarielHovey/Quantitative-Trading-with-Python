# Hedging with self-made Put (Long Stock)
## dt is $ T-t $, can be a vector; $ p =  $
omega <- function(S, X, dt, rf, sigma) {
        d1 <- (log(S/X) + (rf + 0.5*sigma^2)*dt) / (sigma*sqrt(dt))
        d2 <- d1 - sigma*sqrt(dt)
        Nd1 <- pnorm(d1)
        Nd2 <- pnorm(d2)
        Call <- S*Nd1 - X*Nd2*exp(-rf*dt)
        Put <- Call - S + X*exp(-rf*dt)
        p <- S*Nd1/(S + Put)
        return(p)
}

## Example of omega()
### Price for S for 53 weeks
S <- c(56,60,62.50,63.20,62.80,57.10,57.84,57.52,58.61,59.02,61.64,64.76,67.42,67.66,68.39,70.92,73.10,68.95,65.13,65.82,65.64,64.20,
      64.64,64.50,66.86,69.03,66.04,67.10,68.15,68.17,65.77,65.74,63.73,66.94,68.32,70.10,75.21,70.25,72.50,74.03,70.51,70.60,71.62,70.64,
      68.14,71.67,71.34,77.05,74.60,76.40,81.28,85.83,92.50)
week <- 0:52
### Initial portfolio value
deposit <- 1000
### Target floor limit price, also the X for Put option
X <- rep(50,53)
dt <- 1- week/52
rf <- 0.08
sigma <- 0.30
### 'p' is the percentage of 'deposit' to purchase stocks
p <- omega(S, X, dt, rf, sigma)
### use diff() to count weekly return for S
stock.R <- c(exp(diff(log(S))), 1)
bond.R <- c(rep(1+rf/52, 52), 1)
p_Return <- p*stock.R + (1-p)*bond.R
### use cumsum() to count cumulative return. e.g. cumsum(1:4) returns c(1,3,6,10)
cum.R <- exp(cumsum(log(p_Return)))
### Portfolio value for 53 weeks
p_Value <- deposit * cum.R



# Hedging with Delta
Delta <- function(S, X, dt, rf, sigma) {
        d1 <- (log(S/X) + (rf+ 0.5*sigma^2)*dt) / (sigma*sqrt(dt))
        Nd1 <- pnorm(d1)
        return(Nd1)
}

## Short Call -- 10000 contracts
### Price for S for 53 weeks
S <- c(56,60,62.50,63.20,62.80,57.10,57.84,57.52,58.61,59.02,61.64,64.76,67.42,67.66,68.39,70.92,73.10,68.95,65.13,65.82,65.64,64.20,
      64.64,64.50,66.86,69.03,66.04,67.10,68.15,68.17,65.77,65.74,63.73,66.94,68.32,70.10,75.21,70.25,72.50,74.03,70.51,70.60,71.62,70.64,
      68.14,71.67,71.34,77.05,74.60,76.40,81.28,85.83,92.50)
X <- rep(50,length(S))
week <- 0:(length(S) - 1)
dt <- 1- week/52
rf <- 0.08
sigma <- 0.30
### N is the number of long stocks to hedge short call given Delta
N <- Delta(S, X, dt, rf, sigma) * 10000
### stock.cost is the cash needed for long stocks
stock.cost <- N*S
### stock.change is the cash needed per period for long stocks
stock.change <- c(0,diff(N)) * S
R <- c(1, rep(exp(rf/52), (length(S)-1)))
### cost is cumulative cost for constantly adjusting long stocks
cost <- rep(NA, length(S))
interest.cost <- rep(0, length(S))
cost[1] <- stock.cost[1]
for (i in 2:length(S)) {
        cost[i] <- cost[i-1] * R[i] + stock.change[i]
}
### interest.cost is cumulative interest cost
interest.cost <- cost * (exp(rf/52) - 1)
interest.cost <- c(0, interest.cost[-14])
