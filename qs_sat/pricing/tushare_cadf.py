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
import MySQLdb as mdb
from tu_share import TuShare

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
    plt.clf()

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
    plt.clf()

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
    plt.clf()

if __name__ == "__main__":
    # Create an TuShare API instance
    tu = TuShare()

    # Download stock data from DATABASE for 600487 亨通光电 and 600703 三安光电
    start_date = dt(2019, 1, 1).strftime('%Y-%m-%d %H:%M:%S')
    end_date = dt(2020, 2, 12).strftime('%Y-%m-%d %H:%M:%S')
    SH600487 = tu.get_daily_data_sql('600487', start_date, end_date)
    SH600703 = tu.get_daily_data_sql('600703', start_date, end_date)

    # Place them into the Pandas DataFrame format
    # Adj Price is backward-adjusted
    df = pd.DataFrame(index=SH600487.index)
    df["SH600487"] = SH600487["close_price"] * SH600487['adj_factor']
    df["SH600703"] = SH600703["close_price"] * SH600703['adj_factor']

    # Plot the two time series
    plot_price_series(df, "SH600487", "SH600703", start_date, end_date)
    # Display a scatter plot of the two time series
    plot_scatter_series(df, "SH600487", "SH600703")
    # Calculate optimal hedge ratio "beta" via Statsmodels
    model = sm.OLS(df['SH600703'], df["SH600487"])
    res = model.fit()
    beta_hr = res.params[0]
    # Calculate the residuals of the linear combination
    df["res"] = df["SH600703"] - beta_hr * df["SH600487"]
    # Plot the residuals
    plot_residuals(df, start_date, end_date)
    # Calculate and output the CADF test on the residuals
    cadf = ts.adfuller(df["res"])
    pprint.pprint(cadf)

"""
H0: $\beta = 0$, no cointegrating
(-1.357209837848568,  # $\beta$
0.6026097982343958,  # P-value
0, 
269,  # Number of samples
{’1%’: -3.4548987220044336, ’10%’: -2.572527778361272, ’5%’: -2.8723451788613157},
1870.5198659466103)
"""