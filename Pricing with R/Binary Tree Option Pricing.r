# Binary Tree for European Call (no div)
## price is the vector for (steps+1) times of stock price senario at end
## call_value is the vector for Call Value of all senarios at end
bt_eu_c <- function(S, X, r, sigma, t, steps) {
        R <- exp(r*(t/steps))
        R_recip <- 1/R
        u <- exp(sigma*sqrt(t/steps))
        d <- 1/u
        u_square <- u^2
        p_up <- (R-d)/(u-d)
        p_down <- 1-p_up
        price <- numeric(steps +1)
        price[1] <- S * d^steps
        for (i in 2:(steps+1)) {
                price[i] <- u_square * price[i-1]
        }
        call_value <- numeric(steps+1)
        call_value <- pmax(0, price - X)
        for (j in steps:1) {
                for (i in 1:j) {
                        call_value[i] <- (p_up*call_value[i+1] + p_down*call_value[i]) * R_recip
                }
        }
        return(call_value[1])
}





# Binary Tree for European Put (no div)
bt_eu_p <- function(S, X, r, sigma, t, steps) {
        R <- exp(r*(t/steps))
        R_recip <- 1/R
        u <- exp(sigma*sqrt(t/steps))
        d <- 1/u
        u_square <- u^2
        p_up <- (R-d)/(u-d)
        p_down <- 1-p_up
        price <- numeric(steps +1)
        price[1] <- S * d^steps
        for (i in 2:(steps+1)) {
                price[i] <- u_square * price[i-1]
        }
        put_value <- numeric(steps+1)
        put_value <- pmax(0, X - price)
        for (j in steps:1) {
                for (i in 1:j) {
                        put_value[i] <- (p_up*put_value[i+1] + p_down*put_value[i]) * R_recip
                }
        }
        return(put_value[1])
}



# Binary Tree for American Call (no div)
## Add Process to determine if worthy of using option at per period
bt_us_c <- function(S, X, r, sigma, t, steps) {
        R <- exp(r*(t/steps))
        R_recip <- 1/R
        u <- exp(sigma*sqrt(t/steps))
        d <- 1/u
        u_square <- u^2
        p_up <- (R-d)/(u-d)
        p_down <- 1-p_up
        price <- numeric(steps +1)
        price[1] <- S * d^steps
        for (i in 2:(steps+1)) {
                price[i] <- u_square * price[i-1]
        }
        call_value <- numeric(steps+1)
        call_value <- pmax(0, price - X)
        for (j in steps:1) {
                for (i in 1:j) {
                        call_value[i] <- (p_up*call_value[i+1] + p_down*call_value[i]) * R_recip
                        price[i] <- d * price[i+1]
                        call_value[i] <- max(call_value[i], price[i] - X)
                }
        }
        return(call_value[1])
}



# Binary Tree for American Put (no div)
bt_us_p <- function(S, X, r, sigma, t, steps) {
        R <- exp(r*(t/steps))
        R_recip <- 1/R
        u <- exp(sigma*sqrt(t/steps))
        d <- 1/u
        u_square <- u^2
        p_up <- (R-d)/(u-d)
        p_down <- 1-p_up
        price <- numeric(steps +1)
        price[1] <- S * d^steps
        for (i in 2:(steps+1)) {
                price[i] <- u_square * price[i-1]
        }
        put_value <- numeric(steps+1)
        put_value <- pmax(0, X - price)
        for (j in steps:1) {
                for (i in 1:j) {
                        put_value[i] <- (p_up*put_value[i+1] + p_down*put_value[i]) * R_recip
                        price[i] <- d*price[i+1]
                        put_value[i] <- max(put_value[i], X - price[i])
                }
        }
        return(put_value[1])
}



# Binary Tree for American Call (with div)
bt_us_cdiv <- function(S, X, r, y, sigma, t, steps) {
        R <- exp(r*(t/steps))
        R_recip <- 1/R
        u <- exp(sigma*sqrt(t/steps))
        d <- 1/u
        u_square <- u^2
        p_up <- (exp((r-y)*t/steps)-d)/(u-d)
        p_down <- 1-p_up
        price <- numeric(steps +1)
        price[1] <- S * d^steps
        for (i in 2:(steps+1)) {
                price[i] <- u_square * price[i-1]
        }
        call_value <- numeric(steps+1)
        call_value <- pmax(0, price - X)
        for (j in steps:1) {
                for (i in 1:j) {
                        call_value[i] <- (p_up*call_value[i+1] + p_down*call_value[i]) * R_recip
                        price[i] <- d * price[i+1]
                        call_value[i] <- max(call_value[i], price[i] - X)
                }
        }
        return(call_value[1])
}
# y is continuous divident rate


# Binary Tree for American Put (with div)
bt_us_pdiv <- function(S, X, r, y, sigma, t, steps) {
        R <- exp(r*(t/steps))
        R_recip <- 1/R
        u <- exp(sigma*sqrt(t/steps))
        d <- 1/u
        u_square <- u^2
        p_up <- (exp((r-y)*t/steps)-d)/(u-d)
        p_down <- 1-p_up
        price <- numeric(steps +1)
        price[1] <- S * d^steps
        for (i in 2:(steps+1)) {
                price[i] <- u_square * price[i-1]
        }
        put_value <- numeric(steps+1)
        put_value <- pmax(0, X - price)
        for (j in steps:1) {
                for (i in 1:j) {
                        put_value[i] <- (p_up*put_value[i+1] + p_down*put_value[i]) * R_recip
                        price[i] <- d*price[i+1]
                        put_value[i] <- max(put_value[i], X - price[i])
                }
        }
        return(put_value[1])
}
