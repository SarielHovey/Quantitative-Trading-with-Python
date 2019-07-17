# AR(3) Model for US GNP

library(xts)
gnp_us <- scan(file='Z:/linshi/dgnp82.txt')

gnp1 <- ts(gnp_us, frequency=4, start=c(1947,2))
gnp1 <- as.xts(gnp1)
head(gnp1)
#>           [,1]
#>1947 Q2 0.00632
#>1947 Q3 0.00366
#>1947 Q4 0.01202
#>1948 Q1 0.00627
#>1948 Q2 0.01761
#>1948 Q3 0.00918

## 对gnp1绘制时间折线图, show pattern of sin() and cos()
## This infers Complex Characteristic Root for AR model
## For AR model with Real Characteristic Root, pattern of Exponential function is shown
plot(gnp1)
points(gnp1, pch='*')

m1 <- ar(gnp_us, method = 'mle')
#>Call:
#>ar(x = gnp_us, method = "mle")

#>Coefficients:
#>      1        2        3  
#> 0.3480   0.1793  -0.1423  

#>Order selected 3  sigma^2 estimated as  9.427e-05

## Based on AIC value, lag=3 is selected for this AR model
m1$order
#>[1] 3

m2 <- arima(gnp_us, order=c(3,0,0))
#>Call:
#>arima(x = gnp_us, order = c(3, 0, 0))

#>Coefficients:
#>         ar1     ar2      ar3  intercept
#>      0.3480  0.1793  -0.1423     0.0077
#>s.e.  0.0745  0.0778   0.0745     0.0012

#sigma^2 estimated as 9.427e-05:  log likelihood = 565.84,  aic = -1121.68

## As intercept here is the mean of the series, hense Constant Term is:
(1 - .348- .1793-+.1423)*0.0077
#>[1] 0.0047355

## Use sigma^2 to get Residual Standard Error
m2_std <- sqrt(m2$sigma2)
#>[1] 0.009709322

## Initialize a vector for Equation from AR model
p1 <- c(1,-m2$coef[1:3])
## Solve the Equation and we get 3 Complex Roots
roots <- polyroot(p1)
roots
#>[1]  1.590253+1.063882i -1.920152+0.000000i  1.590253-1.063882i

## 求3个复数根的模(Model)
Mod(roots)
#>[1] 1.913308 1.920152 1.913308

# Assume cos(), compute the average Business Cycle
gnp_us_bcyc <- 2*pi / acos(1.590253/1.913308)
#>[1] 10.65638


