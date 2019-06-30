## Caution: All below interests are continuously compounding interest

#                                       # Forwards with no interest paid #
# $f_t + K* \exp{-r*(T-t)} = S_t$
# Forward Value 'f_t' for long side at time t
yqvalue <- function(S, K, rf, time) {
        f = S - K * exp(-rf * time)  
        return(f)
}
# S_t is underlying price at t; K is contract price
# Forward Price 'F_t' at time t
# F_t is the K value to make f_t=0 at time t
yqprice <- function(S,K,rf,time) {
        F = S * exp(rf * time)
        return(F)
}


#                                       # Forwards with known underlying cash return #
# $ f_t = S_t - I_t - K*\exp{-r*(T-t)} $
# $ F_t = (S_t - I_t) * \exp{r*(T-t)} $
# I_t is the Present Value of return for underlying during (T-t)
# pv_div returns I_t
pv_div <- function(div, time, r) {
        s = div * exp(-r * time)
        s1 = sum(s)
        return(s1)
}
# e.g.  div = c(60, 60) & r = c(0.09, 0.1)
yqivalue <- function(div, time, r, S, K, rf, time1) {
        I = pv_div(div, time, r)
        f = S - I - K*exp(-rf * time1)
        return(f)
}

yqiprice <- function(div, time, r, S, K, rf, time1) {
        I = pv_div(div, time, r)
        F = (S - I) * exp(rf * time1)
        return(F)
}


#                                       # Forwards with known return rate #
# $ f_t + K* \exp{-r(T-t)} = S_t \exp{-q(T-t)} $
# q is the average return for interest re-invest during (T-t)
yqqvalue <- function(S, K, r, q, time) {
#       I = pv_div(div, time, r)
        f = S * exp(-q * time) - K * exp(-r * time)
        return(f)
}
        
yqqprice <- function(S, r, q, time) {
        F = S * exp((r - q) * time)
        return(F)
}
