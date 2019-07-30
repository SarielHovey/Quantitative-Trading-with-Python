from __future__ import division
import pandas as pd
import numpy as np
import datetime
from dateutil.parser import parse
from CAL.PyCAL import *
import os
cal = Calendar('China.SSE')





# 时间截面选股
def MichaelHiggins(universe, date):
    """
    Given stock-list and date,
    Args:
        universe -- stocklist -- list of str
        date -- datetime object -- str or datetime
    Returns:
        list: stocks with lowest 30% PEG, lowest 30% Debt/Asset and lowest 30% PCF
    Examples:
        >> universe = set_universe('HS300')
        >> buy_list = MichaelHiggins(universe, '20190729')
    """
    trade_date = date if isinstance(date, datetime.datetime) else parse(date)
    trade_date = trade_date.strftime('%Y%m%d')
    # 使用Uqer API获取股息率数据
    df_factor = DataAPI.MktStockFactorsOneDayGet(secID=universe, tradeDate=trade_date, field=['secID','CTOP'], pandas='1')
    df_factor.sort_values('CTOP', ascending=False, inplace=True)
    df_factor_select = df_factor.head(10)
    sec_list = df_factor_select['secID'].tolist()
    return(sec_list)

# 获取调仓日. 此处设为每年5月1日
tradedaylist = DataAPI.TradeCalGet(exchangeCD=u'XSHG,XSHE',beginDate=u'',endDate=u'',field=u'',pandas='1')
tradedaylist = tradedaylist[tradedaylist['isOpen']==1]
tradedaylist = tradedaylist[tradedaylist.calendarDate > '2007-01-01']
tradedaylist['mon'] = tradedaylist.calendarDate.apply(lambda x: x[5:7])
tradedaylist['year'] = tradedaylist.calendarDate.apply(lambda x: x[:4])
tradedaylist = tradedaylist.drop_duplicates(subset=['mon','year'], keep='first')
t_date = tradedaylist.loc[tradedaylist.mon.isin(['05']),:]['calendarDate'].values
t_date = [datetime.datetime.strptime(x, '%Y-%m-%d') for x in t_date]

start = '2015-01-01'
end = '2017-12-31'
universe = DynamicUniverse('HS300')
benchmark = 'HS300'
freq = 'd'
refresh_rate = 1
commission = Commission(0.0013, 0.0013)
accounts = {
    'security_account': AccountConfig(account_type='security', capital_base=1000000)
}

def initialize(context):
    pass

def handle_data(context):
    account = context.get_account('security_account')
    if context.current_date in t_date:
        position = account.get_positions()
        buy_list = MichaelHiggins(context.get_universe(exclude_halt=True), context.previous_date)
        if len(position) >0:
            # 获取当日停牌secID
            notopen = DataAPI.MktEqudGet(tradeDate=context.now,secID=position.keys(),isOpen='0',field=u'secID',pandas='1')
            sum_ = 0
            # 计算停牌secID权益
            for sec in notopen.secID:
                tmp = account.get_position(sec).value
                sum_ += tmp
            buyweight = 1.0 - sum_ / account.portfolio_value
        else:
            buyweight = 1.0
        for stk in position:
            if stk not in buy_list:
                account.order_to(stk,0)
        if len(buy_list) > 0:
            weight = buyweight/len(buy_list)
        else:
            weight = 0
        for stk in buy_list:
            account.order_pct_to(stk,weight)
