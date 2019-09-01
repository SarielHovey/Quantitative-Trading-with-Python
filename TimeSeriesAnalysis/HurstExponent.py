from __future__ import print_function
import statsmodels.tsa.stattools as ts
from datetime import datetime
from numpy import cumsum, log, polyfit, sqrt, std, subtract
from numpy.random import randn

def hurst(ts):
    """ Return Hurst Exponent of time series vector ts
        If < 0.5 then Mean reverting
        If = 0.5 then Geometric Brownian Motion
        If > 0.5 then Trending
    """
    lags = range(2, 100)
    tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    poly = polyfit(log(lags), log(tau), 1)
    return poly[0] * 2.0
  
gbm = log(cumsum(randn(100000)) + 1000)
mr = log(randn(100000) + 1000)
tr = log(cumsum(randn(100000)+1) + 1000)

print('Hurst for Geometric Brownian Motion  %s' % hurst(gbm))
print('Hurst for Mean-Reverting %s' % hurst(mr))
print('Hurst for Trending Series %s' % hurst(tr))
#>Hurst for Geometric Brownian Motion  0.5094958688977529
#>Hurst for Mean-Reverting 6.374652781798867e-05
#>Hurst for Trending Series 0.9520874471335533

# Now let's try some real world data
import tushare as ts
import pandas as pd
import numpy as np
DATA = ts.pro_bar(ts_code='600519.SH', adj='qfq', start_date='20150101', end_date='20190901') 
GZMT = DATA.close.copy().values

hurst(GZMT)
#> 0.5069715212421458
## So, 贵州茅台A shows Geometric Brownian Motion
