# 1-time simulation for S_T
## Given Ito, $ S_T = S_t*exp((r - 0.5* sigma^2) + sigma * echo * sqrt(T-t)) $, echo is a normal distribution
## sigma, rf are both yearly data
sim_rand <- function(S, r, sigma, t) {
        R <- (r - 0.5*sigma^2) * t
        SD <- sigma * sqrt(t)
        S_T <- 0.000000
        S_T <- S * exp(R + SD*rnorm(1))
        return(S_T)
}




# Monte Carlo Simulation for European Call
payoff_call <- function(price, X) {
        return(max(0, price - X))
}

p_sim <- function(S, r, sigma, t) {
        R <- (r - 0.5*sigma^2)*t
        SD <- sigma * sqrt(t)
        return(S * exp(R + SD*rnorm(1)))
}
## Current price C_t for Call
mc_eu_c <- function(S, X, r, sigma, t, n) {
        s_t <- numeric(n)
        sum_payoff <- numeric(n)
        for (i in 1:n) {
                s_t[i] <- p_sim(S, r, sigma, t)
                sum_payoff[i] <- payoff_call(s_t[i], X)
        }
        s <- sum(sum_payoff)
        return(exp(-r*t)*s/n)
}





# Monte Carlo Simulation for European Put
payoff_put <- function(price, X) {
        return(max(0, X- price))
}

p_sim <- function(S, r, sigma, t) {
        R <- (r - 0.5*sigma^2)*t
        SD <- sigma * sqrt(t)
        return(S * exp(R + SD*rnorm(1)))
}
# n is the times to simulate, t is $T-t$
mc_eu_p <- function(S, X, r, sigma, t, n) {
        s_t <- numeric(n)
        sum_payoff <- numeric(n)
        for (i in 1:n) {
                s_t[i] <- p_sim(S, r, sigma, t)
                sum_payoff[i] <- payoff_put(s_t[i], X)
        }
        s <- sum(sum_payoff)
        return(exp(-r*t)*s/n)
}




# Antithetic Variate (对偶变量法) Monte Carlo for European Call
## use pmax() to work on Vector
payoff_call_v <- function(price, X) {
        return(pmax(0, price - X))
}
## Caution: s_t1 and s_t2 are Vectors, max() returns 1 value
mcav_eu_c <- function(S, X, r, sigma, t, n) {
        R <- (r - 0.5*sigma^2) * t
        SD <- sigma*sqrt(t)
        s_t1 <- numeric(n)
        s_t2 <- numeric(n)
        sum_poff1 <- numeric(n)
        sum_poff2 <- numeric(n)
        sum_poff_avg <- numeric(n)
        for (i in 1:n) {
                x <- rnorm(1)
                s_t1[i] <- S*exp(R+SD*x)
                s_t2[i] <- S*exp(R+SD*(-x))
        }
        sum_poff1 <- payoff_call_v(s_t1, X)
        sum_poff2 <- payoff_call_v(s_t2, X)
        sum_poff_avg <- (sum_poff1 + sum_poff2)/2
        s <- sum(sum_poff_avg)
        return(exp(-r*t)*s/n)
}


# Antithetic Variate (对偶变量法) Monte Carlo for European Put
payoff_put_v <- function(price, X) {
        return(pmax(0, X - price))
}

mcav_eu_p <- function(S, X, r, sigma, t, n) {
        R <- (r - 0.5*sigma^2) * t
        SD <- sigma*sqrt(t)
        s_t1 <- numeric(n)
        s_t2 <- numeric(n)
        sum_poff1 <- numeric(n)
        sum_poff2 <- numeric(n)
        sum_poff_avg <- numeric(n)
        for (i in 1:n) {
                x <- rnorm(1)
                s_t1[i] <- S*exp(R+SD*x)
                s_t2[i] <- S*exp(R+SD*(-x))
        }
        sum_poff1 <- payoff_put_v(s_t1, X)
        sum_poff2 <- payoff_put_v(s_t2, X)
        sum_poff_avg <- (sum_poff1 + sum_poff2)/2
        s <- sum(sum_poff_avg)
        return(exp(-r*t)*s/n)
}



# Variable Controlling Monte Carlo for European Call
## Caution: S_1 and S_2 should be very alike stocks
payoff_call <- function(price, X) {
        return(pmax(0, price - X))
}

sim_rand <- function(S, r, sigma, t) {
        R <- (r - 0.5*sigma^2) * t
        SD <- sigma * sqrt(t)
        S_T <- 0.000000
        S_T <- S * exp(R + SD*rnorm(1))
        return(S_T)
}

bscall_option <- function(S, X, rf, sigma, T) {
        d1 <- (log(S/X) + (rf + 0.5 * sigma^2)*T) / (sigma*sqrt(T))
        d2 = d1 - sigma*sqrt(T)
        C <- 0.000000
        C <- S * pnorm(d1) - X * exp(-rf * T) * pnorm(d2)
        return(C)        
}

mcvc_eu_c <- function(S_1, S_2, X, r, sigma, t, n) {
        c_bs2 <- bscall_option(S_2, X, r, sigma, t)
        s_t1 <- numeric(n)
        s_t2 <- numeric(n)
        sum_payoff1 <- numeric(n)
        sum_payoff2 <- numeric(n)
        for (i in 1:n) {
                s_t1[i] <- sim_rand(S_1, r, sigma, t)
                s_t2[i] <- sim_rand(S_2, r, sigma, t)
        }
        sum_payoff1 <- payoff_call(s_t1, X)
        sum_payoff2 <- payoff_call(s_t2, X)
        t1 <- sum(sum_payoff1)
        t2 <- sum(sum_payoff2)
        c_sim1 <- exp(-r*t)*t1/n
        c_sim2 <- exp(-r*t)*t2/n
        return(c_sim1 + c_bs2 - c_sim2)
}



# Variable Controlling Monte Carlo for European Put
## Caution: S_1 and S_2 should be very alike stocks
payoff_put <- function(price, X) {
        return(pmax(0, X - price))
}

sim_rand <- function(S, r, sigma, t) {
        R <- (r - 0.5*sigma^2) * t
        SD <- sigma * sqrt(t)
        S_T <- 0.000000
        S_T <- S * exp(R + SD*rnorm(1))
        return(S_T)
}

bsput_option <- function(S, X, rf, sigma, T) {
        d1 <- (log(S/X) + (rf + 0.5 * sigma^2)*T) / (sigma*sqrt(T))
        d2 <- d1 - sigma*sqrt(T)
        P <- 0.000000
        P <- X * exp(-rf * T) * pnorm(-d2) - S * pnorm(-d1)
        return(P) 
}

mcvc_eu_p <- function(S_1, S_2, X, r, sigma, t, n) {
        c_bs2 <- bsput_option(S_2, X, r, sigma, t)
        s_t1 <- numeric(n)
        s_t2 <- numeric(n)
        sum_payoff1 <- numeric(n)
        sum_payoff2 <- numeric(n)
        for (i in 1:n) {
                s_t1[i] <- sim_rand(S_1, r, sigma, t)
                s_t2[i] <- sim_rand(S_2, r, sigma, t)
        }
        sum_payoff1 <- payoff_put(s_t1, X)
        sum_payoff2 <- payoff_put(s_t2, X)
        t1 <- sum(sum_payoff1)
        t2 <- sum(sum_payoff2)
        c_sim1 <- exp(-r*t)*t1/n
        c_sim2 <- exp(-r*t)*t2/n
        return(c_sim1 + c_bs2 - c_sim2)
}

