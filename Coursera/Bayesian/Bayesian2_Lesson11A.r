library("rjags")

data_jags = as.list(dat)
params = c("theta", "mu", "prec", "rho")

mod_string = " model {
for (i in 1:length(y)) {
  y[i] ~ dnorm(theta[grp[i]], prec)
}

for (j in 1:max(grp)) {
  theta[j] ~ dnorm(mu, rho)
}

mu ~ dnorm(0, 1.0/1e6)
prec ~ dgamma(2.0/2.0, 2.0/2.0)
rho ~ dgamma(2.0/2, 2.0/2)

} "

mod = jags.model(textConnection(mod_string), data=data_jags, n.chains=3)
update(mod, 1e3)

mod_sim = coda.samples(model=mod,
                       variable.names=params,
                       n.iter=5e3)
mod_csim = as.mcmc(do.call(rbind, mod_sim))

plot(mod_sim)
gelman.diag(mod_sim)
autocorr.diag(mod_sim)
autocorr.plot(mod_sim)
effectiveSize(mod_sim)

(pm_params = colMeans(mod_csim))
means_theta <- pm_params[-(1:3)]
plot(means_anova)
points(means_theta, col="red")