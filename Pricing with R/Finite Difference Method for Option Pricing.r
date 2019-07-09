# Explicit Finite Difference Method for European Call
## $ f_{i,j} = a_j*f_{i+1,j-1} + b_j*f_{i+1,j} +c_j*f_{i+1,j+1} $
ef_eu_c <- function(S, X, r, q, sigma, t, price_step, t_step) {
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
        for (i in 2:M) {
                a[i] <- -0.5*(r-q)*(i-1)*delta_t + 0.5*sigma_square*(i-1)^2*delta_t
                b[i] <- 1-r*delta_t-sigma_square*(i-1)^2*delta_t
                c[i] <- 0.5*(r-q)*(i-1)*delta_t + 0.5*sigma_square*(i-1)^2*delta_t
        }
        f_next <- numeric(M+1)
        f_next <- pmax(0, S_values - X)
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
ef_eu_p <- function(S, X, r, q, sigma, t, price_step, t_step) {
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
        for (i in 2:M) {
                a[i] <- -0.5*(r-q)*(i-1)*delta_t + 0.5*sigma_square*(i-1)^2*delta_t
                b[i] <- 1-r*delta_t-sigma_square*(i-1)^2*delta_t
                c[i] <- 0.5*(r-q)*(i-1)*delta_t + 0.5*sigma_square*(i-1)^2*delta_t
        }
        f_next <- numeric(M+1)
        f_next <- pmax(0, X - S_values)
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
## $ a_j*f_{i,j-1} + b_j*f_{i,j} + c_j*f_{i,j+1} = f_{i+1,j} $
if_eu_c <- function(S, X, r, q, sigma, t, price_step, t_step) {
        sigma_square <- sigma^2
        M <- numeric(1)
        if ((price_step %% 2)==1) M <- price_step +1 else M <- price_step
        delta_S <- 2*S/M
        S_values <- numeric(M+1)
        for (i in 1:(M+1)) {
                S_values[i] <- (i-1)*delta_S
        }
        N <- t_step
        delta_t <- t/N
        A <- matrix(0, M+1, M+1)
        A[1,1] <- 1
        for (i in 2:M) {
                A[i,i-1] <- 0.5*i*delta_t*(r-sigma_square*i)
                A[i,i] <- 1 + delta_t*(r+sigma_square*i^2)
                A[i,i+1] <- 0.5*i*delta_t*(-r-sigma_square*i)
        }
        A[M+1,M+1] <- 1
        B <- matrix(0, M+1, 1)
        for (i in 1:(M+1)) {
                B[i,1] <- max(0, S_values[i] - X)
        }
        F <- solve(A) %*% B
        for (j in (N-1):1) {
                B <- F
                F <- solve(A) %*% B
        }
        return(F[M/2 +1, 1])
}








# Implicit Finite Difference Method for European Put
if_eu_p <- function(S, X, r, q, sigma, t, price_step, t_step) {
        sigma_square <- sigma^2
        M <- numeric(1)
        if ((price_step %% 2)==1) M <- price_step +1 else M <- price_step
        delta_S <- 2*S/M
        S_values <- numeric(M+1)
        for (i in 1:(M+1)) {
                S_values[i] <- (i-1)*delta_S
        }
        N <- t_step
        delta_t <- t/N
        A <- matrix(0, M+1, M+1)
        A[1,1] <- 1
        for (i in 2:M) {
                A[i,i-1] <- 0.5*i*delta_t*(r-q-sigma_square*i)
                A[i,i] <- 1 + delta_t*(r+sigma_square*i^2)
                A[i,i+1] <- -0.5*i*delta_t*(r-q+sigma_square*i)
        }
        A[M+1,M+1] <- 1
        B <- matrix(0, M+1, 1)
        for (i in 1:(M+1)) {
                B[i,1] <- max(0, X - S_values[i])
        }
        F <- solve(A) %*% B
        for (j in (N-1):1) {
                B <- F
                F <- solve(A) %*% B
        }
        return(F[M/2 +1, 1])
}

