# 1-period state price
# $\pi_u$ is the current price of standard asset 'm' whose 1-period future price is 1 or 0
# $\pi_u$ is the current price of standard asset 'n' whose 1-period future price is 0 or 1
# Obviously, we have $ P_A = \pi_u u P_A + \pi_d d P_A$ due to Arbitrage Free Pricing
# Obviously, we can conclude that $ \pi_u * u + \pi_d * d = 1 $--(1)

# If we long 1 m and 1 n, then we will have future value 1 at period 1
# Obviously, we can conclude that $ \pi_u + \pi_d = e^{-r_f} $--(2)

# Get (1) and (2) together, we have
# $\pi_u = (1 - d*e^{-r_f}) / (u - d)$
# $\pi_d = (u*e^{-r_f} - 1) / (u - d)$

pbz <- function(rf, u, d, upb, dpb){
    paiu = (1 - d*exp(-rf)) / (u - d)
    paid = exp(-rf) - paiu
    pb = paiu*upb + paid*dpb
    return(pb)
}
# pb is the spot price of required symbol; upb is the up price of pb at period 1; dpb is the down price of pb at T_1

pbz_paiu <- function(rf, u, d, upb, dpb){
    paiu = (1 - d*exp(-rf)) / (u - d)
    return(paiu)
    }

pbz_paid <- function(rf, u, d, upb, dpb){
    paid = (u*exp(-rf) - 1) / (u - d)
    return(paid)
    }
# paiu and paid are the amout used to syntheic pb
