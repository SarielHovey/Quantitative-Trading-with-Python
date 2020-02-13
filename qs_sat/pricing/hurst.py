from datetime import datetime as dt
import os
import sys
sys.path.append(os.path.join('..', 'pricing'))

from numpy import array, cumsum, log, polyfit, sqrt, std, subtract
from numpy.random import randn

from alpha_vantage import AlphaVantage

def hurst(time_series):
    """
    Calculates the Hurst Exponent of the time series vector ts.

    Parameters
    ----------
    ts : 'np.ndarray' Time series array of prices

    Returns
    -------
    'float' The Hurst Exponent of the time series
    """
    # Create the range of lag values
    lags = range(2, 100)
    # Calculate the array of the variances of the lagged differences
    tau = [ sqrt(std(subtract(time_series[lag:], time_series[:-lag]))) for lag in lags]
    # Use a linear fit to estimate the Hurst Exponent
    poly = polyfit(log(lags), log(tau), 1)
    # Return the Hurst exponent from the polyfit output
    return poly[0] * 2.0


if __name__ == "__main__":
    # Create a Gometric Brownian Motion, Mean-Reverting and Trending Series
    gbm = log(cumsum(randn(100000)) + 1000)
    mr = log(randn(100000) + 1000)
    tr = log(cumsum(randn(100000) + 1) + 1000)

    # Create an AlphaVantage API instance
    av = AlphaVantage()
    # Download the Amazon OHLCV data from 1/1/2000 to 1/1/2015
    start_date = dt(2000, 1, 1)
    end_date = dt(2015, 1, 1)
    amzn = av.get_daily_historic_data('AMZN', start_date, end_date)

    # Output the Hurst Exponent for each of the above series
    print("Hurst(GBM): %0.2f" % hurst(gbm))
    print("Hurst(MR): %0.2f" % hurst(mr))
    print("Hurst(TR): %0.2f" % hurst(tr))
    # Calculate the Hurst exponent for the AMZN adjusted closing prices
    print("Hurst(AMZN): %0.2f" % hurst(array(amzn['Adj Close'].tolist())))
