import itertools
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import copy
import datetime
from mpl_toolkits.mplot3d import Axes3D
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.dates import (
    DateFormatter, WeekdayLocator, DayLocator, MONDAY
)
import pandas as pd
from tu_share import TuShare

plt.style.use('seaborn')

# Set the number of samples, the means and variances of each of the three simulated clusters
def simulate_KMeans():
    samples = 100
    mu = [(7, 5), (8, 12), (1, 10)]
    cov = [
        [[0.5, 0], [0, 1.0]],
        [[2.0, 0], [0, 3.5]],
        [[3, 0], [0, 5]],
    ]
    # Generate a list of the 2D cluster points
    norm_dists = [
        np.random.multivariate_normal(m, c, samples)
        for m, c in zip(mu, cov)
    ] # len(norm_dists) = 3
    X = np.array(list(itertools.chain(*norm_dists))) # use itertools to append values in one array
    # Apply the K-Means Algorithm for k=3, which is equal to the number of true Gaussian clusters
    km3 = KMeans(n_clusters=3)
    km3.fit(X)
    km3_labels = km3.labels_
    # Apply the K-Means Algorithm for k=4, which is larger than the number of true Gaussian clusters
    km4 = KMeans(n_clusters=4)
    km4.fit(X)
    km4_labels = km4.labels_
    # Create a subplot comparing k=3 and k=4 for the K-Means Algorithm
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,6))
    ax1.scatter(X[:, 0], X[:, 1], c=km3_labels.astype(np.float))
    ax1.set_xlabel("$x_1$")
    ax1.set_ylabel("$x_2$")
    ax1.set_title("K-Means with $k=3$")
    ax2.scatter(X[:, 0], X[:, 1], c=km4_labels.astype(np.float))
    ax2.set_xlabel("$x_1$")
    ax2.set_ylabel("$x_2$")
    ax2.set_title("K-Means with $k=4$")
    plt.show()

def get_open_normalised_prices(symbol, start, end):
    """
    Obtains a pandas DataFrame containing open normalised prices for high, low and close for a particular equities symbol from DB. That is, it creates High/Open, Low/Open and Close/Open columns.
    """
    tu = TuShare()
    df = tu.get_daily_data_sql(symbol, startdate=start, enddate=end)
    df["H/O"] = df["high_price"]/df["open_price"]
    df["L/O"] = df["low_price"]/df["open_price"]
    df["C/O"] = df["close_price"]/df["open_price"]
    df.drop([
        'open_price','high_price','low_price','close_price','volume','adj_factor'
    ], axis=1, inplace=True)
    return df

def plot_candlesticks(data, since):
    """
    Plot a candlestick chart of the prices, appropriately formatted for dates.
    """
    # Copy and reset the index of the dataframe to only use a subset of the data for plotting
    df = copy.deepcopy(data)
    df = df[df.index >= since]
    df.reset_index(inplace=True)
    df['date_fmt'] = df['price_date'].apply(
        lambda date: mdates.date2num(date.to_pydatetime())
    )
    # Set the axis formatting correctly for dates with Mondays highlighted as a "major" tick
    mondays = WeekdayLocator(MONDAY)
    alldays = DayLocator()
    weekFormatter = DateFormatter('%b %d')
    fig, ax = plt.subplots(figsize=(16,4))
    fig.subplots_adjust(bottom=0.2)
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(weekFormatter)
    # Plot the candlestick OHLC chart using black for up days and red for down days
    csticks = candlestick_ohlc(
        ax, df[
            ['date_fmt', 'open_price', 'high_price', 'low_price', 'close_price']
        ].values, width=0.6, colorup='#000000', colordown='#ff0000'
    )
    ax.xaxis_date()
    plt.setp(
        plt.gca().get_xticklabels(),
        rotation=45, horizontalalignment='right'
    )
    plt.show()



if __name__ == "__main__":
    tu = TuShare()
    start = datetime.datetime(2018, 1, 1).strftime('%Y-%m-%d %H:%M:%S')
    end = datetime.datetime(2020, 3, 26).strftime('%Y-%m-%d %H:%M:%S')
    ZGYH = tu.get_daily_data_sql('601988',startdate=start,enddate=end)
    plot_candlesticks(ZGYH, datetime.datetime(2018, 3, 26))
