from rpy2 import robjects
r = robjects.r

str = """
setwd("D:/Quant/qs_sat/advance/")
UBS <- read.csv('UBS.csv',sep=',',header=TRUE)
CS <- read.csv('CS.csv',sep=',',header=TRUE)
UBS <- UBS[order(UBS$timestamp),]
CS <- CS[order(CS$timestamp),]
"""
r(str)

str = """
UBSadj = UBS$adjusted_close
CSadj = CS$adjusted_close
plot(UBSadj, type='l', xlim=c(0,1500),ylim=c(5.0, 27.0),xlab='2014-11-21 to 2020-03-12', ylab = 'UBS.NYSE and CS.NYSE Price in USD', col='blue')
par(new=T)
plot(CSadj, type='l', xlim=c(0,1500),ylim=c(5.0, 27.0),xlab='', ylab = '', col='red')
par(new=F)
legend('topright', legend=c('UBS.NYSE', 'CS.NYSE'))
"""
r(str)

str = """
plot(UBSadj,CSadj, xlab='UBS Forward-Adjusted Prices', ylab='CS Forward-Adjusted Prices')
"""
r(str)

r('comb1 <- lm(UBSadj~CSadj)')
r('comb2 <- lm(CSadj~UBSadj)')
r("plot(comb1$resid, type='l', xlab='2014-11-21 to 2020-03-12', ylab='Residuals of UBSadj~CSadj')")
r("plot(comb2$resid, type='l', xlab='2014-11-21 to 2020-03-12', ylab='Residuals of CSadj~UBSadj')")
r('library(tseries)')
r('adf.test(comb1$resid, k=1)')
r('adf.test(comb2$resid, k=1)') # None of the 2 has stationary residuals