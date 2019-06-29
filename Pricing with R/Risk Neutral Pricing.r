# 1-period Arbitrage Free Pricing
# $ S =  e^{-r(T-t)} (S_u P + S_d (1-P)) $
# Easy to get $ P= \prep{e^{-r(T-t)} - d}{u - d} $
# forward price $ f = e^{-r(T-t)} (Pf_u + (1-P)f_d) $

# For Forward Price calculation
qqjz <- function(rf, time, u, d, s0, X){
    p = (exp(rf * time) - d) / (u - d)
    f = exp(-rf * time)(p * max(s0*u - X, 0) + (1-p) * max(X - s0*d, 0))
    return(f)
}
# max(s0*u - X, 0) is f_u; s0 is Spot stock price at $t_0$; time is ${period time}/{a year}$; rf is risk-free rate yearly

# For Risk Neutral Probability
qqjz0 <- function(rf, time, u, d, s0, X){
    p = (exp(rf * time) - d) / (u - d)
    return(p)
}
