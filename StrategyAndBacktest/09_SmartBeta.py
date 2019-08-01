import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')
from scipy.optimize import minimize
from cvxopt import matrix, solvers
from datetime import datetime as dt
from CAL.PyCAL import font
def get_convmat(tickers, date, periods):
    '''
    输入tickers + 日期 + 过期天数, 获得年化协方差矩阵
    '''
    start_date = shift_date(date, periods)
    return_mat = DataAPI.MktEqudAdjGet(ticker=tickers, beginDate=start_date, endDate=date, field=u'ticker,tradeDate,closePrice',pandas='1')
    return_mat = return_mat.pivot(index='tradeDate',columns='ticker',values='closePrice').pct_change().fillna(0.0)
    return(return_mat.cov()*252)

def get_smart_weight(cov_mat, method='min variance', wts_ad):
    '''
    功能: 输入协方差矩阵, 得到优化后的权重配置. Need Scipy package
    Imput:
        cov_mat: pd.DataFrame, 为协方差矩阵, index与column均为资产名称
        method 优化方法, 值可为min variance, risk parity, max diversification, equal weight
    Output:
        pd.Series, index为资产名, values为weight
    '''
    if not isinstance(cov_mat, pd.DataFrame):
        raise ValueError('cov_mat should be pandas DataFrame!')

    omega = np.matrix(cov_mat.values)   # 得出协方差矩阵
    # 定义目标函数
    def fun1(x):
        return(np.matrix(x) * omega * np.matrix(x).T)

    def fun2(x):
        # A1将matrix一维展开成ndarray
        tmp = (omega * np.matrix(x).T).A1
        risk = x * tmp
        delta_risk = [sum((i-risk)**2) for i in risk]
        return(sum(delta_risk))

    def fun3(x):
        den = x * omega.diagonal().T
        num = np.sqrt(np.matrix(x) * omega * np.matrix(x).T)
        return(num/den)

    # 初始值+约束条件
    x0 = np.ones(omega.shape[0]) / omega.shape[0]
    bnds = tuple((0,None) for x in x0)
    cons = ({'type':'eq', 'fun': lambda x: sum(x) - 1})
    options = {'disp':False, 'maxiter':1000, 'ftol':1e-20}

    if method == 'min variance':
        res = minimize(fun1, x0, bounds=bnds, constraints=cons, method='SLSQP', options=options)
    elif method == 'risk parity':
        res = minimize(fun2, x0, bounds=bnds, constraints=cons, method='SLSQP', options=options)
    elif method == 'max diversification':
        res = minimize(fun3, x0, bounds=bnds, constraints=cons, method='SLSQP', options=options)
    elif method == 'equal weight':
        return(pd.Series(index=cov_mat.index, data=1.0/cov_mat.shape[0]))
    else:
        raise ValueError('Method should be min variance/risk parity/max diversification/equal weight.')

        # 权重调整
        if res['success'] == False:
            # print(res['message'])
            pass
        wts = pd.Series(index=cov_mat.index, data=res['x'])
        if wts_adjusted == True:
            wts = wts[wts >= 0.0001]
            return(wts / wts.sum() * 1.0)
        elif wts_adjusted == False:
            return(wts)
        else:
            raise ValueError('wts_adjusted should be True/False.')