# Use arima.sim() to generate data for ARIMA model
# order = c(2,1,2) means MA(2) and AR(2), plus differenced 1 time
x <- arima.sim(list(order = c(2,1,2), ar = c(0.6,-0.4), ma=c(-0.5,-1)), n = 10000)
plot(x)


# Now run arima() for regression
## Obviously, we have good estimate for AR part, but the regression works badly on MA part
x_reg <- arima(x,order = c(2,1,2))
x_reg
#>Call:
#>arima(x = x, order = c(2, 1, 2))
#>
#>Coefficients:
#>         ar1      ar2     ma1      ma2
#>      0.5951  -0.4064  0.0126  -0.6053
#>s.e.  0.0117   0.0112  0.0106   0.0107
#>
#>sigma^2 estimated as 1.657:  log likelihood = -16715,  aic = 33440.01

## Check for trust-intervals of MA part
## Obviously, (-0.5,-1) not included
0.0126 + c(-1.96,1.96)*0.0106
#>[1] -0.008176  0.033376
-0.6053 + c(-1.96,1.96)*0.0107
#>[1] -0.626272 -0.584328


# Check the ACF plot for x_arima
acf(resid(x_reg))
# Run Ljung-Box test on resid of x_reg
## At a lag of 40, the resid passes Ljung-Box test, we accept the H0: no Autoregression with lag of 40
## But we know x_reg is wrong on MA part
## This story tells us, even a regression looks good and passes tests, it may still be wrong
Box.test(resid(x_reg), lag=40, type="Ljung-Box")
#>
#>	Box-Ljung test
#>
#>data:  resid(x_reg)
#>X-squared = 34.46, df = 40, p-value = 0.7174

