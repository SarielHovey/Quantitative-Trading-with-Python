%load_ext Cython
%%cython
import scipy.optimize as sco
import numpy as np
cdef float x = 0.00
cdef float y = 0.00
cdef float z = 0.00
def fo(p):
        x, y = p
        z = np.sin(x) + 0.05 * x  ** 2 + np.sin(y) + 0.05 * y ** 2
        print('%8.4f    |   %8.4f    |    %8.4f'        %       (x, y, z))
        return z

#       Use Brute Force Optimization for Global Optimization
##      以5为步进, 全局最小值为(0, 0, 0)
sco.brute(fo, ((-10.0, 10.1, 5), (-10.0, 10.1, 5)), finish=None) 
"""
-10.0000    |   -10.0000    |     11.0880
-10.0000    |    -5.0000    |      7.7529
-10.0000    |     0.0000    |      5.5440
-10.0000    |     5.0000    |      5.8351
-10.0000    |    10.0000    |     10.0000
 -5.0000    |   -10.0000    |      7.7529
 -5.0000    |    -5.0000    |      4.4178
 -5.0000    |     0.0000    |      2.2089
 -5.0000    |     5.0000    |      2.5000
 -5.0000    |    10.0000    |      6.6649
  0.0000    |   -10.0000    |      5.5440
  0.0000    |    -5.0000    |      2.2089
  0.0000    |     0.0000    |      0.0000
  0.0000    |     5.0000    |      0.2911
  0.0000    |    10.0000    |      4.4560
  5.0000    |   -10.0000    |      5.8351
  5.0000    |    -5.0000    |      2.5000
  5.0000    |     0.0000    |      0.2911
  5.0000    |     5.0000    |      0.5822
  5.0000    |    10.0000    |      4.7471
 10.0000    |   -10.0000    |     10.0000
 10.0000    |    -5.0000    |      6.6649
 10.0000    |     0.0000    |      4.4560
 10.0000    |     5.0000    |      4.7471
 10.0000    |    10.0000    |      8.9120
Out[6]: array([0., 0.])
"""

##      以0.1为步进暴力计算全局最小值, 显示取值点为(-1.4, -1,4)
opt1 = sco.brute(fo, ((-10.0, 10.1, 0.1), (-10.0, 10.1, 0.1)), finish=None)
opt1
#>Out[8]: array([-1.4, -1.4])



#       Use scipy.optimization.fmin() for Local Optimization
##      注意参数2表示在全局最小值点的附近搜寻; 此方法对局部位置的选取敏感
opt2 = sco.fmin(fo, opt1, xtol=0.001, ftol=0.001, maxiter=15, maxfun=20)
opt2                                                                                                                                  
#>Out[16]: array([-1.42702972, -1.42876755])

##      一个不好的初始位置会得出错误结果
opt3 = sco.fmin(fo, (2.0,2.0), maxiter=250)
'''
Optimization terminated successfully.
         Current function value: 0.015826
         Iterations: 46
         Function evaluations: 86
'''
opt3
#>Out[18]: array([4.2710728 , 4.27106945])



#       Use scipy.optimization.minimize() for Constrained Optimization
##      cython中不要使用's, b = p', 否则会报错, 因为对应的C Object不可迭代
%%cython
from numpy import sqrt
cdef double s
cdef double b
def Eutility(p):
        s = p[0]
        b = p[1]
        return -(0.5 *sqrt(s * 15 + b * 5) + 0.5 * sqrt(s * 5 + b * 12))

##      以字典的形式设置不等式约束
cons = ({'type': 'ineq', 'fun': lambda p: 100 - p[0] * 10.0 - p[1] * 10.0})
##      设定边界条件
bnds = ((0, 1000), (0, 1000))
result = sco.minimize(Eutility, [5,5], method='SLSQP', bounds=bnds, constraints=cons)
result
'''
Out[43]: 
fun: -9.700883611487832
jac: array([-0.48508096, -0.48489535])
message: 'Optimization terminated successfully.'
nfev: 21
nit: 5
njev: 5
status: 0
success: True
x: array([8.02547122, 1.97452878])
'''
##      查看最小值点
result['x']
#>Out[44]: array([8.02547122, 1.97452878])
##      查看最大值(函数乘以-1的最小值即为原函数的最大值))
-result['fun']
#>Out[45]: 9.700883611487832
##      查看是否仍满足约束条件
np.dot(result['x'], [10,10])
#>99.999999999999999999999

