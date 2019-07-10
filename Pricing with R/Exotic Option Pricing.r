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
        sigma_sqr <- sigma^2
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







