da <- read.csv("Z:/linshi/m-deciles08.txt", sep="", stringsAsFactors=FALSE)
class(da$date)
#> [1] "integer"
da$date <- as.character(da$date)
da$date <- as.Date(da$date, format='%Y%m%d')

head(da)
#>        date   CAP1RET   CAP2RET   CAP9RET  CAP10RET
#>1 1970-01-30  0.054383 -0.004338 -0.073082 -0.076874
#>2 1970-02-27  0.020264  0.020155  0.064185  0.059512
#>3 1970-03-31 -0.031790 -0.028090 -0.004034 -0.001327
#>4 1970-04-30 -0.184775 -0.193004 -0.115825 -0.091112
#>5 1970-05-29 -0.088189 -0.085342 -0.085565 -0.053193
#>6 1970-06-30 -0.059476 -0.085212 -0.046605 -0.048133

d1 <- da[,2]
names(d1) <- da$date
# Create dummy variable for January
jan <- rep(c(1, rep(0,11)),39)
m1 <- lm(d1 ~ jan)
summary(m1)
#>Call:
#>lm(formula = d1 ~ jan)
#>
#>Residuals:
#>     Min       1Q   Median       3Q      Max 
#>-0.30861 -0.03475 -0.00176  0.03254  0.40671 
#>
#>Coefficients:
#>            Estimate Std. Error t value Pr(>|t|)    
#>(Intercept) 0.002864   0.003333   0.859    0.391    
#>jan         0.125251   0.011546  10.848   <2e-16 ***
#>---
#>Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
#>
#>Residual standard error: 0.06904 on 466 degrees of freedom
#>Multiple R-squared:  0.2016,	Adjusted R-squared:  0.1999 
#>F-statistic: 117.7 on 1 and 466 DF,  p-value: < 2.2e-16



m2 <- arima(d1, order=c(1,0,0),seasonal = list(order=c(1,0,1),period=12))
m2
#>Coefficients:
#>         ar1    sar1     sma1  intercept
#>      0.1769  0.9882  -0.9144     0.0118
#>s.e.  0.0456  0.0093   0.0335     0.0129
#>
#>sigma^2 estimated as 0.004717:  log likelihood = 584.07,  aic = -1158.14
tsdiag(m2, gof=36)

