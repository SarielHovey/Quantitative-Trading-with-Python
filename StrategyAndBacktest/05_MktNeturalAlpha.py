# This strategy typically long stocks and Short futures
# 策略基于CAPM:
#CAPM: $E(R_p) = R_f + \beta * (R_m - R_f)$
#$ \beta_i = \frac{Cov(R_i,R_m)}{Var(R_m)} $
# 策略的目的在于构造长期稳定的自用组合,对冲Long stock的$\beta$; 从而避免择时,获得长期稳定的绝对收益
# 回测基于Uqer
from CAL.PyCAL import *         # This library is provided by Uqer for financial calculation
import numpy as np
from pandas import DataFrame

start = '2015-01-01'
end = '2017-07-01'
universe = DynamicUniverse('HS300') + ['IFL0', 'IFL1']      # IFL0为当月合约, IFL1为下月合约
benchmark = 'HS300'
capital_base = 10000000
freq = 'd'
refresh_rate = 1
cal = Calendar('China.SSE')
period = Period('-1B')

stock_commission = Commission(buycost=0.001, sellcost=0.002, unit='perValue')
futures_commission = Commission(buycost=0.001, sellcost=0.002, unit='perValue')
slippage = Slippage(value=0, unit='perValue')
  
accounts = {
    'stock_account': AccountConfig(account_type='security', capital_base=capital_base, commission=stock_commission, slippage=slippage),
    'futures_account' AccountConfig(account_type='futures', capital_base=capital_base, commission=futures_commission, slippage=slippage)
}
  
def initialize(context):
    context.signal_generator = SignalGenerator(Signal('NetProfitGrowRate'),Signal('ROE'),Signal('RSI'))
    context.need_to_switch_position = False
    context.contract_holding = ''
  
def handle_data(context):
    universe = context.get_universe(exclude_halt=True)

    yesterday = context.previous_date
    signal_composit = DataFrame()

    # Signal for Net Profit Growth Rate
    NetProfitGrowRate = context.signal_result['NetProfitGrowRate']
    signal_NetProfitGrowRate = standardize(neutralize(winsorize(NetProfitGrowRate), yesterday.strftime('%Y%m%d')))
    signal_composit['NetProfitGrowRate'] = signal_NetProfitGrowRate

    # Signal for ROE
    ROE = context.signal_result['ROE']
    signal_ROE = standardize(neutralize(winsorize(ROE), yesterday.strftime('%Y%m%d')))
    signal_composit['ROE'] = signal_ROE

    # Signal for RSI
    RSI = context.signal_result['RSI']
    signal_RSI = standardize(neutralize(winsorize(RSI), yesterday.strftime('%Y%m%d')))
    signal_composit['RSI'] = signal_RSI

    # 合成信号并设置3个因子权重. np.dot用于计算矩阵积
    weight = np.array([0.6,0.3,0.1])
    signal_composit['total_score'] = np.dot(signal_composit, weight)

    # 构建组合
    total_score = signal_composit['total_score'].to_dict()
    wts = simple_long_only(total_score, yesterday.strftime('%Y%m%d'))
    handle_stock_orders(context, wts)
    handle_futures_orders(context)
    # handle_futures_position_switch(context)

# 下单
def handle_stock_orders(context, wts):
    account = context.get_account('stock_account')
    sell_list = account.get_positions()
    for stk in sell_list:
        account.order_to(stk, 0)

    buy_list = wts.keys()
    total_money = account.portfolio_value
    prices = account.reference_price
    for stk in buy_list:
        if np.isnan(prices[stk]) or prices[stk] == 0:       # 停牌或未上市
            continue
        account.order(stk, int(total_money * wts[stk] / prices[stk] /100)*100)




def handle_futures_orders(context):
    stock_account = context.get_account('stock_account')
    future_account = context.get_account('futures_account')
    # 使用实际合约映射主力连续合约
    contract_current_month = context.get_symbol('IFL0')

    # 判断是否需要移仓换月
    contract_holding = context.contract_holding
    if not contract_holding:
        contract_holding = contract_current_month
    else:
        last_trade_date = get_asset(contract_holding).last_trade_date
        days_to_expire = (last_trade_date - context.current_date).days
        if days_to_expire == 3:
            log.info(u'距离到期,还有%s天' % (contract_holding, days_to_expire))
            contract_next_month = context.get_symbol('IFL1')
            futures_position = future_account.get_position(contract_holding)
            if futures_position:
                current_holding = futures_position.short_amount
                log.info(u'移仓换月. [旧%s, 新%s, 共%s手.]' % (contract_holding, contract_next_month, int(current_holding)))
                if current_holding == 0:
                    return
                future_account.order(contract_holding, current_holding, 'close')
                future_account.order(contract_next_month, -1*current_holding, 'open')
                context.contract_holding = contract_next_month
                return
    stock_position = stock_account.get_positions()
    # 使用空头期货对冲多头股票
    if stock_position:
        stock_positions_value = stock_account.portfolio_value - stock_account.cash
        # print(u'当前股票市值 ', stock_positions_value )
        futures_position = future_account.get_position(contract_holding)
        # 若无期货空头则建仓
        if not futures_position:
            contract_current_month = context.get_symbol('IFL0')
            multiplier = get_asset(contract_current_month).multiplier
            futures_price = context.current_price(contract_current_month)
            total_hedging_amount = int(stock_positions_value / futures_price / multiplier)
            log.info(u'%s未期货建仓, 空头开仓%s手' % (contract_current_month, contract_holding))
            future_account.order(contract_current_month, -1*total_hedging_amount, 'open')
            context.contract_holding = contract_current_month
        # 若有期货空头则调仓
        else:
            contract_holding = context.contract_holding
            contract_current_month = context.get_symbol('IFL0')
            futures_price = context.current_price(contract_current_month)
            multiplier = get_asset(contract_holding).multiplier
            # 计算hedge需要的期货手数
            total_hedging_amount = int(stock_positions_value / futures_price / multiplier)
            hedging_amount_diff = total_hedging_amount - futures_position.short_amount
            # 调仓阈值, 调大则减少调仓频率
            threshold = 2
            if hedging_amount_diff >= threshold:
                log.info(u'空头调仓. [合约:%s, 当前空头手数:%s, 目标空头手数:%s]' %(contract_holding, int(futures_position.short_amount), total_hedging_amount))
                # 多开空仓
                future_account.order(contract_holding, -1*int(hedging_amount_diff), 'open')
            elif hedging_amount_diff <= (-threshold):
                log.info(u'空头调仓. [合约:%s, 当前空头手数:%s, 目标空头手数:%s]' %(contract_holding, int(futures_position.short_amount), total_hedging_amount))
                # 减少空仓
                future_account.order(contract_holding, int(abs(hedging_amount_diff)), 'close')


