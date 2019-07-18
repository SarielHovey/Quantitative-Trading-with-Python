da <- m.ibm3dx2608 <- read.csv("Z:/linshi/m-ibm3dx2608.txt", sep="")
da[1,]
#>      date    ibmrtn    vwrtn    ewrtn    sprtn
#>1 19260130 -0.010381 0.000724 0.023174 0.022472

da$date <- as.Date(as.character(da$date), format='%Y%m%d')

require(xts)
vw <- xts(da$vwrtn, order.by = da$date)

m3 <- arima(vw,order=c(3,0,0))
#>Call:
#>arima(x = vw, order = c(3, 0, 0))

#>Coefficients:
#>         ar1      ar2      ar3  intercept
#>      0.1158  -0.0187  -0.1042     0.0089
#>s.e.  0.0315   0.0317   0.0317     0.0017

#>sigma^2 estimated as 0.002875:  log likelihood = 1500.86,  aic = -2991.73

## 对m3回归的余值进行自相关检验,滞后项12期
## p值显示在0.05的置信水平下无法拒绝余值的12项滞后期系数均为0的原假设
Box.test(m3$residuals, lag=12, type = 'Ljung')
#>	Box-Ljung test
#>data:  m3$residuals
#>X-squared = 16.352, df = 12, p-value = 0.1756

## 由于m3使用了3项滞后项,因此再考虑9个自由度下的卡方检验的p值
## 同样无法拒绝H0
pv <- 1-pchisq(16.352, 9)
#>[1] 0.05988496

## 注意到系数ar2的值接近0, 并不显著, 予以修正
m3 <- arima(vw, order=c(3,0,0), fixed = c(NA,0,NA,NA))
#>Call:
#>arima(x = vw, order = c(3, 0, 0), fixed = c(NA, 0, NA, NA))

#>Coefficients:
#>         ar1  ar2      ar3  intercept
#>      0.1136    0  -0.1063     0.0089
#>s.e.  0.0313    0   0.0315     0.0017
#>sigma^2 estimated as 0.002876:  log likelihood = 1500.69,  aic = -2993.38

Box.test(m3$residuals, lag=12, type = 'Ljung')
#>	Box-Ljung test

#>data:  m3$residuals
#>X-squared = 16.828, df = 12, p-value = 0.1562

1-pchisq(16.828, 10)
#>[1] 0.0782576
## 显然,去除二阶滞后项有效


