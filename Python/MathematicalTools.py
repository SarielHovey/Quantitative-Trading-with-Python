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
#       回归结果为一条斜率为0.4, 通过原点的直线
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
