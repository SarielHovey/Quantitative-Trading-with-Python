from rpy2 import robjects
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn')

r = robjects.r

str = """
set.seed(1)
x <- seq(1,100) + 20.0*rnorm(1:100)
"""
x = list(r(str))

str = """
set.seed(2)
y <- seq(1,100) + 20.0*rnorm(1:100)
"""
y = list(r(str))
plt.scatter(x,y)
plt.show()

# Calculate Covariance
r("cov(x,y)")[0]
# 681.6858560619356

# Calculate Sample Correlation
r("cor(x,y)")[0]
# 0.5796604285173594

# Correlogram
str = """
setwd("D:/Quant/qs_sat/advance/")
jpeg(file='Rplot.jpg')
set.seed(1)
w <- rnorm(100)
acf(w)
dev.off()
"""
r(str)

# Fixed Linear Trend ACF
str = """
setwd("D:/Quant/qs_sat/advance/")
jpeg(file='Rplot.jpg')
w <- seq(1, 100)
acf(w)
dev.off()
"""
r(str)

# Repeated Sequence ACF
str = """
setwd("D:/Quant/qs_sat/advance/")
jpeg(file='Rplot.jpg')
w <- rep(1:10, 10)
acf(w)
dev.off()
"""
r(str)