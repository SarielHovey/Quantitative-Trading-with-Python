from datetime import datetime as dt
import json
import time
import warnings
import MySQLdb as mdb
import requests

ALPHA_VANTAGE_API_KEY = 'YOUR_API_KEY' # Change this to your API Key
ALPHA_VANTAGE_BASE_URL = 'https://www.alphavantage.co'
ALPHA_VANTAGE_TIME_SERIES_CALL = 'query?function=TIME_SERIES_DAILY_ADJUSTED'

TICKER_COUNT = 10 # Change this to 500 to download all tickers
WAIT_TIME_IN_SECONDS = 15.0 # Adjust how frequently the API is called (second)

# Obtain a database connection to the MySQL instance
DB_HOST = 'localhost'
DB_USER = 'sec_user'
DB_PASS = 'password'
DB_NAME = 'securities_master'
con = mdb.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)

def obtain_list_of_db_tickers():
    """
    Obtains a list of the ticker symbols in the database.
    """
    cur = con.cursor()
    cur.execute("SELECT id, ticker FROM symbol")
    con.commit()
    data = cur.fetchall()
    return [(d[0], d[1]) for d in data]

def construct_alpha_vantage_symbol_call(ticker):
    """
    Construct the full API call to AlphaVantage based on the user provided API key and the desired ticker symbol.
    """
    return "%s/%s&symbol=%s&outputsize=full&apikey=%s" % (
        ALPHA_VANTAGE_BASE_URL, 
        ALPHA_VANTAGE_TIME_SERIES_CALL, 
        ticker, 
        ALPHA_VANTAGE_API_KEY)

def get_daily_historic_data_alphavantage(ticker):
    """
    Use the generated API call to query AlphaVantage with the appropriate API key and return a list of price tuples for a particular ticker.
    """
    av_url = construct_alpha_vantage_symbol_call(ticker)
    try:
        av_data_js = requests.get(av_url)
        data = json.loads(av_data_js.text)['Time Series (Daily)']
    except Exception as e:
        print(
            "Could not download AlphaVantage data for %s ticker "
            "(%s)...skipping." % (ticker, e))
        return []
    else:
        prices = []
        for date_str in sorted(data.keys()):
            bar = data[date_str]
            prices.append(
                (
                    dt.strptime(date_str, '%Y-%m-%d'),
                    float(bar['1. open']),
                    float(bar['2. high']),
                    float(bar['3. low']),
                    float(bar['4. close']),
                    int(bar['6. volume']),
                    float(bar['5. adjusted close'])
                ))
        return prices

def insert_daily_data_into_db(data_vendor_id, symbol_id, daily_data):
    """
    Takes a list of tuples of daily data and adds it to the MySQL database. Appends the vendor ID and symbol ID to the data.
    """
    now = dt.utcnow()
    # Amend the data to include the vendor ID and symbol ID
    daily_data = [
        (data_vendor_id, symbol_id, d[0], now, now, d[1], d[2], d[3], d[4], d[5], d[6]) for d in daily_data
    ]
    # Create the insert strings
    column_str = (
        "data_vendor_id, symbol_id, price_date, created_date, "
        "last_updated_date, open_price, high_price, low_price, "
        "close_price, volume, adj_close_price"
    )
    insert_str = ("%s, " * 11)[:-2]
    final_str = (
        "INSERT INTO daily_price (%s) VALUES (%s)" % (column_str, insert_str)
    )
    # Using the MySQL connection, carry out an INSERT INTO for every symbol
    cur = con.cursor()
    cur.executemany(final_str, daily_data)
    con.commit()


if __name__ == "__main__":
    # This ignores the warnings regarding Data Truncation from the AlphaVantage precision to Decimal(19,4) datatypes
    warnings.filterwarnings('ignore')
    # Loop over the tickers and insert the daily historical data into the database
    tickers = obtain_list_of_db_tickers()[:TICKER_COUNT]
    lentickers = len(tickers)
    for i, t in enumerate(tickers):
        print(
            "Adding data for %s: %s out of %s" % (t[1], i+1, lentickers)
        )
        av_data = get_daily_historic_data_alphavantage(t[1])
        insert_daily_data_into_db('1', t[0], av_data)
        time.sleep(WAIT_TIME_IN_SECONDS)
    print("Successfully added AlphaVantage pricing data to DB.")
