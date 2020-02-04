from datetime import datetime as dt
import pandas as pd
import tushare as ts


COLUMNS = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
class TuShare(object):
    """
    Encapsulates calls to the TuShare API with a provided API key.
    API key shold be preset
    """
    def __init__(self, api_key='Your_KEY_Here'):
        """
        Initialise the TuShare instance.
        Parameters
        ----------
        api_key : 'str', optional
        The API key for the associated Tushare account
        """
        # ts.set_token(api_key)
        self.api_key = api_key

    def _construct_tushare_symbol_call(self, ticker):
        """
        Construct the full API call to AlphaVantage based on the user provided API key and the desired ticker symbol.
        Parameters
        ----------
        ticker : 'str'
        The ticker symbol, e.g. '600388'
        Returns
        -------
        'str'
        The full API call for a ticker time series
        """
        if ticker[:2] == '60':
            ticker += '.SH'
        elif ticker[:2] == '00':
            ticker += '.SZ'
        elif ticker[:2] == '30':
            ticker += '.SZ'
        return ticker

    def get_daily_historic_data(self, ts_code, adj, startdate, enddate):
        """
        Use the generated API call to query AlphaVantage with the appropriate API key and return a list of price tuples for particular ticker.
        Parameters
        ----------
        ticker : 'str', The ticker symbol, e.g. '600388.SZ'
        adj : Default as 'qfq'
        start_date : 'datetime', The starting date to obtain pricing for
        end_date : 'datetime', The ending date to obtain pricing for
        Returns
        -------
        'pd.DataFrame', The frame of OHLCV prices and volumes
        """
        ticker = self._construct_tushare_symbol_call(ts_code)
        try:
            ts_data_df = ts.pro_bar(ts_code=ticker, adj='qfq', start_date=startdate, end_date=enddate, pro_api=self.api_key)
        except Exception as e:
            print("Could not download Tushare data for %s ticker (%s)...stopping." % (ticker, e))
            return pd.DataFrame(columns=COLUMNS)
        else:
            ts_data_df['trade_date'] = pd.to_datetime(ts_data_df['trade_date'])
            return ts_data_df.set_index('trade_date')
