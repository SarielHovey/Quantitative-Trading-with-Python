# Interest Cap
## Fk is Future Interest; Rx is interest cap; L is principle; r is risk-free rate; sigma is sd of Fk;
## tau is effective time for option; k is times of paying interest
bs_IRcap <- function(Fk, Rx, L, r, sigma, tau, k) {
    sigmasqr <- sigma^2
    tausqrt <- sqrt(k*tau)
    d1 <- (log(Fk/Rx) + 0.5*sigmasqr*k*tau) / (sigma*tausqrt)
    d2 <- d1 - sigma*tausqrt
    callp <- (tau*L)/(1+tau*Fk)*exp(-r*k*tau)*(Fk*pnorm(d1)-Rx*pnorm(d2))
    return(callp)
}



# Interest Floor
bs_IRfloor <- function(Fk, Rx, L, r, sigma, tau, k) {
    sigmasqr <- sigma^2
    tausqrt <- sqrt(k*tau)
    d1 <- (log(Fk/Rx) + 0.5*sigmasqr*k*tau) / (sigma*tausqrt)
    d2 <- d1 - sigma*tausqrt
    putp <- -(tau*L)/(1+tau*Fk)*exp(-r*k*tau)*(Fk*pnorm(-d1)+Rx*pnorm(-d2))
    return(putp)
}




# Zero-Bond Call
bs_zbo_c <- function(B, X, R, sigma, t) {
    sigmasqr <- sigma^2
    tsqr <- sqrt(t)
    d1 <- (log(B/X) + (R +0.5*sigmasqr)*t) / (sigma*tsqr)
    d2 <- d1 - sigma*tsqr
    c <- B*pnorm(d1) - X*exp(-R*t)*pnorm(d2)
    return(c)
}



# Zero-Bond Put
bs_zbo_p <- function(B, X, R, sigma, t) {
    sigmasqr <- sigma^2
    tsqr <- sqrt(t)
    d1 <- (log(B/X) + (R +0.5*sigmasqr)*t) / (sigma*tsqr)
    d2 <- d1 - sigma*tsqr
    p <- X*exp(-R*t)*pnorm(-d2) - B*pnorm(-d1)
    return(p)
}



# Bond Call with coupon
bs_cbo_c <- function(B, X, r, sigma, t, co_pay_times, co_amt) {
    n <- t %/% co_pay_times
    cou_amt_vector <- numeric(n-1)
    cou_pay_times_vector <- numeric(n-1)
    cou_discount <- numeric(n-1)
    cou_amt_vector <- cou_amt_vector + co_amt
    cou_pay_times_vector <- cou_pay_times_vector + co_pay_times
    for (i in 1:(n-1)) {
        cou_discount[i] <- cou_amt_vector[i] * exp(-r* i* cou_pay_times_vector[i])
        }
    total_discount <- sum(cou_discount)
    adjust_B <- B - total_discount
    return(bs_zbo_c(adjust_B, X, r, sigma, t))
}



# Bond Put with coupon
bs_cbo_p <- function(B, X, r, sigma, t, co_pay_times, co_amt) {
    n <- t %/% co_pay_times
    cou_amt_vector <- numeric(n-1)
    cou_pay_times_vector <- numeric(n-1)
    cou_discount <- numeric(n-1)
    cou_amt_vector <- cou_amt_vector + co_amt
    cou_pay_times_vector <- cou_pay_times_vector + co_pay_times
    for (i in 1:(n-1)) {
        cou_discount[i] <- cou_amt_vector[i] * exp(-r* i* cou_pay_times_vector[i])
        }
    total_discount <- sum(cou_discount)
    adjust_B <- B - total_discount
    return(bs_zbo_p(adjust_B, X, r, sigma, t))
}






