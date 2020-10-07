library("rjags")
library("car")
data("Anscombe")

mod_string = " model {
    for (i in 1:length(education)) {
        education[i] ~ dnorm(mu[i], prec)
        mu[i] = b[1]*income[i] + b[2]*young[i] + b[3]*urban[i]
    }
    
    for (i in 1:3) {
        b[i] ~ ddexp(0.0, 1.0)
    }
    
    prec ~ dgamma(1.0/2.0, 1.0*1500.0/2.0)
    	## Initial guess of variance based on overall
    	## variance of education variable. Uses low prior
    	## effective sample size. Technically, this is not
    	## a true 'prior', but it is not very informative.
    sig2 = 1.0 / prec
    sig = sqrt(sig2)
} "

params = c("b","sig")

mod_sim = coda.samples(model=mod,
                        variable.names=params,
                        n.iter=5e3)
-------------------------------------------------------------------                        
mod0_string = " model {
    for (i in 1:length(education)) {
        education[i] ~ dnorm(mu[i], prec)
        mu[i] = b0 + b[1]*income[i] + b[2]*young[i] + b[3]*urban[i]
    }
    
    b0 ~ dnorm(0.0, 1.0/1.0e6)
    for (i in 1:3) {
        b[i] ~ dnorm(0.0, 1.0/1.0e6)
    }
    
    prec ~ dgamma(1.0/2.0, 1.0*1500.0/2.0)
    	## Initial guess of variance based on overall
    	## variance of education variable. Uses low prior
    	## effective sample size. Technically, this is not
    	## a true 'prior', but it is not very informative.
    sig2 = 1.0 / prec
    sig = sqrt(sig2)
} "

mod0 = jags.model(textConnection(mod0_string), data=data_jags, n.chains=3)

params0 = c("b0","b","sig")

mod0_sim = coda.samples(model=mod0,
                        variable.names=params0,
                        n.iter=5e3)
------------------------------------------------------------------

data("warpbreaks")

mod4_string = " model {
    for( i in 1:length(y)) {
        y[i] ~ dnorm(mu[woolGrp[i], tensGrp[i]], prec[woolGrp[i], tensGrp[i]])
    }
    
    for (j in 1:max(woolGrp)) {
        for (k in 1:max(tensGrp)) {
            mu[j,k] ~ dnorm(0.0, 1.0/1.0e6)
        }
    }
    
    for (j in 1:max(woolGrp)) {
        for (k in 1:max(tensGrp)) {
            prec[j,k] ~ dgamma(1.0/2.0,1.0*1.0/2.0)
        }
    }
    
    sig = sqrt(1.0 / prec)
} "

data3_jags = list(y=log(warpbreaks$breaks), woolGrp=as.numeric(warpbreaks$wool), tensGrp=as.numeric(warpbreaks$tension))

params3 = c("mu", "sig")

mod4 = jags.model(textConnection(mod4_string), data=data3_jags, n.chains=3)

update(mod4, 1e3)

mod4_sim = coda.samples(model=mod4,
                        variable.names=params3,
                        n.iter=5e3)
                        
mod4_csim = as.mcmc(do.call(rbind, mod3_sim))

plot(mod4_sim, ask=TRUE)
gelman.diag(mod4_sim)
autocorr.diag(mod4_sim)
effectiveSize(mod4_sim)
raftery.diag(mod4_sim)

(dic4 = dic.samples(mod4, n.iter=1e3))

