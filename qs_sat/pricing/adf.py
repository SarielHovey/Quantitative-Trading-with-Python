from datetime import datetime as dt
import os
import pprint
import sys
# Requires 'alpha_vantage.py' in current path
sys.path.append(os.path.join('..', 'pricing'))
import statsmodels.tsa.stattools as ts
from alpha_vantage import AlphaVantage

if __name__ == "__main__":
    # Create an AlphaVantage API instance
    av = AlphaVantage()
    # Download the Amazon OHLCV data from 1/1/2000 to 1/1/2015
    start_date = dt(2000, 1, 1)
    end_date = dt(2015, 1, 1)
    amzn = av.get_daily_historic_data('AMZN', start_date, end_date)
    # Output the results of the Augmented Dickey-Fuller test for Amazon
    # with a lag order value of 1
    pprint.pprint(ts.adfuller(amzn['Adj Close'].tolist(), 1))