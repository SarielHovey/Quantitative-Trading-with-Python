# European Call without div
# S is {S_0}, the current price for S
bscall_option <- function(S, X, rf, sigma, T) {
        d1 <- (log(S/X) + (rf + 0.5 * sigma^2)*T) / (sigma*sqrt(T))
        d2 = d1 - sigma*sqrt(T)
        C <- 0.000000
        C <- S * pnorm(d1) - X * exp(-rf * T) * pnorm(d2)
        return(C)        
}


# European Put without div
bsput_option <- function(S, X, rf, sigma, T) {
        d1 <- (log(S/X) + (rf + 0.5 * sigma^2)*T) / (sigma*sqrt(T))
        d2 <- d1 - sigma*sqrt(T)
        P <- 0.000000
        P <- X * exp(-rf * T) * pnorm(-d2) - S * pnorm(-d1)
        return(P) 
}


# European Call with div
divbscall_option <- function(S, X, rf, div, divT, sigma, T) {
        d1 <- (log(S/X) + (rf + 0.5 * sigma^2)*T) / (sigma*sqrt(T))
        d2 <- d1 - sigma*sqrt(T)
        V <- 0.000000
        V <- sum(div * exp(-rf * divT))
        C <- 0.000000
        C <- (S-V) * pnorm(d1) - X * exp(-rf * T) * pnorm(d2)
        return(C)
}


# European Put with div
divbsput_option <- function(S, X, rf, div, divT, sigma, T) {
        d1 <- (log(S/X) + (rf + 0.5 * sigma^2)*T) / (sigma*sqrt(T))
        d2 <- d1 - sigma*sqrt(T)
        V <- 0.000000
        V <- sum(div * exp(-rf * divT))
        P <- 0.000000
        P <- X * exp(-rf*T) * pnorm(-d2) - (S-V) * pnorm(-d1)
        return(P)
}


# Implied Volatility
## Bisection method for IV
## op is the current market price of option
# options(digits = 6)
opimvol <- function(S, X, rf, T, op) {
        accu <- 1e-7
        maxiter <- 200
        error <- -1e40
        sigma_left <- 1e-7
        sigma_right <- 1
        for (i in 0:maxiter) {
                sigma <- (sigma_left + sigma_right)/2
                price <- bscall_option(S, X, rf, sigma, T)
                test <- price - op
                if(abs(test) < accu) return(sigma)
                if(test < 0.0) 
                        sigma_left <- sigma
                else
                        sigma_right <- sigma
        }
}


## Newton-Raphson method
## $ x_{n+1} = x_n - \prep{f(x_n}{f'(x_n)} $
newtonopimvol <- function(S, X, fr, T, op) {
        accu <- 1e-6
        maxiter <- 200
        error <- -1e40
        ts <- sqrt(T)
        sigma < (op/S)/(0.398*ts)
        for(i in 0:maxiter) {
                price <- bscall_option(S, X, rf, sigma, T)
                diff <- op - price
                if(abs(diff) < accu) return(sigma)
                d1 <- (log(S/X) + (rf + 0.5*sigma^2)*T) / (sigma*sqrt(T))
                nd1 <- 1/(sqrt(2*pi)) * exp(- d1^2/2)
                vega <- S*ts*nd1
                sigma <- sigma + diff/vega
        }
        return(error)
}





