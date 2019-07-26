# Initialize in Uqer
# An example for context.get_rolling_tuple()
start = '2016-01-15'                       
end = '2016-06-01'                        
universe = ['IFM0', 'SRM0','RBM0','TFM0']   
benchmark = 'HS300'                   
freq = 'd'                         
refresh_rate = 1      
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






# An example for account.switch_position() 用于调仓
start = '2016-12-15'           
end = '2016-12-19'        
universe = ['IFM0']      
benchmark = 'HS300'              
freq = 'd'                         
refresh_rate = 1            
  
accounts = {
    'futures_account': AccountConfig(account_type='futures', capital_base=10000000)
}
  
def initialize(context):
    pass
  
def handle_data(context):  
    print(context.current_date)
    futures_account = context.get_account('futures_account')
    current_date = context.current_date.strftime('%Y-%m-%d')
    
    if current_date == "2016-12-15":
        symbol_bf, symbol_af = context.get_rolling_tuple('IFM0')
        print(symbol_bf, symbol_af)
        futures_account.order(symbol_af, 3, 'open')
        print(futures_account.position)
    elif current_date == "2016-12-16":
        symbol_bf, symbol_af = context.get_rolling_tuple('IFM0')
        print(symbol_bf, symbol_af)
        futures_account.switch_position(symbol_bf, symbol_af)
        print(futures_account.position)
    elif current_date == "2016-12-19":
        symbol_bf, symbol_af = context.get_rolling_tuple('IFM0')
        print(symbol_bf, symbol_af)
        print(futures_account.position)

#>2016-12-15 00:00:00
#>('IF1612', 'IF1612')
{}
#>2016-12-16 00:00:00
#>('IF1612', 'IF1701')
#>{'IF1612': FuturesPosition(long_amount: 3.0, short_amount: 0.0, long_margin: 1197936.0, short_margin: 0.0, long_cost: 3364.0, short_cost: 0.0, price: 3327.6, today_profit: 0.0, profit: -32760.0)}
#>2016-12-19 00:00:00
#>('IF1701', 'IF1701')
#>{'IF1701': FuturesPosition(long_amount: 3.0, short_amount: 0.0, long_margin: 1193760.0, short_margin: 0.0, long_cost: 3306.0, short_cost: 0.0, price: 3316.0, today_profit: 0.0, profit: 9000.0)}




