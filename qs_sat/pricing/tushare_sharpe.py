from datetime import datetime as dt
import os
import pprint
import sys
sys.path.append(os.path.join('..', 'pricing'))

import numpy as np
import pandas as pd
from tu_share import TuShare

def annualised_sharpe(returns, N=252):
    """
    Calculate the annualised Sharpe ratio of a returns stream based on a number of trading periods, N. N defaults to 252, which then assumes a stream of daily returns.
    'returns' should be a pandas Series
    """
    return np.sqrt(N) * returns.mean() / returns.std()

def equity_sharpe(ticker):
    """
    Calculates the annualised Sharpe ratio based on the daily returns of an equity ticker symbol listed in AlphaVantage.
    """
    # Use the percentage change method to easily calculate daily returns
    ticker['daily_ret'] = (ticker['close_price'] * ticker['adj_factor']).pct_change()

    # Assume an average annual risk-free rate over the period of 4%
    ticker['excess_daily_ret'] = ticker['daily_ret'] - 0.04/252

    # Return the annualised Sharpe ratio based on the excess daily returns
    return annualised_sharpe(ticker['excess_daily_ret'])

def market_neutral_sharpe(ticker, benchmark):
    """
    Calculates the annualised Sharpe ratio of a market neutral long/short strategy inolving the long of 'ticker' with a corresponding short of the 'benchmark'.
    Both input should be pandas DataFrame
    """
    # Calculate the percentage returns on each of the time series
    ticker['daily_ret'] = (ticker['close_price'] * ticker['adj_factor']).pct_change()
    benchmark['daily_ret'] = (benchmark['close_price'] * benchmark['adj_factor']).pct_change()

    # Create a new DataFrame to store the strategy information
    # The net returns are (long - short)/2, since there is twice
    # the trading capital for this strategy
    strat = pd.DataFrame(index=ticker.index)
    strat['net_ret'] = (ticker['daily_ret'] - benchmark['daily_ret'])/2.0

    # Return the annualised Sharpe ratio for this strategy
    return annualised_sharpe(strat['net_ret'])



if __name__ == "__main__":
    # Create an AlphaVantage API instance
    tu = TuShare()
    # Download the data from tushare
    start_date = dt(2015, 1, 1).strftime('%Y%m%d')
    end_date = dt(2020, 2, 14).strftime('%Y%m%d')

    # Create a DataFrame of 中国银行A股 stock prices
    SH601988 = tu.get_daily_historic_data('601988', start_date, end_date, asset='E', adj=None)
    # Create a DataFrame of HS300 stock prices based on 中国银行A股 data
    #   tushare allows at most 800 records per time for funds data
    HS300_0 = tu.get_daily_historic_data('510300', start_date, '20170420', asset='FD', adj=None)
    HS300_1 = tu.get_daily_historic_data('510300', '20170421', end_date, asset='FD', adj=None)
    HS300 = pd.concat([HS300_0, HS300_1])

    """
    Typeical output from TuShare.get_daily_historic_data() method
                ts_code  open  high   low  close         vol  adj_factor
    trade_date
    2015-01-05   601988  4.18  4.50  4.18   4.42  2308454847       1.432
    2015-01-06   601988  4.38  4.74  4.28   4.56  2312726022       1.432
    2015-01-07   601988  4.46  4.64  4.44   4.54  1548575455       1.432
    2015-01-08   601988  4.55  4.57  4.31   4.33  1489272605       1.432
    2015-01-09   601988  4.28  4.76  4.23   4.47  2277619375       1.432
    """

    print( "Sharpe Ratio: %s" % equity_sharpe(SH601988))
    # Sharpe Ratio: -0.02453723664721581
    print( "Market Neutral Sharpe Ratio: %s" % market_neutral_sharpe(SH601988, HS300))
    # Market Neutral Sharpe Ratio: -0.06990796850282632
