import scipy.integrate as sci; import numpy as np
%load_ext Cython
def f(x):
        return np.sin(x) + 0.5 * x

#       建立np array, 50个元素
x = np.linspace(0, 10)
y = f(x)
#       积分左区间
a = 0.5
#       积分右区间
b = 9.5
Ix = np.linspace(a, b)
Iy = f(Ix)

#       高斯积分法
sci.fixed_quad(f, a, b)
#>(24.366995967084602, None)


#       面积法
sci.quad(f, a, b)
#>(24.374754718086752, 2.706141390761058e-13)


#       Romberg Integration
sci.romberg(f, a, b)
#>24.374754718086713


#       使用Monte Carlo模拟求解积分
x = np.random.random(1000) * (b - a) + a
result = np.mean(f(x)) * (b - a)
result
#>Out[20]: 24.409124452679745


