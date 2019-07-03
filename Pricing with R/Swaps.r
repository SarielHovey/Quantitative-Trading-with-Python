#                                       # Interest Swap #
# Caution: All below rates are yearly continuously compounding interest rate
## Fix-Float IRS(no principle exchange)
bportwap_price <- function(times, cf, r, A, fr, time) {
        b1 = cf / exp(r * times)
        s1 = sum(b1)
        b2 = A / exp(fr * time)
        V = b2 - s1
        return(V)
}
## Example: times = c(0.25, 0.75, 1.25); cf = c(4, 4, 104); r = c(0.1,0.105,0.11)
## 对于float side而言,每次浮动利息支付日,其价值被重设为100,因此现值A为(面值+最近一次浮动利息)对下一次付息时间time的贴现值

### For fix rate calculation
### For a Fix-float IRS, at deal date the value should be 0, given the floating rate, the fixed rate:
### assume the contract makes payment 'n' times a year, we have
### $ (1 + r_i / n)^i * (1 + f_{i+1,i} / n) = (1 + r_{i+1} / n)^(i+1) $
### f_{i+1,i} is the Forward Rate in time i to time i+1; Obviously, we have f_{1,0} = r_1
bportwap_fix <- function(r) {
        n <- length(r)
        fr <- rep(NA, n)
        fr[1] <- r[1]
        for (i in 2:n) {fr[i] <- ((1+ r[i]/n)^i / (1+ r[i-1]/n)^(i-1) -1) *n }
        rr <- rep(NA, n)
        for (i in 1:n) {rr[i] <- (1 + r[i] / n)^i}
        fix <- sum(fr / rr) / sum(rr)
        return(fix)
}




## Currency Swap(principle exchange)
## S is current fx rate, {domestic currency}/{foreign currency}
## cf1, cf2, time can all be vectors
curr_swap_price = function(S, time, cf1, cf2, y1, y2) {
        bf = cf1 * exp(-y1 * time)
        bd = cf2 * exp(-y2 * time)
        s1 = sum(bf)
        s2 = sum(bd)
        V = S * s1 - s2
        return(V)
}

