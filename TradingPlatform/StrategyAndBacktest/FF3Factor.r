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

