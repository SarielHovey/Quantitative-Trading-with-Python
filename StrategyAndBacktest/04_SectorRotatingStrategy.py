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
    global index_symbol
    index_symbol = DataAPI.IndustryGet(industryVersion=u'SW',industryVersionCD=u'',industryLevel=u'1',isNew=u'1',field=u'',pandas='1')['indexSymbol'].tolist()
    # 加上后缀以调用API
    index_symbol1 = [str(item) + '.ZICN' for item in index_symbol]
    symbol_history_list = []
    for symbol in index_symbol1:
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

# Transform Daily Price to Monthly Price
def getMonthlyIndex(df_index):
    """
    Daily Data to Monthly Data
    """
    # Transfar Column 'tradeDate' into Datetime Object
    # 使用index方法提取出日期作为列加入原DataFrame
    # Caution: 必须加上copy()方法, 否则py将同时更改行标签(愚蠢的引用)
    A = df_index.index.copy()
    A = pd.to_datetime(A, format='%Y-%m-%d')
    A = A.strftime('%Y-%m')
    df_index['year_month'] = A
    # head(1)保证了返回每月第一个交易日的数据
    return(df_index.groupby(['year_month']).head(1))

# 得到月度价格数据
df_monthly_industry_unstack = getMonthlyIndex(df_daily_industry_unstack[:])
# 删除已不再需要的列
del(df_monthly_industry_unstack['year_month'])

# pct_change方法可直接得出每期百分比变化, axis=0表示逐行计算
df_monthly_industry_return = df_monthly_industry_unstack.pct_change(axis=0)
# 去除均为NA的第一行
df_monthly_industry_return = df_monthly_industry_return.dropna(how='all')

# rank方法排序, axis=1表示在同一行的不同列之间排序
df_monthly_industry_return_rank = df_monthly_industry_return.rank(axis=1)

def get_corr(ind1, ind2, df_ind):
    """
    返回1与2的一阶滞后相关系数
    Args:
        ind1 (str); ind2 (str)
        df_ind (pd.DataFrame) consists of ind1 and ind2
    Returns:
        numpy.float64 Correlation Coefficient for ind1 --> [AR(1) for ind2]
    """
    x = df_ind[ind1].iloc[0:-1].values
    y = df_ind[ind2].iloc[1:].values
    return np.corrcoef(x,y)[0][1]

predict_corr = {}
# itertools.product用于替代嵌套for循环生成笛卡尔积. repeat=2下返回元组,每个元素为2
for item in itertools.product(index_symbol, repeat=2):
    predict_corr[item] = get_corr(item[0],item[1],df_monthly_industry_return_rank)

predict_corr = pd.Series(predict_corr)
predict_corr.hist()

# Check t-test
#$t = \frac{r \sqrt{n-2}}{1-r^3} , df= n-2$
#$t_{(34)0.01} = 2.728$ $\Longrightarrow$ $|r|=0.43$

# 按照t检验,在99%置信度下,相关系数需要超过0.43
filter_corr = predict_corr[abs(predict_corr) > 0.43]
filter_corr.sort_values(ascending=0)

#>801760  801140    0.465998
#>        801730    0.447453
#>        801790   -0.486136
#>dtype: float64
# 这4个行业之间符合要求

