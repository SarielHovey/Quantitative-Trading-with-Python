# Initialize in Uqer
start = '2016-01-15'                       # 回测起始时间
end = '2016-06-01'                         # 回测结束时间
universe = ['IFM0', 'SRM0','RBM0','TFM0']       # 证券池，支持股票、基金、期货、指数四种资产
benchmark = 'HS300'                        # 策略参考标准
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1                           # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟
  
# 配置账户信息，支持多资产多账户
accounts = {
    'futures_account': AccountConfig(account_type='futures', capital_base=10000000)
}
  
def initialize(context):
    pass
  
def handle_data(context):    
    futures_account = context.get_account('futures_account')
    for symbol in universe:
# context.get_rolliing_tuple()方法返回一个tuple(a,b); 表示期货合约映射关系变化前后
        symbol_bf, symbol_af = context.get_rolling_tuple(symbol)
# 以下if打印出了2016-01-15至2016-06-01期间主力期货合约的映射变化
        if symbol_bf != symbol_af:
            print("{0}: {1} -> {2}".format(context.current_date, symbol_bf, symbol_af))

#>2016-01-15 00:00:00: IF1601 -> IF1602
#>2016-02-15 00:00:00: TF1603 -> TF1606
#>2016-02-18 00:00:00: IF1602 -> IF1603
#>2016-03-02 00:00:00: SR605 -> SR609
#>2016-03-14 00:00:00: RB1605 -> RB1610
#>2016-03-18 00:00:00: IF1603 -> IF1604
#>2016-04-15 00:00:00: IF1604 -> IF1605
#>2016-04-29 00:00:00: TF1606 -> TF1609
#>2016-05-19 00:00:00: IF1605 -> IF1606



