import tushare as ts; import pandas as pd; import numpy as np; import matplotlib.pyplot as plt
import scipy.optimize as sco
pro = ts.pro_api()
df_temp = pd.read_csv("/mnt/d/R_Quant/HS300.csv",encoding='UTF8',dtype={'IncludeDate':str, 'Ticker':str})
list300 = df_temp.Ticker.tolist()
for i in range(0,300):
    if list300[i][:2] == '00' or list300[i][:2] == '30':
        list300[i] = list300[i] + '.SZ'
    elif list300[i][:2] == '60':
        list300[i] = list300[i] + '.SH'


DATA = pd.DataFrame()
for i in list300:
    df_temp = ts.pro_bar(ts_code= i, adj='qfq', start_date='20160101',end_date='20191111')
    DATA = DATA.append(df_temp)


DATA.info()
'''
<class 'pandas.core.frame.DataFrame'>
Int64Index: 260094 entries, 0 to 843
Data columns (total 11 columns):
ts_code       260094 non-null object
trade_date    260094 non-null object
open          260094 non-null float64
high          260094 non-null float64
low           260094 non-null float64
close         260094 non-null float64
pre_close     260094 non-null float64
change        260094 non-null float64
pct_chg       260094 non-null float64
vol           260094 non-null float64
amount        260094 non-null float64
dtypes: float64(9), object(2)
memory usage: 23.8+ MB
'''

DATA.head(7)
'''
     ts_code trade_date    open    high     low   close  pre_close  change  pct_chg       vol      amount
0  000596.SZ   20191111  109.22  109.88  106.36  107.30     110.12   -2.82  -2.5608  22112.42  238990.677
1  000596.SZ   20191108  111.66  112.62  109.68  110.12     111.66   -1.54  -1.3792  24732.93  274589.898
2  000596.SZ   20191107  112.98  112.98  110.81  111.66     112.01   -0.35  -0.3125  13989.38  156369.357
3  000596.SZ   20191106  112.15  112.67  110.64  112.01     112.98   -0.97  -0.8586  17777.59  198800.971
4  000596.SZ   20191105  113.99  114.14  111.40  112.98     114.15   -1.17  -1.0250  24025.77  270352.039
5  000596.SZ   20191104  111.40  114.72  111.01  114.15     110.73    3.42   3.0886  30640.34  348407.828
6  000596.SZ   20191101  111.40  111.73  108.66  110.73     110.40    0.33   0.2989  23052.32  254095.470
'''

Cls = DATA.pivot(index='trade_date',columns='ts_code',values='close')
Cls = Cls.dropna(axis=1, how='any')
Rtn = np.log(Cls/Cls.shift(1))
Rtn.shape
'''
(939, 102)
'''

weights = np.random.random(Rtn.shape[1])

Rtn = Rtn.dropna(axis=0)

def port_rtn(weights):
    return np.sum(Rtn.mean() * weights) * 252
def port_vol(weights):
    return np.sqrt(np.dot(weights.T,np.dot(Rtn.cov() * 252, weights)))
Prtn = []; Pvol = []



#   Generate Efficient Frontier based on Monte Carlo
for p in range(2500):
    weights = np.random.random(Rtn.shape[1])
    weights /= np.sum(weights)
    Prtn.append(port_rtn(weights))
    Pvol.append(port_vol(weights))

Prtn = np.array(Prtn)
Pvol = np.array(Pvol)

plt.figure(figsize=(10, 6))
plt.scatter(Pvol, Prtn, c=Prtn/Pvol, marker='o', cmap='coolwarm')
plt.xlabel('expected Vol')
plt.ylabel('expected Rtn')
plt.colorbar(label='Sharp Ratio')
plt.show()



#   Calculate Optimal Portfolio
def min_sharpe(weights):
    return -port_rtn(weights)/port_vol(weights)

cons = ({'type':'eq','fun': lambda x: np.sum(x) - 1})
bounds = tuple((0,1) for x in range(Rtn.shape[1]))

initial_wt = np.array(Rtn.shape[1] * [1. / Rtn.shape[1]])

