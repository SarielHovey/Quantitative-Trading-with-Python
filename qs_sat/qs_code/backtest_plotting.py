import pandas as pd
import matplotlib.pyplot as plt

aapl = pd.read_csv('equity.csv',encoding='UTF-8')
print(aapl.head())

aapl.loc[:,'datetime'] = aapl.loc[:,'datetime'].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d'))

plt.figure(figsize=(8,8),dpi=80)

plt.subplot(311)
plt.plot(aapl.datetime, aapl.equity_curve, label='Equity Curve')
plt.grid(True)
plt.ylabel('Portfolio Value')
plt.legend()

plt.subplot(312)
plt.plot(aapl.datetime, aapl.returns, label='Period Returns')
plt.grid(True)
plt.ylabel('Period Returns, %')


plt.subplot(313)
plt.plot(aapl.datetime, aapl.returns, label='Draw Down, %')
plt.grid(True)
plt.ylabel('Draw Down, %')

plt.gcf().autofmt_xdate()