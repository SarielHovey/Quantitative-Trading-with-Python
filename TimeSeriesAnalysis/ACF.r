# Portmanteau Test(混成检验) for ACF(样本自相关系数)
da <- m.ibm3dx2608 <- read.csv("Z:/linshi/m-ibm3dx2608.txt", sep="")
da[1,]
#>      date    ibmrtn    vwrtn    ewrtn    sprtn
#>1 19260130 -0.010381 0.000724 0.023174 0.022472

da$date <- as.Date(as.character(da$date), format='%Y%m%d')
head(da$date)
#>[1] "1926-01-30" "1926-02-27" "1926-03-31" "1926-04-30" "1926-05-28" "1926-06-30"

sibm <- xts(da$ibmrtn, order.by = da$date)
head(sibm)
#>                [,1]
#>1926-01-30 -0.010381
#>1926-02-27 -0.024476
#>1926-03-31 -0.115591
#>1926-04-30  0.089783

## 使用Ljung-Box检验多个自相关系数是否均为0
## m for lag in Box.test should be around ln(T); T is the total number of sample
## H0: all ACF in m are 0
Box.test(sibm, lag=5, type = 'Ljung-Box')
#>	Box-Ljung test

#>data:  sibm
#>X-squared = 3.3682, df = 5, p-value = 0.6434

Box.test(sibm, lag=10, type = 'Ljung-Box')
#>	Box-Ljung test

#>data:  sibm
#>X-squared = 13.99, df = 10, p-value = 0.1734

libm <- log(1+sibm)
Box.test(libm, lag = 10, type = 'Ljung-Box')
#>	Box-Ljung test

#>data:  libm
#>X-squared = 13.386, df = 10, p-value = 0.2029

Box.test(sibm, lag=5, type = 'Ljung-Box')
#>	Box-Ljung test

#>data:  sibm
#>X-squared = 3.3682, df = 5, p-value = 0.6434

