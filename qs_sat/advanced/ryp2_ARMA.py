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
r('x.ma <- arima(x, order=c(0,0,1))')
#> [0.5939098442993538, 0.08514836477533867] ma1 and intercept
#> AIC: 270.864588