from rpy2 import robjects
r = robjects.r

# AR(1)
str = """
x <- w <- rnorm(100)
for (t in 2:100) {x[t] <- 0.6*x[t-1] + w[t]}
setwd("D:/Quant/qs_sat/advance/")
jpeg(file='Rplot.jpg')
layout(1:2)
plot(x,type='l')
acf(x)
dev.off()
"""
r(str)
r('x.ar <- ar(x, method = "mle")')
tuple([r('x.ar$order'), r('x.ar$ar')])
#> 1, 0.598158
r('x.ar$ar + c(-1.96, 1.96)*sqrt(x.ar$asy.var)')
#> [0.430881, 0.747436]


# AR(2)
str = """
x <- w <- rnorm(100)
for (t in 3:100) {x[t] <- 0.77*x[t-1] -0.43*x[t-2] + w[t]}
setwd("D:/Quant/qs_sat/advance/")
jpeg(file='Rplot.jpg')
layout(1:2)
plot(x,type='l')
acf(x)
dev.off()
"""
r(str)
r('x.ar <- ar(x, method="mle")')
r('x.ar$order')[0], list(r('x.ar$ar'))
#> (2, [0.715382953301904, -0.42252601934217004])
str = """
setwd("D:/Quant/qs_sat/advance/")
jpeg(file='Rplot.jpg')
acf(x.ar$resid, na.action=na.omit)
dev.off()
"""
r(str)

# Financial Data
r("ubs <- read.csv('UBS.csv',sep=',',header=TRUE)")
list(r('colnames(ubs)'))
#> ['Date', 'Open', 'High', 'Low', 'Close', 'Adj.Close', 'Volume']
r("names(ubs) <- c('Date','Op','Hi','Lo','Cl','Ad','Vo')")
str = """
setwd("D:/Quant/qs_sat/advance/")
jpeg(file='Rplot.jpg')
plot(ubs$Cl,type='l')
dev.off()
"""
r(str)
r('ubsrt <- diff(log(ubs$Cl))')
r("""
setwd("D:/Quant/qs_sat/advance/")
jpeg(file='Rplot.jpg')
plot(ubsrt,type='l')
dev.off()
""")
r("""
setwd("D:/Quant/qs_sat/advance/")
jpeg(file='Rplot.jpg')
acf(ubsrt, na.action=na.omit)
dev.off()
""")
r("ubs.ar <- ar(ubsrt, na.action=na.omit)")
r('ubs.ar$order')[0], list(r('ubs.ar$ar'))
#> (1, [-0.08191877603479637])
r("""
jpeg(file='Rplot.jpg')
acf(ubs.ar$resid, na.action=na.omit)
dev.off()
""")
r('ubs.ar$asy.var')
#> [0.000389]
r('-0.081919 + c(-1.96, 1.96)*sqrt(0.000389)')
#> [-0.120576, -0.043262] Confidence Interval doesnt include 0, ar1 is more trustworthy


# MA(1)
str = """
x <- w <- rnorm(100)
for (t in 2:100) {x[t] <- w[t] + 0.6*w[t-1]}
"""
r(str)
x_ma = r('x.ma <- arima(x, order=c(0,0,1))')
#> [0.5939098442993538, 0.08514836477533867] ma1 and intercept
#> AIC: 270.864588


# Financial Data
str = """
ubs <- read.csv('UBS.csv',sep=',',header=TRUE)
names(ubs) <- c('Date','Op','Hi','Lo','Cl','Ad','Vo')
ubsrt <- diff(log(ubs$Cl))
plot(ubsrt, type='l')
acf(ubsrt)
ubsrt.ma <- arima(ubsrt, order=c(0,0,2))
acf(ubsrt.ma$res)
"""
r(str)


# ARIMA(1,1)
str = """
x <- arima.sim(n=1000, model=list(ar=0.5, ma=-0.5))
plot(x)
acf(x)
x.ma <- arima(x, order=c(1,0,1))
acf(x.ma$resid)
"""
r(str)


# Choose the best ARMA model
str = """
x <- arima.sim(n=1000, model=list(ar=c(0.5, -0.25, 0.4), ma=c(0.5, -0.3)))
final.aic <- Inf
final.order <- c(0,0,0)
for (i in 0:4) for (j in 0:4) {
    current.aic <- AIC(arima(x, order=c(i, 0, j)))
    if (current.aic < final.aic) {
        final.aic <- current.aic
        final.order <- c(i, 0, j)
        final.arma <- arima(x, order=final.order)
        }}
final.order
"""
r(str)
#> 3 0 2
r("Box.test(final.arma$resid, lag=20, type='Ljung-Box')")
#>        Box-Ljung test
#> H0:No autocorrelation
#> data:  final.arma$resid
#> X-squared = 25.558, df = 20, p-value = 0.1809


# Financial Data
str = """
final.aic <- Inf
final.order <- c(0,0,0)
for (i in 0:4) for (j in 0:4) {
    current.aic <- AIC(arima(ubsrt, order=c(i, 0, j)))
    if (current.aic < final.aic) {
        final.aic <- current.aic
        final.order <- c(i, 0, j)
        final.arma <- arima(ubsrt, order=final.order)
        }}
Box.test(final.arma$resid, lag=20, type='Ljung-Box')
"""
r(str)
#>Coefficients:
#>         ar1      ar2      ar3      ar4      ma1     ma2     ma3  intercept
#>      0.0063  -0.2509  -0.8302  -0.0481  -0.0899  0.2685  0.7791     -2e-04
#>s.e.  0.1781   0.1242   0.1452   0.0354   0.1761  0.1477  0.1637      4e-04
#>
#>sigma^2 estimated as 0.0004227:  log likelihood = 6303.99,  aic = -12589.99
#>
#>        Box-Ljung test
#>
#>data:  final.arma$resid
#>X-squared = 19.485, df = 20, p-value = 0.4905