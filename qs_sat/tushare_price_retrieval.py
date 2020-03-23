from datetime import datetime as dt
import warnings
import time
import MySQLdb as mdb
import tushare as ts
import pandas as pd
# Please set Tushare Pro API before use this
WAIT_TIME_IN_SECONDS = 1.5 # Adjust how frequently the API is called (second)

# Obtain a database connection to the MySQL instance
DB_HOST = 'localhost'
DB_USER = 'sec_user'
DB_PASS = 'Your_Password_Here'
DB_NAME = 'securities_master'
con = mdb.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)

def obtain_list_of_db_tickers():
    """
    Obtains a list of the ticker symbols of HS300 in the database.
    """
    cur = con.cursor()
    cur.execute("SELECT id, ticker FROM symbol where exchange_id = 3 or exchange_id = 4")
    con.commit()
    data = cur.fetchall()
    return [[d[0], d[1]] for d in data]

def tushare_ticker(ticker_list):
    """
    Input should be output from obtain_list_of_db_tickers(),
    Output will be a modified ticker_list for Tushare API with same shape.
    Further Version will be rewrite in Cython for performance.
    """
    for i, tick in enumerate(ticker_list):
        if tick[1][:2] == '60':
            tick[1] += '.SH'
        elif tick[1][:2] == '00':
            tick[1] += '.SZ'
        elif tick[1][:2] == '30':
            tick[1] += '.SZ'
    return ticker_list

def tushare_data(tick, start_date, end_date):
    """
    Download daily data via tushare API for one tick.
    Price are non-adjusted.
    """
    global errList
    errList = []
    try:
        data0 = ts.pro_bar(ts_code=tick, start_date=start_date, end_date=end_date,adj=None)
        data1 = ts.pro_api().adj_factor(ts_code=tick, start_date=start_date, end_date=end_date)
    except Exception as e:
        print(
            "Could not download Tushare data for %s ticker "
            "(%s)...skipping." % (tick, e))
        errList.append(tick)
        return []
    else:
        data = pd.merge(data0[['ts_code','trade_date','open','high','low','close','vol']],data1[['trade_date','adj_factor']],how='left',left_on='trade_date',right_on='trade_date')
        data.vol = data.vol.apply(lambda x: int(x * 100))
        data.trade_date = pd.to_datetime(data.trade_date)
        prices = []
        for i, day in enumerate(data.trade_date):
            prices.append(
                (
                    data.ix[i,'trade_date'], # d0
                    data.ix[i,'open'], # d1
                    data.ix[i,'high'], # d2
                    data.ix[i,'low'], # d3
                    data.ix[i,'close'], # d4
                    data.ix[i,'vol'], # d5
                    data.ix[i,'adj_factor'] # d6
                ))
        return prices

def insert_daily_data_into_db(data_vendor_id, symbol_id, daily_data):
    """
    Takes a list of tuples of daily_data and adds it to the MySQL database. Appends the vendor ID and symbol ID to the data.
    """
    now = dt.utcnow()
    # Amend the data to include the vendor ID and symbol ID
    daily_data = [
        (data_vendor_id, symbol_id, d[0], dt.utcnow(), dt.utcnow(), d[1], d[2], d[3], d[4], d[5], d[6]) for d in daily_data
    ]
    # Create the insert strings
    column_str = (
        "data_vendor_id, symbol_id, price_date, created_date, last_updated_date, open_price, high_price, low_price, close_price, volume, adj_factor"
    )
    insert_str = ("%s, " * 11)[:-2]
    final_str = ("INSERT INTO daily_price (%s) VALUES (%s)" % (column_str, insert_str))
    # Using the MySQL connection, carry out an INSERT INTO for every symbol
    cur = con.cursor()
    cur.executemany(final_str, daily_data)
    con.commit()



if __name__ == '__main__':
    # This ignores the warnings regarding Data Truncation from the AlphaVantage precision to Decimal(19,4) datatypes
    warnings.filterwarnings('ignore')
    ticker_list = obtain_list_of_db_tickers()
    tickers = tushare_ticker(ticker_list)
    lentickers = len(tickers)
    for i, t in enumerate(tickers):
        print("Adding data for %s: %s out of %s" % (t[1], i+1, lentickers))
        ts_data = tushare_data(t[1],start_date='20200323',end_date='20200323')
        insert_daily_data_into_db(2, t[0], ts_data)
        time.sleep(WAIT_TIME_IN_SECONDS)
    errList = pd.Series(errList)
    errList.to_csv('ErrorList.csv',header=False,index=False,encoding='UTF-8')
    print("Successfully added TuSharePro pricing data to DB.")