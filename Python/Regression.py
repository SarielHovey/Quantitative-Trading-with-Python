import numpy as np                                                                                                                     
from pylab import plt, mpl                                                                                                           
plt.style.use('seaborn')                                                                                                               
mpl.rcParams['font.family'] = 'serif'
#       %matplotlib inline

def f(x):
        return np.sin(x) + 0.5 * x

def create_plot(x, y, styles, labels, axlabels):
        plt.figure(figsize=(10,6))
        for i in range(len(x)):
                plt.plot(x[i],  y[i], styles[i], label=labels[i])
                plt.xlabel(axlabels[0])
                plt.ylabel(axlabels[1])
        plt.legend(loc=0)
        plt.show()

#       Set a np array from -2 pi to 2 pi, consisting 50 elements
x = np.linspace(-2 * np.pi, 2* np.pi, 50) 

create_plot([x], [f(x)], ['b'], ['f(x)'], ['x', 'f(x)']) 



#       Regression with Least Squares Method
res = np.polyfit(x, f(x), deg=1, full=True)
res                                                                                                                                   
#Out[16]: 
#       回归结果为一条斜率为0.4的直线
#(array([ 4.28841952e-01, -5.69158516e-17]),
 #array([21.03238686]),
 #2,
 #array([1., 1.]),
 #1.1102230246251565e-14)

#       使用7阶多项式拟合f(x)
res = np.polyfit(x, f(x), deg=7, full=True)
res
"""
(array([-5.47508597e-05,  9.96245105e-19,  4.99394999e-03, -3.27841038e-17,
        -1.35368487e-01,  3.43358409e-16,  1.41870278e+00, -5.37562408e-16]),
 array([0.08884567]),
 8,
 array([1.9224113 , 1.83844254, 0.75277939, 0.53867891, 0.22886461,
        0.11804067, 0.0327599 , 0.01504008]),
 1.1102230246251565e-14)
"""

#       使用矩阵方法拟合f(x), 基于 np.linalg.lstsq()
mtrx = np.zeros((3+1, len(x)))
mtrx[3, :] = x ** 3
mtrx[2, :] = x ** 2
mtrx[1, :] = x ** 1
mtrx[0, :] = 1

reg = np.linalg.lstsq(mtrx.T, f(x), rcond=None)
"""
(array([ 1.16778801e-14,  5.62777448e-01, -8.88178420e-16, -5.43553615e-03]),
 array([18.70019638]),
 4,
 array([703.78757296, 130.00970131,  10.44694523,   4.7085911 ]))
 """

#       这个方法的价值在于能够手动指定参数个数与使用的函数
mtrx[3, :] = np.sin(x)
reg2 = np.linalg.lstsq(mtrx.T, f(x), rcond=None)
#       可以看到, 0.5 与1 被完美的拟合出来了,而x0与x1的系数几乎为0
#       拟合结果为 0 * x0 + 0.5 * x1 + 0 * x2 + 1 * x3; 这与手动设定的f(x)一致
"""
(array([4.36463437e-16, 5.00000000e-01, 0.00000000e+00, 1.00000000e+00]),
 array([1.51928882e-29]),
 4,
 array([130.00970131,  26.23750347,   4.7085911 ,   4.57417802]))
"""


