from datetime import datetime as dt
import os
import pprint
import sys
sys.path.append(os.path.join('..', 'pricing'))

import numpy as np
import pandas as pd
from alpha_vantage import AlphaVantage

def annualised_sharpe(returns, N=252):
    """
    Calculate the annualised Sharpe ratio of a returns stream based on a number of trading periods, N. N defaults to 252, which then assumes a stream of daily returns.
    'returns' should be a pandas DataFrame
    """
    return np.sqrt(N) * returns.mean() / returns.std()

def equity_sharpe(ticker):
    """
    Calculates the annualised Sharpe ratio based on the daily returns of an equity ticker symbol listed in AlphaVantage.
    """
    # Use the percentage change method to easily calculate daily returns
    ticker['daily_ret'] = ticker['Close'].pct_change()

    # Assume an average annual risk-free rate over the period of 5%
    ticker['excess_daily_ret'] = ticker['daily_ret'] - 0.05/252

    # Return the annualised Sharpe ratio based on the excess daily returns
    return annualised_sharpe(ticker['excess_daily_ret'])

def market_neutral_sharpe(ticker, benchmark):
    """
    Calculates the annualised Sharpe ratio of a market neutral long/short strategy inolving the long of 'ticker' with a corresponding short of the 'benchmark'.
    Both input should be pandas DataFrame
    """
    # Calculate the percentage returns on each of the time series
    ticker['daily_ret'] = ticker['Close'].pct_change()
    benchmark['daily_ret'] = benchmark['Close'].pct_change()

    # Create a new DataFrame to store the strategy information
    # The net returns are (long - short)/2, since there is twice
    # the trading capital for this strategy
    strat = pd.DataFrame(index=ticker.index)
    strat['net_ret'] = (ticker['daily_ret'] - benchmark['daily_ret'])/2.0

    # Return the annualised Sharpe ratio for this strategy
    return annualised_sharpe(strat['net_ret'])



if __name__ == "__main__":
    # Create an AlphaVantage API instance
    av = AlphaVantage()
    # Download the AlphaBet (Google) OHLCV data from 1/1/2005 to 1/1/2013
    start_date = dt(2005, 1, 1)
    end_date = dt(2013, 1, 1)

    # Create a DataFrame of AlphaBet (Google) stock prices
    goog = av.get_daily_historic_data('GOOGL', start_date, end_date)
    # Create a DataFrame of S&P ETF stock prices based on AlphaVantage data
    spy = av.get_daily_historic_data('SPY', start_date, end_date)

    print( "AlphaBet Sharpe Ratio: %s" % equity_sharpe(goog))

    print( "AlphaBet Market Neutral Sharpe Ratio: %s" % market_neutral_sharpe(goog, spy))
