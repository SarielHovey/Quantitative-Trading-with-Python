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

def get_open_normalised_prices(symbol, start, end, query_switch=False):
    """
    Obtains a pandas DataFrame containing open normalised prices for high, low and close for a particular equities symbol from DB. That is, it creates High/Open, Low/Open and Close/Open columns.
    ------
    Default query_switch=False, will query data from DB.
    If query_switch=True, then symbol should be a DataFrame with same format with DB output.
    """
    if query_switch == False:
        tu = TuShare()
        df = tu.get_daily_data_sql(symbol, startdate=start, enddate=end)
    else:
        df = symbol
    df["H/O"] = df["high_price"]/df["open_price"]
    df["L/O"] = df["low_price"]/df["open_price"]
    df["C/O"] = df["close_price"]/df["open_price"]
    return df.drop([
        'open_price','high_price','low_price','close_price','volume','adj_factor'
    ], axis=1)

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

def plot_3d_normalised_candles(data):
    """
    Plot a 3D scatterchart of the open-normalised bars highlighting the separate clusters by colour.
    """
    fig = plt.figure(figsize=(12, 9))
    ax = Axes3D(fig, elev=21, azim=-136)
    ax.scatter(
        data["H/O"], data["L/O"], data["C/O"],
        c=labels.astype(np.float)
    )
    ax.set_xlabel('High/Open')
    ax.set_ylabel('Low/Open')
    ax.set_zlabel('Close/Open')
    plt.show()

def plot_cluster_ordered_candles(data):
    """
    Plot a candlestick chart ordered by cluster membership with the dotted blue line representing each cluster boundary.
    """
    # Set the format for the axis to account for dates correctly, particularly Monday as a major tick
    mondays = WeekdayLocator(MONDAY)
    alldays = DayLocator()
    weekFormatter = DateFormatter("")
    fig, ax = plt.subplots(figsize=(16,4))
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(weekFormatter)
    # Sort the data by the cluster values and obtain a separate DataFrame listing the index values at which the cluster boundaries change
    df = copy.deepcopy(data)
    df.sort_values(by="Cluster", inplace=True)
    df.reset_index(inplace=True)
    df["clust_index"] = df.index
    df["clust_change"] = df["Cluster"].diff()
    change_indices = df[df["clust_change"] != 0]
    # Plot the OHLC chart with cluster-ordered "candles"
    csticks = candlestick_ohlc(
        ax, df[
            ["clust_index", 'open_price', 'high_price', 'low_price', 'close_price']
        ].values, width=0.6,colorup='#000000', colordown='#ff0000'
    )
    # Add each of the cluster boundaries as a blue dotted line
    for row in change_indices.iterrows():
        plt.axvline(
            row[1]["clust_index"],
            linestyle="dashed", c="blue"
        )
    plt.xlim(0, len(df))
    plt.setp(
        plt.gca().get_xticklabels(),
        rotation=45, horizontalalignment='right'
    )
    plt.show()

def create_follow_cluster_matrix(data, k=5):
    """
    Creates a k x k matrix, where k is the number of clusters that shows when cluster j follows cluster i.
    """
    data["ClusterTomorrow"] = data["Cluster"].shift(-1)
    data.dropna(inplace=True)
    data["ClusterTomorrow"] = data["ClusterTomorrow"].apply(int)
    data["ClusterMatrix"] = list(
        zip(data["Cluster"], data["ClusterTomorrow"])
    )
    # create a frequency distribution of ClusterToday--ClusterTomorrow pairs
    cmvc = data["ClusterMatrix"].value_counts()
    clust_mat = np.zeros( (k, k) )
    for row in cmvc.iteritems():
        clust_mat[row[0]] = row[1]*100.0/len(data)
    print("Cluster Follow-on Matrix:")
    print(clust_mat)

if __name__ == "__main__":
    tu = TuShare()
    start = datetime.datetime(2018, 1, 1).strftime('%Y-%m-%d %H:%M:%S')
    end = datetime.datetime(2020, 3, 26).strftime('%Y-%m-%d %H:%M:%S')
    ZGYH = tu.get_daily_data_sql('601988',startdate=start,enddate=end)

    plot_candlesticks(ZGYH, datetime.datetime(2018, 3, 26))
    # Carry out K-Means clustering with five clusters on the three-dimensional data H/O, L/O and C/O
    ZGYH_norm = get_open_normalised_prices(ZGYH, start, end, query_switch=True)
    k = 5
    km = KMeans(n_clusters=k)
    km.fit(ZGYH_norm)
    labels = km.labels_
    ZGYH["Cluster"] = labels
    # Plot the 3D normalised candles using H/O, L/O, C/O
    plot_3d_normalised_candles(ZGYH_norm)
    # Plot the full OHLC candles re-ordered into their respective clusters
    plot_cluster_ordered_candles(ZGYH)
    # Create and output the cluster follow-on matrix
    create_follow_cluster_matrix(ZGYH)