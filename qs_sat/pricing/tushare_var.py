from datetime import datetime as dt
import os
import pprint
import sys
sys.path.append(os.path.join('..', 'pricing'))
import numpy as np
from scipy.stats import norm
from tu_share import TuShare

def var_cov_var(P, c, mu, sigma):
    """
    Variance-Covariance calculation of daily Value-at-Risk using confidence level c, with mean of returns mu and standard deviation of returns sigma, on a portfolio of value P.
    """
    alpha = norm.ppf(1-c, mu, sigma)
    return P - P*(alpha + 1)

if __name__ == "__main__":
    # Create an AlphaVantage API instance
    tu = TuShare()

    # Download the Citi Group OHLCV data from 1/1/2010 to 1/1/2014
    start_date = dt(2018, 1, 1).strftime('%Y%m%d')
    end_date = dt(2020, 2, 19).strftime('%Y%m%d')
    HS300 = tu.get_daily_historic_data('510300', start_date, end_date, asset='FD', adj=None)

    # Calculate the percentage change
    HS300["rets"] = (HS300["close_price"] * HS300['adj_factor']).pct_change()
    
    P = 1e6 # 1,000,000 CNY
    c = 0.99 # 99% confidence interval
    mu = np.mean(HS300["rets"])
    sigma = np.std(HS300["rets"])

    var = var_cov_var(P, c, mu, sigma)
    print("Value-at-Risk: ￥%0.2f" % var)