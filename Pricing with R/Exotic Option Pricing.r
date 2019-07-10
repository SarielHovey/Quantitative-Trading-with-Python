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




