# Asian Call (Geometric Average)
bs_as_ga_c <- function(S_av, X, r, q, sigma, t) {
        sigma_sqr <- sigma^2
        qp <- 0.5*(r+q+sigma_sqr/6)
        sigmap <- sigma/sqrt(3)
        sigmap_sqr <- sigmap^2
        tsqr <- sqrt(t)
        d1 <- (log(S_av/X)+ (r-qp+0.5*sigmap_sqr)*t) / (sigmap*tsqr)
        d2 <- d1 - sigmap*tsqr
        callp <- S_av*exp(-qp*t)*pnorm(d1) - X*exp(-r*t)*pnorm(d2)
        return(callp)
}



# Asian Put (Geometric Average)
bs_as_ga_p <- function(S_av, X, r, q, sigma, t) {
        sigma_sqr <- sigma^2
        qp <- 0.5*(r+q+sigma_sqr/6)
        sigmap <- sigma/sqrt(3)
        sigmap_sqr <- sigmap^2
        tsqr <- sqrt(t)
        d1 <- (log(S_av/X)+ (r-qp+0.5*sigmap_sqr)*t) / (sigmap*tsqr)
        d2 <- d1 - sigmap*tsqr
        put_p <- -S_av*exp(-qp*t)*pnorm(-d1) + X*exp(-r*t)*pnorm(-d2)
        return(put_p)
}



# Asian Call (Arismatic Average)
## m1 为期权价格算术平均值的一阶矩; m2 为期权价格算术平均值的二阶矩
bs_as_aa_c <- function(S, X, r, q, sigma, t) {
        sigmasqr <- sigma^2
        tsqr <- sqrt(t)
        m1 <- S*(exp((r-q)*t) - 1) / ((r-q)*t)
        m2 <- (2*S*S*exp((2*(r-q)+sigmasqr)*t))/((r-q+sigmasqr)*(2*r - 2*q+sigmasqr)*t^2) + 2*S*S/((r-q)*t^2)*(1/(2*(r-q)+sigmasqr)-exp((r-q)*t)/(r-q+sigmasqr))
        F <- m1
        sigma_a <- 1/t * log(m2/(m1*m1))
        d1 <- (log(F/X) + (0.5*sigma_a^2)*t)/(sqrt(sigma_a)*tsqr)
        d2 <- d1 - sqrt(sigma_a)*tsqr
        c <- exp(-r*t) * (F*pnorm(d1) - X*pnorm(d2))
        return(c)
}



# Asian Put (Arismatic Average)
bs_as_aa_p <- function(S, X, r, q, sigma, t) {
        sigmasqr <- sigma^2
        tsqr <- sqrt(t)
        m1 <- S*(exp((r-q)*t) - 1) / ((r-q)*t)
        m2 <- (2*S*S*exp((2*(r-q)+sigmasqr)*t))/((r-q+sigmasqr)*(2*r - 2*q+sigmasqr)*t^2) + 2*S*S/((r-q)*t^2)*(1/(2*(r-q)+sigmasqr)-exp((r-q)*t)/(r-q+sigmasqr))
        F <- m1
        sigma_a <- 1/t * log(m2/(m1*m1))
        d1 <- (log(F/X) + (0.5*sigma_a^2)*t)/(sqrt(sigma_a)*tsqr)
        d2 <- d1 - sqrt(sigma_a)*tsqr
        p <- exp(-r*t) * (-F*pnorm(-d1) + X*pnorm(-d2))
        return(p)
}



# European Lookback Call
## Smin is the min price during t; S is current price
bs_eu_lb_c <- function(S, Smin, r, q, sigma, t) {
        sigmasqr <- sigma^2
        tsqr <- sqrt(t)
        a1 <- (log(S/Smin) + (r-q+sigmasqr/2)*t)/(sigma*tsqr)
        a2 <- a1 - sigma*tsqr
        a3 <- (log(S/Smin) + (-r+q+sigmasqr/2)*t)/(sigma*tsqr)
        Y1 <- 2 * (r-q-sigmasqr/2)*log(S/Smin)/sigmasqr
        c <- S*exp(-q*t)*pnorm(a1)-S*exp(-q*t)*(sigmasqr/(2*(r-q)))*pnorm(-a1)-Smin*exp(-r*t)*(pnorm(a2)-(sigmasqr/(2*(r-q)))*exp(Y1)*pnorm(-a3))
        return(c)
}



# European Lookback Put
## Smax is the max price during t; S is current price
bs_eu_lb_p <- function(S, Smax, r, q, sigma, t) {
        sigmasqr <- sigma^2
        tsqr <- sqrt(t)
        b1 <- (log(Smax/S) + (-r+q+sigmasqr/2)*t)/(sigma*tsqr)
        b2 <- b1 - sigma*tsqr
        b3 <- (log(Smax/S) + (r-q-sigmasqr/2)*t)/(sigma*tsqr)
        Y2 <- 2 * (r-q-sigmasqr/2)*log(Smax/S)/sigmasqr
        p <- Smax*exp(-r*t)*(pnorm(b1)-(sigmasqr/(2*(r-q)))*exp(Y2)*pnorm(-b3)) + S*exp(-q*t)*sigmasqr/(2*(r-q))*pnorm(-b2) - S*exp(-q*t)*pnorm(b2)
        return(p)
}



