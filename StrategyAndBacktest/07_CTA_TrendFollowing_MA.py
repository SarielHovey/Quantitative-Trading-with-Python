# Trend Following Strategy should be used in time > 3 days to capture the trend in mkt
# The strategy should be used when mkt shows obvious trend, NOT when mkt stays around a certain level
# Remember: Futures mks is a gambel table. Usage of Kelly's Fuction is recommended
# In this strategy, we use 2 MA lines, one Short term and one Long term to capture trends
# Warnning: The Strategy shows high profitability in past years, but behaves badly recently, either due to (1)limit of capacity; (2)tighter regulations
import re
import talib
from datetime import datetime
import pandas as pd
import numpy as np

start = '2014-07-01'
end = '2017-12-31'
universe = ['RBM0']
freq = 'd'
refresh_rate = 1

margin_ratio = DataAPI.FutuGet(ticker=universe, field=['ticker','tradeMarginRatio'], pandas='1')
margin_rate = dict(zip(margin_ratio.ticker.tolist(), [0.01*index for index in margin_ratio.tradeMarginRatio.tolist()]))
  
accounts = {
    'futures_account': AccountConfig(account_type='futures', capital_base=10000, margin_rate=margin_rate)
}
  
def initialize(context):
    pass

def handle_data(context):
    futures_account = context.get_account('futures_account')

    if main_contract_mapping_changed(context, futures_account):
        return

    symbol = context.get_symbol('RBM0')
    amount = 1

    current_long = futures_account.get_positions().get(symbol, dict()).get('long_amount', 0)
    current_short = futures_account.get_positions().get(symbol, dict()).get('short_amount', 0)

    history_data = context.history(symbol=symbol, attribute=['closePrice','openPrice','lowPrice','highPrice'], time_range=30, freq='1d')[symbol]
    # Here we use MA3 and MA5
    MA_S = talib.MA(history_data['closePrice'].apply(float).values,timeperiod=3)
    MA_L = talib.MA(history_data['closePrice'].apply(float).values,timeperiod=5)
    if MA_S[-1] > MA_L[-1] and MA_S[-2] < MA_L[-2]:
        if current_short >0:
            futures_account.order(symbol, current_short, 'close')
        if current_long < amount:
            futures_account.order(symbol, amount, 'open')
        
    if MA_S[-1] < MA_L[-1] and MA_S[-2] > MA_L[-2]:
        if current_long >0:
            futures_account.order(symbol, -current_long, 'close')
        if current_short <amount:
            futures_account.order(symbol, -amount, 'open')

    # Set a point to stop loss or profit
    profit = futures_account.get_positions().get(symbol,dict()).get('profit',0)
    margin = futures_account.get_positions().get(symbol,dict()).get('long_margin',0) - futures_account.get_positions().get(symbol,dict()).get('short_margin',0)
    # Seems the best stop-loss/profit interval currently
    if margin and profit/margin < -0.1:
        if current_long > 0:
            futures_account.order(symbol, -current_long, 'close')
        if current_short > 0:
            futures_account.order(symbol, current_short, 'close')
        print(datetime.strftime(context.current_date, '%Y-%m-%d') + ' 止损')

    if margin and profit/margin > 0.3:
        if current_long >0:
            futures_account.order(symbol, -current_long, 'close')
        if current_short > 0:
            futures_account.order(symbol, current_short, 'close')
        print(datetime.strftime(context.current_date, '%Y-%m-%d') + ' 止盈')   

def main_contract_mapping_changed(context, futures_account):
    if context.mapping_changed('RBM0'):
        symbol_bef, symbol_aft = context.get_rolling_tuple('RBM0')
        if futures_account.get_position(symbol_bef):
            futures_account.switch_position(symbol_bef, symbol_aft)
            return(True)
    return(False)
