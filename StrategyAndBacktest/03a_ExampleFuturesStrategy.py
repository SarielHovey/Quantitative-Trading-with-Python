start = '2016-12-15'  
end = '2016-12-19'    
universe = ['IFM0']  # 沪深300期货
benchmark = 'HS300'
capital_base = 600000
freq = 'm'          
refresh_rate = 1
  
commission = Commission(buycost=0.0001, sellcost=0.0002, unit='perValue')
slippage = Slippage(value=0, unit='perValue')

accounts = {
    'futures_account': AccountConfig(account_type='futures', capital_base=capital_base, commission=commission, slippage=slippage)
}
  
def initialize(context):
    pass

# 类已无法使用,尝试修改中
def handle_data(context):  
    
    futures_account = context.get_account('futures_account')
    symbol = context.get_symbol(universe[0])
    if context.current_minute == '09:30':
        futures_account.order(symbol, 10, 'open')
        
    elif context.current_minute == '09:36':
        long_pos = futures_account.get_positions().get(symbol,dict()).long_amount
        if long_pos > 0:
            futures_account.order(symbol, -long_pos, 'close')
            
    elif context.current_minute < '09:36':
        if len(futures_account.get_positions()) > 0 and futures_account.get_positions().get(symbol).today_profit<-5000:
            long_pos = futures_account.get_positions().get(symbol, dict()).long_amount
            if long_pos > 0:
                futures_account.order(symbol, -long_pos, 'close')


