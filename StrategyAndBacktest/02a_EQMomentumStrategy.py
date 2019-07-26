# Initialize on Uqer platform
# This is a typical momentum strategy for EQ, but out of sample test from 2018-01-01 to 2019-07-25 proves it to be unsuccessful
import pandas as pd
start = '2014-01-01'
end = '2018-01-01'
universe = DynamicUniverse('HS300')
benchmark = 'HS300'
freq = 'd'
refresh_rate = 60
## max_history_window must >= context.history() time length
max_history_window = 80
    
accounts = {
    'security_account': AccountConfig(account_type='security', capital_base=10000000, commission = Commission(buycost=0.001, sellcost=0.002, unit='perValue'), slippage=Slippage(value=0.0, unit='perValue'))
}
  
def initialize(context):
    pass
def handle_data(context):
    
    account = context.get_account('security_account')
    universe = context.get_universe(exclude_halt=True)
    history = context.history(universe, 'closePrice', 80)
    momentum = {'symbol':[], 'c_return':[]}
    for stk in history.keys():
        momentum['symbol'].append(stk)
        momentum['c_return'].append(history[stk]['closePrice'][-1]/history[stk]['closePrice'][0])
        
    momentum = pd.DataFrame(momentum).sort(columns='c_return',ascending=False).reset_index()
## Get the first 80 stocks with highest closePrice{today}/closePrice{80 days ago}
    momentum = momentum[:80]
    buylist = momentum['symbol'].tolist()
    
    for stk in account.get_positions():
        if stk not in buylist:
            account.order_to(stk, 0)
            
    portfolio_value = account.portfolio_value
    for stk in buylist:
        account.order_pct_to(stk, 1.0/len(buylist))



        
