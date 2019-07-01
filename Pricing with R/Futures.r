# Caution: All insterests are yearly continuous compounding interest

# Long side: $Future Price = S_0*(1 + r_f)^T + PV(holding csot) - PV(holding return)$


#                                       # FX Futures #
# $ f_t + K*e^{-r_1(T-t)} = S_t*e^{-r_2(T-t)} $
# $ F_t = S_t * e^{(r_1 - r_2)*(T-t)}
whqhvalue = function(S, r1, K, r2, time) {
        f = S * exp(-r2 * time) - K * exp(-r1 * time)
        return(f)
}

whqhprice = function(S, r1, r2, time) {
        F = S * exp((r1 - r2) * time)
        return(F)
}
# r1 is domestic interest; r2 is foreign interest


#                                       # Stock Index Futures #
# $ F_t = S_t * e^{(r-q)(T-t)} $
gzqhprice = function(S, r, q, time) {
        F = S * exp((r-q) * time)
        return(F)
}


#                                       # Interest Futures #
## Long term bonds with interest
## I is the present value of interest during 'time'
zcqzqh = function(S, I, r, time) {
        F = (S - I) * exp(r * time)
        return(F)
}


## Short term bills
## V is principle value of bill
## r1 is interest of time T; T1 is (T-t)
## r2 is interest of time bill expires; T2 is the time bill expires
## T2 > T1
dqgzqhprice = function(V, r1, r2, t1, t2) {
        r = (r2 * t2 -r1 * t1)/(t2 - t1)
        F = V * exp(-r * (t2 - t1) / 365)
        return(F)
}
## r is defined to be forward interest
