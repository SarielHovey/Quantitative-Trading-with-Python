mod1_string = " model {
    for (i in 1:length(numvisit)) {
        numvisit[i] ~ dpois(lam[i])
        log(lam[i]) = int + b_badh*badh[i] + b_age*age[i]
    }
    
    int ~ dnorm(0.0, 1.0/1e6)
    b_badh ~ dnorm(0.0, 1.0/1e4)
    b_age ~ dnorm(0.0, 1.0/1e4)
} "

params1 = c("int", "b_badh", "b_age")

mod1 = jags.model(textConnection(mod1_string), data=data_jags, n.chains=3)

update(mod1, 1e3)

mod1_sim = coda.samples(model=mod1,
                        variable.names=params1,
                        n.iter=5e3)
                        
mod1_csim = as.mcmc(do.call(rbind, mod1_sim))

dic1 = dic.samples(mod1, n.iter=1e3)

---------------------------------------------------------------

dat = read.csv(file="callers.csv", header=TRUE)
dat2_jags = as.list(dat)

mod2_string = " model {
    for (i in 1:length(calls)) {
		calls[i] ~ dpois( days_active[i] * lam[i] )
		log(lam[i]) = b0 + b[1]*age[i] + b[2]*isgroup2[i]
	}
    
    b0 ~ dnorm(0.0, 1.0/1e2)
    b[1] ~ dnorm(0.0, 1.0/1e2)
    b[2] ~ dnorm(0.0, 1.0/1e2)

} "

params2 = c("b0", "b")

mod2 = jags.model(textConnection(mod2_string), data=dat2_jags, n.chains=3)

update(mod2, 1e3)

mod2_sim = coda.samples(model=mod2,
                        variable.names=params2,
                        n.iter=5e3)
                        
mod2_csim = as.mcmc(do.call(rbind, mod2_sim))

gelman.diag(mod2_sim)
autocorr.diag(mod2_sim)
autocorr.plot(mod2_sim)

mean(mod2_csim[,2] > 0) # Prob of b[2]>0

(pmean_coef = apply(mod2_csim, 2, mean))

llam_hat = pmean_coef["b0"] + X %*% pmean_coef[c("b[2]","b[1]")]
lam_hat = exp(llam_hat)
resid = dat$calls - lam_hat*dat$days_active
