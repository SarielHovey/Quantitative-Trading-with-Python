import numpy as np
import scipy.interpolate as spi

x = np.linspace(-2 * np.pi, 2 * np.pi, 50)
def f(x):
        return np.sin(x) + 0.5  * x

#       k = 1 means Linear Interpolation
ipo = spi.splrep(x, f(x), k=1)
#       生成经过Linear Interpolation的曲线
iy = spi.splev(x, ipo)
#       比对生成的iy与f(x), 结果显示2者匹配
np.allclose(f(x), iy)
#>      True
