import DataAPI
import numpy as np
import pandas as pd
import talib as ta
from collections import deque
from itertools import product
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
from CAL import *
cal = Calendar('China.SSE')

universe = ['RBM0']
start = '2017-01-02'
end = '2017-12-31'
capital_base = 1e7
refresh_rate = (1, 5)
freq = 'm'
commission = {'RB': (0.000025, 'perValue')}
slippage = Slippage(0, 'perValue')
amount = 20
accounts = {
    'futures_account': AccountConfig(account_type='futures', capital_base=capital_base, commission=commission, slippage=slippage)
}

def initialize(context):
    context.pipe_length = 2
    context.refresh_rate = refresh_rate[1]
    context.keys = [u'openPrice', u'highPrice', u'lowPrice', u'closePrice', u'turnoverVol', u'tradeDate']
    context.data = {key:deque([], maxlen=context.pipe_length) for key in context.keys}
    context.high = np.NAN
    context.low = np.NAN
    context.close = np.NAN
    context.count1 = 0
    context.count2 = 0

def handle_data(context):
    futures_account = context.get_account('futures_account')
    symbol = context.get_symbol(universe[0])
    long_position = futures_account.get_positions().get(symbol, dict()).get('long_amount', 0)
    short_position = futures_account.get_positions().get(symbol, dict()).get('short_amount', 0)
    if context.current_minute == '09:30':
        yester_data = DataAPI.MktFutdGet(tradeDate=context.previous_date,ticker=symbol,field=[u'closePrice',u'highestPrice',u'lowestPrice'],pandas='1')
        context.high = yester_data['highestPrice'].iat[0]
        context.low = yester_data['lowestPrice'].iat[0]
        context.close = yester_data['closePrice'].iat[0]

    if context.current_minute > '09:30' and context.current_minute < '14:55':
        #-------------------------------------------------------------------------
        if len(context.data['openPrice']) < context.pipe_length:
            hist = context.history(symbol=symbol, attribute=context.keys[:-1], time_range=context.refresh_rate*context.pipe_length, freq='1m')[symbol]
        else:
            hist = context.history(symbol=symbol, attribute=context.keys[:-1], time_range=context.refresh_rate, freq='1m')[symbol]

        current_data = {key:[] for key in context.keys}
        for i in range(len(hist)/context.refresh_rate):
            current_bar = hist[context.refresh_rate*i : context.refresh_rate*(i+1)]
            current_bar['tradeDate'] = [i[:10] for i in current_bar.index]
            current_data['closePrice'].append(current_bar.ix[len(current_bar)-1, 'closePrice'])
            current_data['openPrice'].append(current_bar.ix[0, 'openPrice'])
            current_data['highPrice'].append(current_bar['highPrice'].max())
            current_data['lowPrice'].append(current_bar['lowPrice'].min())
            current_data['turnoverVol'].append(current_bar['turnoverVol'].sum())
            current_data['tradeDate'].append(current_bar.ix[len(current_bar)-1, 'tradeDate'])

        for i in context.keys:
            for j in current_data[i]:
                context.data[i].append(j)
        #------------------------------------------------------------------------------
        data = context.data
        bef_2_close = data['closePrice'][-2]
        bef_2_high = data['highPrice'][-2]
        bef_1_close = data['closePrice'][-1]
        bef_1_high = data['highPrice'][-1]
        bef_1_low = data['lowPrice'][-1]
        bef_1_open = data['openPrice'][-1]
        # 观察卖出价
        ssetup = context.high + 0.35*(context.close - context.low)
        # 观察买入价
        bsetup = context.low - 0.35*(context.high - context.close)
        # 反转卖出价
        senter = (1+0.07)/2*(context.high-context.low) - 0.07*context.low
        # 反转买入价
        benter = (1+0.07)/2*(context.high-context.low) - 0.07*context.high
        # 突破买入价
        bbreak = ssetup+0.25*(ssetup-bsetup)
        # 突破卖出价
        sbreak = bsetup-0.25*(ssetup-bsetup)

        ## 趋势
        if bef_2_close <= bbreak and bef_1_close > bbreak:
            if long_position == 0:
                futures_account.order(symbol, amount, 'open')
            if short_position != 0:
                futures_account.order(symbol, short_position, 'close')
        if bef_2_close >= sbreak and bef_1_close < sbreak:
            if short_position == 0:
                futures_account.order(symbol, -amount, 'open')
            if long_position != 0:
                futures_account.order(symbol, -long_position, 'close')
        ## 反转
        ### 多单反转
        if bef_1_high > ssetup and bef_1_close > senter:
            context.count1 = 1
        if context.count1 == 1 and bef_1_close < senter:
            if long_position >0:
                futures_account.order(symbol, -long_position, 'close')
                futures_account.order(symbol, -amount, 'open')
        ### 空单反转
        if bef_1_low < bsetup:
            context.count2 == 1
        if context.count2 == 1 and bef_1_close > benter:
            if short_position != 0:
                futures_account.order(symbol, short_position, 'close')
                futures_account.order(symbol, amount, 'open')

    elif context.current_minute >= '14:55':
        if short_position >0:
            futures_account.order(symbol, short_position, 'close')
        if long_position >0:
            futures_account.order(symbol, -long_position, 'close')
        context.high = np.NAN
        context.low = np.NAN
        context.close = np.NAN
        context.count1 = 0
        context.count2 = 0




