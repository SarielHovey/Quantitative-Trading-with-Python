# Greeks for European Call(no div)
greek_call <- function(S, X, rf, sigma, T) {
        Ts <- sqrt(T)
        d1 <- (log(S/X) + (rf + 0.5*sigma^2)*T)/(sigma*sqrt(T))
        d2 <- d1 - sigma*Ts
        nd1 <- 1/(sqrt(2*3.1415926)) * exp(-d1^2 /2)
        Delta <- pnorm(d1)
        Gamma <- nd1 / (S*sigma*Ts)
        Theta <- -(S*sigma*nd1)/(2*Ts) - rf*X*exp(-rf*T)*pnorm(d2)
        Vega <- S * Ts * nd1
        Rho <- X*T*exp(-rf*T)*pnorm(d2)
        Greeks_C <- c(Delta, Gamma, Theta, Vega, Rho)
        names(Greeks_C) <- c('Delta','Gamma','Theta','Vega','Rho')
        return(Greeks_C)
}




# Greeks for European Put(no div)
greek_put <- function(S, X, rf, sigma, T) {
        Ts <- sqrt(T)
        d1 <- (log(S/X) + (rf + 0.5*sigma^2)*T)/(sigma*sqrt(T))
        d2 <- d1 - sigma*Ts
        nd1 <- 1/(sqrt(2*3.1415926)) * exp(-d1^2 /2)
        Delta <- pnorm(d1) - 1
        Gamma <- nd1 / (S*sigma*Ts)
        Vega <- S * Ts * nd1
        Theta <- -(S*nd1*sigma)/(2*Ts) + rf*X*exp(-rf*T)*pnorm(-d2)
        Rho <- X*T*exp(-rf*T)*pnorm(-d2)
        Greeks_P <- c(Delta, Gamma, Theta, Vega, Rho)
        names(Greeks_P) <- c('Delta','Gamma','Theta','Vega','Rho')
        return(Greeks_P)
}
