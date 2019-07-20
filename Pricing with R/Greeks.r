# Greeks for European Call(no div)
greek_call <- function(S, X, rf, sigma, T) {
        Ts <- sqrt(T)
        d1 <- (log(S/X) + (rf + 0.5*sigma^2)*T)/(sigma*sqrt(T))
        d2 <- d1 - sigma*Ts
        nd1 <- 1/(sqrt(2*pi)) * exp(-d1^2 /2)
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
        nd1 <- 1/(sqrt(2*pi)) * exp(-d1^2 /2)
        Delta <- pnorm(d1) - 1
        Gamma <- nd1 / (S*sigma*Ts)
        Vega <- S * Ts * nd1
        Theta <- -(S*nd1*sigma)/(2*Ts) + rf*X*exp(-rf*T)*pnorm(-d2)
        Rho <- X*T*exp(-rf*T)*pnorm(-d2)
        Greeks_P <- c(Delta, Gamma, Theta, Vega, Rho)
        names(Greeks_P) <- c('Delta','Gamma','Theta','Vega','Rho')
        return(Greeks_P)
}



# Greeks for European Call(with div)
## q is continuously compounded dividend yield
## Delta_call for stocks with div is between 0 and exp(-q*T)
## Gamma for Call or Put is always positive; Gamma max when option is At-the-Money
## Theta is Time Decay for Option, thus is always negative
## During very short T, according to Tyler, $ \delta_C = Theta* \delta_T + Delta * \delta_S + 0.5*Gamma*(\delta_S)^2 $
greek_call <- function(S, X, rf, q, sigma, T) {
    Ts <- sqrt(T)
    d1 <- (log(S/X) + (rf - q + 0.5*sigma^2)*T)/(sigma*sqrt(T))
    d2 <- d1 - sigma*Ts
    nd1 <- 1/(sqrt(2*pi)) * exp(-d1^2 /2)
    Delta <- exp(-q*T)*pnorm(d1)
    Gamma <- exp(-q*T) * nd1 / (S*sigma*Ts)
    Greeks_C <- c(Delta, Gamma)
    names(Greeks_C) <- c('Delta','Gamma')
    return(Greeks_C)
}



# Greeks for European Put(with div)
greek_put <- function(S, X, rf, q, sigma, T) {
    Ts <- sqrt(T)
    d1 <- (log(S/X) + (rf - q + 0.5*sigma^2)*T)/(sigma*sqrt(T))
    d2 <- d1 - sigma*Ts
    Delta <- -exp(-q*T)*pnorm(-d1)
    Gamma <- exp(-q*T) * nd1 / (S*sigma*Ts)
    Greeks_P <- c(Delta, Gamma)
    names(Greeks_P) <- c('Delta','Gamma')
    return(Greeks_P)
}


