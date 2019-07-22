require(fUnitRoots)
require(xts)
q_gdp4708 <- read.csv("Z:/linshi/q-gdp4708.txt", sep="")
View(q_gdp4708)

date <- as.Date(paste(q_gdp4708$year, q_gdp4708$mon, q_gdp4708$day, sep='.'),format='%Y.%m.%d')
gdp <- xts(q_gdp4708$gdp, order.by=date)
gdp <- log(gdp)

# 取差分后去除diff_gdp中的NA值
diff_gdp <- diff(gdp)
diff_gdp[1] <- 0

# coredata()用于提取xts对象的数据区域,返回结果为矩阵
m1 <- ar(coredata(diff_gdp)[,1], method = 'mle')
m1$order
#>[1] 9

# 对数化gdp随时间近乎直线增加
plot(gdp)

# 对数化gdp一阶差分围绕某个不为0的水平波动
plot(diff_gdp)

# 对数化gdp的ACF图显示滞后20项时,自回归系数仍>0.8, 呈现高度自相关性
acf(gdp, lag=20)
# 对对数化gdp一阶差分的PACF图
pacf(diff_gdp, lag=20)

# 对一阶差分的ar回归中, AIC选择了AR(9)模型,因而对原数据进行DF检验时选择>9的滞后项
# 对对数化GDP数据进行DF单位根检验,发现在10项滞后项时无法拒绝H0
# H0: 回归系数\beta_1 = 1; H1: \beta_1 < 1
adfTest(gdp, lags=10, type=c("c"))
#>Title:
#> Augmented Dickey-Fuller Test

#>Test Results:
#>  PARAMETER:
#>    Lag Order: 10
#>  STATISTIC:
#>    Dickey-Fuller: -1.6109
#>  P VALUE:
#>    0.4569 
#>Description:
#> Mon Jul 22 10:22:34 2019 by user: sariel


