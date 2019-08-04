# require(reticulate)
library(reticulate)
repl_python()
import pandas as pd
import datetime as dt


# Import Data for HS300
HS300 = pd.read_csv("D:/R_Quant/DATA_HS300.csv",encoding='UTF8',dtype={'trade_date':str, 'ts_code':str})
Bench = pd.read_csv("D:/R_Quant/Benchmark_HS300.csv",encoding='UTF8',dtype={'trade_date':str, 'ts_code':str})
Factor = pd.read_csv("D:/R_Quant/DATA_HS300_Factors.csv",encoding='UTF8',dtype={'trade_date':str, 'ts_code':str})
IR = pd.read_csv("D:/R_Quant/DATA_InterestRate.csv",encoding='UTF8',dtype={'date':str})

Mkt = tushare.pro_bar(ts_code='000906.SH', asset='I', start_date='20100101', end_date='20190802')

len(HS300.trade_date) == len(Factor.trade_date)
#> True
DATA_temp = pd.merge(HS300, Factor)
del([HS300, Factor])
# Use copy() to avoid unnecessary modify to DATA_temp
DATA = DATA_temp[['ts_code','trade_date','pct_chg','pb','circ_mv']].copy()
DATA['Date'] = pd.to_datetime(DATA.trade_date, format='%Y%m%d')
DATA.head(6)
#>     ts_code trade_date  pct_chg      pb    circ_mv       Date
#>0  000596.SZ   20190802   1.4777  7.8411  4557168.0 2019-08-02
#>1  000596.SZ   20190801  -1.6962  7.7270  4490805.2 2019-08-01
#>2  000596.SZ   20190731  -2.0319  7.8603  4568292.4 2019-07-31
#>3  000596.SZ   20190730   0.6208  8.0233  4663041.6 2019-07-30
#>4  000596.SZ   20190729   0.6666  7.9738  4634271.6 2019-07-29
#>5  000596.SZ   20190726   0.5361  7.9210  4603583.6 2019-07-26

Bchmk = Bench[['ts_code','trade_date','pct_chg']].copy()
Bchmk['Date'] = pd.to_datetime(Bchmk.trade_date, format='%Y%m%d')
Bchmk.head(6)
#>     ts_code trade_date  pct_chg       Date
#>0  000300.SH   20190802  -1.4732 2019-08-02
#>1  000300.SH   20190801  -0.8315 2019-08-01
#>2  000300.SH   20190731  -0.9033 2019-07-31
#>3  000300.SH   20190730   0.4163 2019-07-30
#>4  000300.SH   20190729  -0.1114 2019-07-29
#>5  000300.SH   20190726   0.1948 2019-07-26

Retn = DATA.pivot(index='Date',columns='ts_code',values='pct_chg')
Retn.iloc[0,] = Retn.iloc[0,].fillna(value=0)
# Use data in previous row to fill NA
Retn = Retn.fillna(method='pad',axis=0)
Retn_bh = Bchmk.pivot(index='Date',columns='ts_code',values='pct_chg')

PB = DATA.pivot(index='Date',columns='ts_code',values='pb')
# Use P/B in next row to fill NA
PB = PB.fillna(method='backfill', axis=0)

MV = DATA.pivot(index='Date',columns='ts_code',values='circ_mv')
MV = MV.fillna(method='backfill', axis=0)

# Check if there is Date-Mismatch on Date
len(Retn) == len(PB) == len(Retn_bh) == len(MV)
#>True

MktRt = Mkt[['ts_code','trade_date','pct_chg']].copy()
MktRt['Date'] = pd.to_datetime(Bchmk.trade_date, format='%Y%m%d')
MktRt = MktRt.pivot(index='Date',columns='ts_code',values='pct_chg')

exit

# Import Data from Python to R
DATA_temp <- py$DATA_temp
DATA <- py$DATA
Retn <- py$Retn
Retn_bh <- py$Retn_bh
PB <- py$PB
MV <- py$MV
MktRt <- py$MktRt



# Construct Pofrtfolio
require(fBasic)
require(fUnitRoots)
row.names(PB) -> Tdate
Tdate <- as.Date(Tdate, format = '%Y-%m-%d')
P_Rtn <- rowMeans(Retn)
MKT <- P_Rtn - 0.04/360
P_Std <- rowSds(Retn)



# Try CAPM first
## 检验序列平稳性
m1 <- ar(Retn$`300136.SZ`,method = 'mle')
m1$order
#>[1] 11
adfTest(Retn$'300136.SZ', lag=11)
#>Title:
#> Augmented Dickey-Fuller Test
#>Test Results:
#>  PARAMETER:
#>    Lag Order: 11
#>  STATISTIC:
#>    Dickey-Fuller: -10.6569
#>  P VALUE:
#>    0.01 
m1 <- ar(MKT,method = 'mle')
m1$order
#>[1] 10
adfTest(MKT, lags = 12)
#>Title:
#> Augmented Dickey-Fuller Test
#>
#>Test Results:
#>  PARAMETER:
#>    Lag Order: 12
#>  STATISTIC:
#>    Dickey-Fuller: -11.287
#>  P VALUE:
#>    0.01 

lm_1 <- lm(Retn$`300136.SZ` ~ MKT)
par(mfrow=c(2,2))
plot(lm_P)
## residuals vs Fitted：残差与拟合图，看到一个曲线关系，这暗示着你可能需要对回归模型加上一个二次项
## normal Q~Q：正态Q-Q图，针对QLS的统计假设中的正态性，图上的点应该落在呈45度角的直线上；若不是如此，那么就违反了正态性的假设
## Scale-Location：尺寸位置图，满足同方差性要求在水平线周围的点是随机分布的
## Residuals vs Leverage（残差与杠杆图）：提供了你可能关注的单个观测点的信息。从图形可以鉴别出离群点、高杠杆值点和强影响点
summary(lm_1)
#>Call:
#>lm(formula = Retn$`300136.SZ` ~ MKT)
#>
#>Residuals:
#>    Min      1Q  Median      3Q     Max 
#>-16.060  -1.739  -0.199   1.540  61.446 
#>
#>Coefficients:
#>            Estimate Std. Error t value Pr(>|t|)    
#>(Intercept)  0.14836    0.06716   2.209   0.0273 *  
#>MKT          1.35613    0.05099  26.594   <2e-16 ***
#>---
#>Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
#>
#>Residual standard error: 3.233 on 2328 degrees of freedom
#>Multiple R-squared:  0.233,	Adjusted R-squared:  0.2327 
#>F-statistic: 707.2 on 1 and 2328 DF,  p-value: < 2.2e-16
acf(lm_1$residuals)
# 回归的余值项呈现自相关



### 3-Factor Model