# European Knock-in Barriar Call
## H is barriar price; r is market yearly return; rf is risk-free yearly return
bs_eu_bar_in_c <- function(S, X, H, r, rf, q, sigma, t) {
        sigmasqr <- sigma^2
        tsqr <- sqrt(t)
        lambda <- (r - rf + 0.5*sigmasqr)/sigmasqr
        y <- (log((H*H)/(S*X))) / (sigma*tsqr)
        c <- S*exp(-q*t)*(H/S)^(2*lambda)*pnorm(y) - X*exp(-r*t)*(H/S)^(2*lambda -2)*pnorm(y-sigma*tsqr)
        return(c)
}



# European Knock-in Barriar Put
## H is barriar price; r is market yearly return; rf is risk-free yearly return
bs_eu_bar_in_p <- function(S, X, H, r, rf, q, sigma, t) {
        sigmasqr <- sigma^2
        tsqr <- sqrt(t)
        lambda <- (r - rf + 0.5*sigmasqr)/sigmasqr
        y <- (log((H*H)/(S*X))) / (sigma*tsqr)
        p <- X*exp(-r*t)*(H/S)^(2*lambda -2)*pnorm(-y+sigma*tsqr) - S*exp(-q*t)*(H/S)^(2*lambda)*pnorm(-y)
        return(p)
}


# Asset Exchange Call
## q1 is asset return for S1; give up S1 for S2; rho is correlation coefficient between S1 and S2;
bs_eu_ae_c <- function(S1, S2, q1, q2, sigma1, sigma2, rho, t) {
        sigma1sqr <- sigma1^2
        sigma2sqr <- sigma2^2
        tsqr <- sqrt(t)
        sigma <- sqrt(sigma1sqr + sigma2sqr - 2*rho*sigma1*sigma2)
        d1 <- (log(S2/S1) + (q1-q2+0.5*sigma^2)*t)/(sigma*tsqr)
        d2 <- d1 - sigma*tsqr
        c <- S2*exp(-q2*t)*pnorm(d1) - S1*exp(-q1*t)*pnorm(d2)
        return(c)
}



# Bermudan Call
## potential_et is yearly potential execution time, like c(0.25,0.5,0.75)
bt_berm_c <- function(S, X, r, q, sigma, times, potential_et, steps) {
        delta_t <- times/steps
        R <- exp(r*delta_t)
        u <- exp(sigma*sqrt(delta_t))
        d <- 1/u
        p_up <- (exp((r-q)*delta_t)-d)/(u-d)
        p_down <- 1 - p_up
        prices <- numeric(steps+1)
        call_values <- numeric(steps+1)
        potential_es <- numeric(length(potential_et))
        for (i in 1:length(potential_et)) {
                t <- potential_et[i]
                if (t>0 & t<times) {potential_es[i] <- floor(t/delta_t)}
        }
        prices[1] <- S*d^steps
        for (i in 2:(steps+1)) {prices[i] <- u^2 * prices[i-1]}
        call_values <- pmax(0, prices - X)
        for (j in steps:1) {
                check_exe <- FALSE
                if (j %in% potential_es) {check_exe <- TRUE}
                for (i in 1:j) {
                        call_values[i] <- (p_up*call_values[i+1] + p_down*call_values[i])/R
                        prices[i] <- d*prices[i+1]
                        if (check_exe) {call_values[i] <- max(call_values[i], prices[i]-X)}
                }
        }
        return(call_values[1])       
}



# Bermudan Put
bt_berm_p <- function(S, X, r, q, sigma, times, potential_et, steps) {
        delta_t <- times/steps
        R <- exp(r*delta_t)
        u <- exp(sigma*sqrt(delta_t))
        d <- 1/u
        p_up <- (exp((r-q)*delta_t)-d)/(u-d)
        p_down <- 1 - p_up
        prices <- numeric(steps+1)
        put_values <- numeric(steps+1)
        potential_es <- numeric(length(potential_et))
        for (i in 1:length(potential_et)) {
                t <- potential_et[i]
                if (t>0 & t<times) {potential_es[i] <- floor(t/delta_t)}
        }
        prices[1] <- S*d^steps
        for (i in 2:(steps+1)) {prices[i] <- u^2 * prices[i-1]}
        put_values <- pmax(0, X - prices)
        for (j in steps:1) {
                check_exe <- FALSE
                if (j %in% potential_es) {check_exe <- TRUE}
                for (i in 1:j) {
                        put_values[i] <- (p_up*put_values[i+1] + p_down*put_values[i])/R
                        prices[i] <- d*prices[i+1]
                        if (check_exe) {put_values[i] <- max(put_values[i], X-prices[i])}
                }
        }
        return(put_values[1])       
}


