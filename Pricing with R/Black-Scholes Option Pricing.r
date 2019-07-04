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



