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

