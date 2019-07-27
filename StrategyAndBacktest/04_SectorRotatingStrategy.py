import numpy as np
import pandas as pd
import itertools
from datetime import datetime
from scipy import stats as ss
import matplotlib.pyplot as plt
import seaborn as sn
sn.set_style('white')

def get_sw_ind_quotation():
    """
    返回申万一级行业指数历史行情
    Args:
        opt(bool): 选择是否剔除综合行业,默认为False
    Returns:
        DataFrame: 申万一级行业指数日线行情
    Examples:
        >> df_daily_industry_unstack = get_sw_ind_quotation()
    """
    # 抓取共28个申万一级行业指数代码
    index_symbol = DataAPI.IndustryGet(industryVersion=u'SW',industryVersionCD=u'',industryLevel=u'1',isNew=u'1',field=u'',pandas='1')['indexSymbol'].tolist()
    # 加上后缀以调用API
    index_symbol = [str(item) + '.ZICN' for item in index_symbol]
    symbol_history_list = []
    for symbol in index_symbol:
        df_daily_industry_symbol = DataAPI.MktIdxdGet(beginDate='2015-01-01',endDate='2019-07-27',ticker=symbol[:6],field=u'ticker,tradeDate,closeIndex')
        symbol_history_list.append(df_daily_industry_symbol)

    df_daily_industry_symbol = pd.concat(symbol_history_list,axis=0)
    # 汇总获得的行业数据
    #df_daily_industry_unstack = df_daily_industry_symbol.set_index(['tradeDate','ticker']).unstack()['closeIndex']
    df_daily_industry_unstack = df_daily_industry_symbol.pivot(index='tradeDate', columns='ticker', values='closeIndex')
    return(df_daily_industry_unstack)
# 注意retrun()的缩进, 同时,u''中不可有空格,否则空格后参数会被API忽略导致数据缺失
df_daily_industry_unstack = get_sw_ind_quotation()
df_daily_industry_unstack.head()

# 判断数据框df_daily_industry_unstack中是否有NA值
print((df_daily_industry_unstack.isnull().any() * 1).sum())
# 此处利用了Bool值的计算特性. 结果为0表示无NA值
#>[1] 0 

# 使用index方法提取出日期作为列加入原DataFrame
df_daily_industry_unstack['tradeDate'] = df_daily_industry_unstack.index

# Transform Daily Price to Monthly Price
def getMonthlyIndex(df_index):
    """
    Daily Data to Monthly Data
    """
    # Transfar Column 'tradeDate' into Datetime Object
    ## parse()无定义 需要重构
    df_index['tradeDate'] = df_index['tradeDate'].map(lambda x: parse(x))
    df_index['year_month'] = df_index['tradeDate'].map(lambda x: (x.year, x.month))
    return(df_index.groupby(['year_month']).head(1))





