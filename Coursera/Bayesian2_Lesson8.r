mod1_string = " model {
    for (i in 1:length(y)) {
        y[i] ~ dnorm(mu[grp[i]], prec[grp[i]])
    }
    
    for (j in 1:3) {
        mu[j] ~ dnorm(0.0, 1.0/1.0e6)
    }
    
    for (k in 1:3) {
        prec[k] ~ dgamma(5/2.0, 5*1.0/2.0)
    }
    
    sig = sqrt( 1.0 / prec )
} "

inits1 = function() {
    inits = list("mu"=rnorm(3,0.0,100.0), "prec"=rgamma(3,1.0,1.0))
}

mod1 = jags.model(textConnection(mod1_string), data=data_jags, inits=inits1, n.chains=3)

mod1_sim = coda.samples(model=mod1,
                        variable.names=params,
                        n.iter=5e3)
                        
mod1_csim = as.mcmc(do.call(rbind, mod1_sim))