opti = sco.minimize(min_sharpe, initial_wt, method='SLSQP', bounds=bounds, constraints=cons)
'''
     fun: -1.6878726800913604
     jac: array([ 4.26154748e-01,  1.09029174e+00,  4.03992727e-01,  1.18389817e+00,
        1.40436620e+00,  6.38587311e-01,  1.19156833e+00,  9.65696111e-01,
        8.18461791e-01,  1.17653777e+00,  1.18276918e+00,  1.44201130e+00,
        1.54290378e-01,  9.29931775e-01,  1.13728313e+00,  2.01529741e-01,
        9.37892854e-01,  2.02780703e+00,  1.51289904e+00,  8.94545704e-01,
        1.33023560e-01,  8.77212718e-01,  3.61574054e-01,  1.43367690e+00,
        1.27437444e+00, -9.76666808e-04,  2.20778033e-01,  6.66024715e-01,
        2.54489988e-01,  8.28326806e-01,  1.28840469e+00,  1.26121140e+00,
        1.10117593e+00,  1.66581711e+00,  6.77745640e-02,  3.17028552e-01,
        4.89546627e-01,  8.63716006e-04,  7.24027738e-01,  8.04432705e-01,
        5.50406829e-01,  9.81313199e-01,  1.08753797e+00,  2.97283903e-01,
        6.09010011e-02, -4.21628356e-04,  8.72139454e-01,  1.13398324e+00,
        1.08912514e+00,  1.41321738e+00,  4.87257391e-01,  1.57922773e+00,
        1.16095473e+00,  1.54947162e+00,  5.89014009e-01,  1.74501859e+00,
        1.31776021e+00,  1.58551802e+00,  3.43906596e-01, -5.45382500e-06,
        1.60471846e+00,  9.86780450e-01,  1.08769274e+00, -8.29562545e-04,
        1.57487778e+00,  3.69341090e-01,  5.51394537e-01,  9.87557516e-01,
        1.18090072e+00,  1.38121766e+00,  4.09235314e-01,  8.91234308e-01,
        3.86492297e-01,  1.11049965e+00,  4.81763124e-01,  1.06244704e+00,
        1.18313794e+00,  1.93686575e+00,  1.15789694e+00,  2.28399381e-01,
        1.04724616e-01,  5.06602824e-02,  3.31200913e-01,  1.29178829e+00,
        4.10765857e-02,  7.24886551e-01,  8.90941411e-01,  1.54514815e+00,
        7.23268226e-01,  5.20013705e-01,  1.10092196e+00,  1.63014881e+00,
        1.17319191e+00,  6.95978552e-01,  8.51124823e-01,  3.82082313e-02,
        9.53316376e-01,  2.05851600e-01,  1.23113571e+00,  3.18263158e-01,
        6.04169309e-01,  1.16880238e-03])
 message: 'Optimization terminated successfully.'
    nfev: 833
     nit: 8
    njev: 8
  status: 0
 success: True
       x: array([0.00000000e+00, 2.25768672e-15, 0.00000000e+00, 0.00000000e+00,
       1.33606416e-15, 2.79651261e-15, 2.63913591e-16, 0.00000000e+00,
       0.00000000e+00, 2.90124424e-15, 4.42585875e-16, 1.60794918e-16,
       2.65429435e-14, 1.19923557e-15, 2.71742698e-15, 0.00000000e+00,
       1.53097062e-15, 2.94120845e-15, 3.70758677e-15, 0.00000000e+00,
       0.00000000e+00, 3.33583100e-16, 0.00000000e+00, 1.98191212e-15,
       3.20002660e-15, 5.16507858e-02, 0.00000000e+00, 1.22241918e-15,
       0.00000000e+00, 3.24283927e-16, 0.00000000e+00, 9.16157818e-16,
       1.92585560e-15, 1.28284248e-15, 0.00000000e+00, 0.00000000e+00,
       9.01077615e-16, 1.18422689e-01, 0.00000000e+00, 9.33653271e-17,
       0.00000000e+00, 9.19603858e-17, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 1.00424247e-01, 0.00000000e+00, 5.63784832e-16,
       1.94276682e-16, 1.21493719e-15, 0.00000000e+00, 8.14353289e-16,
       1.53641242e-15, 2.49704555e-15, 0.00000000e+00, 1.02908030e-15,
       7.94345582e-16, 3.64526443e-16, 0.00000000e+00, 5.91070093e-01,
       4.83679464e-16, 1.29951327e-15, 1.71675696e-15, 8.51598649e-02,
       1.75817582e-15, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       9.95251557e-16, 6.49304687e-16, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 7.21887850e-16, 0.00000000e+00, 5.94676876e-16,
       1.20123095e-15, 2.97594426e-15, 1.41426793e-15, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.03241413e-15,
       0.00000000e+00, 0.00000000e+00, 2.56427653e-16, 0.00000000e+00,
       0.00000000e+00, 0.00000000e+00, 1.47327154e-15, 1.28479855e-15,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       7.06474324e-17, 0.00000000e+00, 1.18160522e-15, 0.00000000e+00,
       0.00000000e+00, 5.32723205e-02])
'''

print('Optimal Portfolio Return: ' + str(port_rtn(opti['x']).round(6)))
'''
Optimal Portfolio Return: 0.401951
'''
print('Optimal Portfolio Volatility: ' + str(port_vol(opti['x']).round(6)))
'''
Optimal Portfolio Volatility: 0.238141
'''
print('Optimal Sharpe Ratio: ' + str(port_rtn(opti['x'])/port_vol(opti['x'])))
'''
Optimal Sharpe Ratio: 1.6878726800913604
'''

