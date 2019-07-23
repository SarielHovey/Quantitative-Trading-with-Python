#library(reticulate)
#repl_python()
#>Python 3.7.3 (C:\PROGRA~3\ANACON~1\python.exe)
#>Reticulate 1.12 REPL -- A Python interpreter in R.

import numpy as np

# Initialize a NumPy array
data = [1,2,3,4]
arr = np.array(data)
arr
#>[1] array([1, 2, 3, 4])



# NumPy array is like Matrix in R
np.zeros((3,3))
#>array([[0., 0., 0.],
#>       [0., 0., 0.],
#>       [0., 0., 0.]])
  
arr.dtype
#>dtype('int32')



# 切片与索引NumPy数据
## 注意用np.array()建立矩阵需要一个list作为参数
arr = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
#>array([[ 1,  2,  3,  4],
#>       [ 5,  6,  7,  8],
#>       [ 9, 10, 11, 12]])
## 相比R,Python具有愚蠢的差一特性,以下切片表示取第1,2行与第3列至末尾的矩阵元素
arr[:2,2:]
#>array([[3, 4],
#>       [7, 8]])
## 与R不同,对Numpy切片的修改会修改原数据的值,这会造成危险
arr[2,1] = 0
arr
#>array([[ 1,  2,  3,  4],
#>       [ 5,  6,  7,  8],
#>       [ 9,  0, 11, 12]])
## 为了与R同步,建议一直使用.copy()方法获取切片
arr.copy()[2,1] = 10
arr
#>array([[ 1,  2,  3,  4],
#>       [ 5,  6,  7,  8],
#>       [ 9,  0, 11, 12]])



# 与R相同,Numpy的array对象的计算与函数均向量化(不知道这有什么好吹嘘的)
## 简单示例,加上常数与部分函数均对矩阵所有元素进行操作
arr + 5
arr + arr**2
## 需要注意,向量操作的函数以方法的形式使用(R中以函数的方式);但仍可自定义函数传递给array
arr.sum(); arr.max(); arr.argmax(); arr.std(); arr.cumsum()
## 定义函数f()后
f(arr)



# 伪随机数生成
import numpy.random as npr
import matplotlib.pyplot as plt











