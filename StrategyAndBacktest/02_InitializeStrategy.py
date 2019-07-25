# 典型的Uqer策略框架
start = '2017-01-01'                       # 回测起始时间
end = '2018-01-01'                         # 回测结束时间
universe = DynamicUniverse('HS300')        # 证券池，支持股票、基金、期货、指数四种资产; 此处使用了动态沪深300库以防止幸存者偏误
# 证券池支持SH50,SH180,HS300,ZZ500,CYB,ZXB,A
benchmark = 'HS300'                        # 策略参考标准
# 可通过Uqer的内部secID获取benchmark, 如 benchmark = '000001.XSHE'
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1                           # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟
# refresh_rate可设为按week,month调仓. 如Weekly(1)在每周第1个交易日;Monthly(1,-1)在每月第1和最后1个交易日调仓
    
# 配置账户信息，支持多资产多账户; 下例提供了stock账户与futures账户
accounts = {
    'security_account': AccountConfig(account_type='security', capital_base=10000000, position_base={'000001.XSHE':1000, '600000.XSHG':2000}, cost_base={'000001.XSHE':12, '600000.XSHG':4.7}, commission = Commission(buycost=0.001, sellcost=0.002, unit='perValue'), slippage=Slippage(value=0.0, unit='perValue')),
    
    'futures_account': AccountConfig(account_type='futures', capital_base=10000000, commission=Commission(buycost=0.001, sellcost=0.002, unit='perValue'), slippage=Slippage(value=0.0, unit='perValue'), margin_rate=0.1)
}
  
def initialize(context):            #初始化策略运行环境
    pass


# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data(context):               # 核心策略逻辑
    # context.previous用于获取交易日前一日, 返回datatime
    previous_date = context.previous_date.strftime('%Y-%m-%d')
    
    # 获取策略运行的当前时刻与日期
    print(context.now)
    print(context.current_date)
    
    # 获取最后一次成交价. symbol需在Line04的universe中
    print(contex.current_price('00001.XSHE'))
    
    # 获取因子PE的的历史数据集，截止到前一个交易日
    # context.get_universe('stock',exclude_halt=True)获取当天universe的未停牌证券池
    hist = context.history(symbol=context.get_universe(exclude_halt=True), attribute='PE', time_range=1, style='tas')[previous_date]
     
    # 将因子值从小到大排序，并取前100支股票作为目标持仓
    signal = hist['PE'].order(ascending=True)
    target_position = signal[:100].index
     
    # 获取当前账户信息
    stock_account = context.get_account('security_account')   
    current_position = stock_account.get_positions(exclude_halt=True)       
     
    # 卖出当前持有，但目标持仓没有的部分
    for stock in set(current_position).difference(target_position):
        stock_account.order_to(stock, 0)
     
    # 根据目标持仓权重，逐一委托下单
    for stock in target_position:
        stock_account.order(stock, 10000)

    # 账户间资金划转
    futures_account = context.get_account('futures_account')
    if context.current_date.strfttime('%d')== '01'
        context.transfer_cash(origin=stock_account, target=futures_account, amount = 1e5)
