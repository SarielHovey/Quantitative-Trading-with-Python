# 1-time simulation for S_T
## Given Ito, $ S_T = S_t*exp((r - 0.5* sigma^2) + sigma * echo * sqrt(T-t)) $, echo is a normal distribution
## sigma, rf are both yearly data
sim_rand <- function(S, rf, sigma, t) {
        R <- (rf - 0.5*sigma^2) * t
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

