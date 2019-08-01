import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')
from scipy.optimize import minimize
from cvxopt import matrix, solvers
from datetime import datetime as dt
from CAL.PyCal import font
def get_convmat(tickers, date, periods):
    '''
    输入tickers + 日期 + 过期天数, 获得年化协方差矩阵
    '''
    start_date = shift_date(date, periods)
    return_mat = DataAPI.MktEqudAdjGet(ticker=tickers, beginDate=start_date, endDate=date, field=u'ticker,tradeDate,closePrice',pandas='1')
    return_mat = return_mat.pivot(index='tradeDate',columns='ticker',values='closePrice').pct_change().fillna(0.0)
    return(return_mat.cov()*252)

