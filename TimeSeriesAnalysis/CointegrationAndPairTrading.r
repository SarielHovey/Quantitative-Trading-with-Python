library(reticulate)
repl_python()
import tushare as ts
import pandas as pd
import numpy as np

# 基于 贵州茅台(600519.SH), 五粮液(000858.SZ), 泸州老窖(000568.SZ), 古井贡酒(000596.SZ)
DATA = pd.DataFrame()
list0 = ['600519.SH','000858.SZ','000568.SZ','000596.SZ']
for i in list0:
    df_temp = ts.pro_bar(ts_code=i, adj='qfq', start_date='20150101', end_date='20190826')
    DATA = DATA.append(df_temp)

len(DATA)
#> 4454
Coin = DATA[['ts_code','trade_date','close','pct_chg']].copy()
Coin['Date'] = pd.to_datetime(Coin.trade_date, format='%Y%m%d')
Coin.head(7)
#>     ts_code trade_date    close  pct_chg       Date
#>0  600519.SH   20190823  1130.10   2.3641 2019-08-23
#>1  600519.SH   20190822  1104.00   3.5647 2019-08-22
#>2  600519.SH   20190821  1066.00  -0.3738 2019-08-21
#>3  600519.SH   20190820  1070.00   1.3373 2019-08-20
#>4  600519.SH   20190819  1055.88   0.1214 2019-08-19
#>5  600519.SH   20190816  1054.60   0.9283 2019-08-16
#>6  600519.SH   20190815  1044.90   0.1505 2019-08-15

Close = Coin.pivot(index='Date',columns='ts_code',values='close')
Return = Coin.pivot(index='Date',columns='ts_code',values='pct_chg')
exit

# Now return to R environment and transfer the DATA
Data <- py$Coin
Cls <- py$Close; Rtn <- py$Return
# 作图对协整性做出初步判断. 可发现协整性在18年后似乎已被破坏.
plot(Cls$'600519.SH', type="l", xlim=c(0, 1133), , xlab="2015-01-01 to 2019-08-26", ylab="Daily Return in CNY", col="blue")
par(new=T)
plot(Cls$'000858.SZ', type="l", xlim=c(0, 1133), , axes=F, xlab="", ylab="", col="red")
par(new=F)

plot(Cls$'600519.SH', Cls$'000858.SZ', xlab="贵州茅台收盘价", ylab="五粮液收盘价")

pair1 <- lm(Cls$'600519.SH' ~ Cls$'000858.SZ')
pair2 <- lm(Cls$'000858.SZ' ~ Cls$'600519.SH')

summary(pair1)
#>Call:
#>lm(formula = Cls$"600519.SH" ~ Cls$"000858.SZ")
#>
#>Residuals:
#>    Min      1Q  Median      3Q     Max 
#>-173.30  -28.54  -13.17   20.07  182.54 
#>
#>Coefficients:
#>                Estimate Std. Error t value Pr(>|t|)    
#>(Intercept)     21.10473    3.54819   5.948 3.67e-09 ***
#>Cls$"000858.SZ"  8.87462    0.06136 144.631  < 2e-16 ***
#>---
#>Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
#>
#>Residual standard error: 54.3 on 1071 degrees of freedom
#>  (60 observations deleted due to missingness)
#>Multiple R-squared:  0.9513,	Adjusted R-squared:  0.9512 
#>F-statistic: 2.092e+04 on 1 and 1071 DF,  p-value: < 2.2e-16

summary(pair2)
#>Call:
#>lm(formula = Cls$"000858.SZ" ~ Cls$"600519.SH")
#>
#>Residuals:
#>     Min       1Q   Median       3Q      Max 
#>-19.4784  -1.5329   0.6384   2.2813  22.4087 
#>
#>Coefficients:
#>                 Estimate Std. Error t value Pr(>|t|)    
#>(Intercept)     0.2279112  0.3962820   0.575    0.565    
#>Cls$"600519.SH" 0.1071927  0.0007411 144.631   <2e-16 ***
#>---
#>Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
#>
#>Residual standard error: 5.968 on 1071 degrees of freedom
#>  (60 observations deleted due to missingness)
#>Multiple R-squared:  0.9513,	Adjusted R-squared:  0.9512 
#>F-statistic: 2.092e+04 on 1 and 1071 DF,  p-value: < 2.2e-16

# ADF检验的结果告诉我们:想用茅台和五粮液做Pair Trading? 洗洗睡吧
require(tseries)
adf.test(pair1$residuals, k=1)
#>	Augmented Dickey-Fuller Test
#>
#>data:  pair1$residuals
#>Dickey-Fuller = -2.4062, Lag order = 1, p-value = 0.4064
#>alternative hypothesis: stationary

adf.test(pair2$residuals, k=1)
#>	Augmented Dickey-Fuller Test
#>
#>data:  pair2$residuals
#>Dickey-Fuller = -2.2355, Lag order = 1, p-value = 0.4786
#>alternative hypothesis: stationary
