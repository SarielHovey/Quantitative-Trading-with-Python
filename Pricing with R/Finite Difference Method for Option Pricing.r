# Explicit Finite Difference Method for European Call
ef_eu_c <- function(S, X, r, sigma, t, price_step, t_step) {
        sigma_square <- sigma^2
        M <- numeric(1)
        if ((price_step %% 2)==1) M <- price_step +1 else M <- price_step
        delta_S <- 2*S/M
        S_values <- numeric(M+1)
        for (i in 1:(M+1)) {
                S_values[i] <- (i-1) * delta_S
        }
        N <- t_step
        delta_t <- t/N
        a <- numeric(M)
        b <- numeric(M)
        c <- numeric(M)
        r1 <- 1/(1 + r*delta_t)
        r2 <- delta_t/(1 + r*delta_t)
        for (i in 2:M) {
                a[i] <- r2*0.5*(i-1)*(-r+sigma_square*(i-1))
                b[i] <- r1*(1-sigma_square*(i-1)^2 *delta_t)
                c[i] <- r2*0.5*(i-1)*(r+sigma_square*(i-1))
        }
        f_next <- numeric(M+1)
        for(i in 1:(M+1)) {
                f_next[i] <- max(0,S_values[i]-X)
        }
        f <- numeric(M+1)
        for(j in N:1) {
                f[1] <- 0
                for(i in 2:M) {
                        f[i] <- a[i]*f_next[i-1] + b[i]*f_next[i] + c[i]*f_next[i+1]
                }
                f[M+1] <- 0
                for(i in 1:(M+1)) {
                        f_next[i] <- f[i]
                }
        }
        return(f[M/2 +1])
}



# Explicit Finite Difference Method for European Put
ef_eu_p <- function(S, X, r, sigma, t, price_step, t_step) {
        sigma_square <- sigma^2
        M <- numeric(1)
        if ((price_step %% 2)==1) M <- price_step +1 else M <- price_step
        delta_S <- 2*S/M
        S_values <- numeric(M+1)
        for (i in 1:(M+1)) {
                S_values[i] <- (i-1) * delta_S
        }
        N <- t_step
        delta_t <- t/N
        a <- numeric(M)
        b <- numeric(M)
        c <- numeric(M)
        r1 <- 1/(1 + r*delta_t)
        r2 <- delta_t/(1 + r*delta_t)
        for (i in 2:M) {
                a[i] <- r2*0.5*(i-1)*(-r+sigma_square*(i-1))
                b[i] <- r1*(1-sigma_square*(i-1)^2 *delta_t)
                c[i] <- r2*0.5*(i-1)*(r+sigma_square*(i-1))
        }
        f_next <- numeric(M+1)
        for(i in 1:(M+1)) {
                f_next[i] <- max(0, X-S_values[i])
        }
        f <- numeric(M+1)
        for(j in N:1) {
                f[1] <- X
                for(i in 2:M) {
                        f[i] <- a[i]*f_next[i-1] + b[i]*f_next[i] + c[i]*f_next[i+1]
                }
                f[M+1] <- 0
                for(i in 1:(M+1)) {
                        f_next[i] <- f[i]
                }
        }
        return(f[M/2 +1])
}



# Implicit Finite Difference Method for European Call






# Implicit Finite Difference Method for European Put


