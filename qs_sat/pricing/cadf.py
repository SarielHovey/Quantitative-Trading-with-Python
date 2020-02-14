# Cointegrated Augmented Dickey-Fuller Test
from datetime import datetime as dt
import os
import pprint
import sys
sys.path.append(os.path.join('..', 'pricing'))

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
from alpha_vantage import AlphaVantage

def plot_price_series(df, ts1, ts2, start_date, end_date):
    """
    Plot both time series on the same line graph for the specified date range.

    Parameters
    ----------
    df : 'pd.DataFrame' The DataFrame containing prices for each series
    ts1 : 'str' The first time series column name
    ts2 : 'str' The second time series column name
    start_date : 'datetime' The starting date for the plot
    end_date : 'datetime' The ending date for the plot
    """
    months = mdates.MonthLocator() # every month
    fig, ax = plt.subplots()
    ax.plot(df.index, df[ts1], label=ts1)
    ax.plot(df.index, df[ts2], label=ts2)
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(start_date, end_date)
    ax.grid(True)
    fig.autofmt_xdate()
    plt.xlabel('Month/Year')
    plt.ylabel('Price ($)')
    plt.title('%s and %s Daily Prices' % (ts1, ts2))
    plt.legend()
    plt.savefig('PriceSeries.png')

def plot_scatter_series(df, ts1, ts2):
    """
    Plot a scatter plot of both time series for via the provided DataFrame.

    Parameters
    ----------
    df : 'pd.DataFrame' The DataFrame containing prices for each series
    ts1 : 'str' The first time series column name
    ts2 : 'str' The second time series column name
    """
    plt.xlabel('%s Price ($)' % ts1)
    plt.ylabel('%s Price ($)' % ts2)
    plt.title('%s and %s Price Scatterplot' % (ts1, ts2))
    plt.scatter(df[ts1], df[ts2])
    plt.savefig('Scatter.png')

def plot_residuals(df, start_date, end_date):
    """
    Plot the residuals of OLS procedure for both time series.
    Require df has column "res" to store residuals.

    Parameters
    ----------
    df : 'pd.DataFrame' The residuals DataFrame
    start_date : 'datetime' The starting date of the residuals plot
    end_date : 'datetime' The ending date of the residuals plot
    """
    months = mdates.MonthLocator() # every month
    fig, ax = plt.subplots()
    ax.plot(df.index, df["res"], label="Residuals", c='blue')
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(start_date, end_date)
    ax.grid(True)
    fig.autofmt_xdate()
    plt.xlabel('Month/Year')
    plt.ylabel('Price ($)')
    plt.title('Residual Plot')
    plt.legend()
    plt.plot(df["res"])
    plt.savefig('Residual.png')

if __name__ == "__main__":
    # Create an AlphaVantage API instance
    av = AlphaVantage()

    # Download AREX and WLL for the duration of 2015
    start_date = dt(2015, 1, 1)
    end_date = dt(2016, 1, 1)
    arex = av.get_daily_historic_data('AREX', start_date, end_date)
    wll = av.get_daily_historic_data('WLL', start_date, end_date)

    # Place them into the Pandas DataFrame format
    df = pd.DataFrame(index=arex.index)
    df["AREX"] = arex["Close"]
    df["WLL"] = wll["Close"]

    # Plot the two time series
    plot_price_series(df, "AREX", "WLL", start_date, end_date)
    # Display a scatter plot of the two time series
    plot_scatter_series(df, "AREX", "WLL")
    # Calculate optimal hedge ratio "beta" via Statsmodels
    model = sm.OLS(df['WLL'], df["AREX"])
    res = model.fit()
    beta_hr = res.params[0]
    # Calculate the residuals of the linear combination
    df["res"] = df["WLL"] - beta_hr * df["AREX"]
    # Plot the residuals
    plot_residuals(df, start_date, end_date)
    # Calculate and output the CADF test on the residuals
    cadf = ts.adfuller(df["res"])
    pprint.pprint(cadf)

"""
H0: $\beta = 0$, no cointegrating
(-2.902690165051807,  # $\beta$
0.04503606102328277,  # P-value
2, 
249,  # Number of samples
{’1%’: -3.4568881317725864, ’10%’: -2.5729936189738876, ’5%’: -2.8732185133016057},
818.2699213707956)
"""