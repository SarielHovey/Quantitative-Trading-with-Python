from datetime import datetime as dt
import os
import pprint
import sys
# Requires 'tushare.py' in current path
# Default: Get daily OHLCV data from DATABASE securities_master
sys.path.append(os.path.join('..', 'pricing'))
import statsmodels.tsa.stattools as ts
from tu_share import TuShare

if __name__ == "__main__":
    # Create an Tushare API instance
    tu = TuShare()
    # Download the 601988.SH OHLCV data from 1/1/2008 to 1/1/2018
    start_date = dt(2008, 1, 1).strftime('%Y-%m-%d %H:%M:%S')
    end_date = dt(2018, 1, 1).strftime('%Y-%m-%d %H:%M:%S')
    SH601988 = tu.get_daily_data_sql('601988', start_date, end_date)
    # Output the results of the Augmented Dickey-Fuller test for 601988.SH
    # with a lag order value of 1
    SH601988['adj_price'] = SH601988['close_price'] * SH601988['adj_factor']
    pprint.pprint(ts.adfuller(SH601988['adj_price'].tolist(), 1))

"""
ADF H0: $\gamma = 0$, series is not mean-reverting
OutPut:
    (-428.00838401505246,
    0.0, # P-value
    1,
    537281,
    {'1%': -3.4303621711566996,
     '10%': -2.5667728633158964,
     '5%': -2.8615453795088244},
     7664127.066837918)
"""
