#library(reticulate)        以下Python3代码均在R下的reticualte环境中运行,目的在于能够同时使用Python的数据清洗与R的数据分析
#repl_python()      启动R下的Python解释器,输入exit则退出
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



# 与R相同,Numpy的array对象的计算与函数均向量化
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

## npr.rand()用于生成位于[0,1)的随机数组
npr.rand(4,3)
#>array([[0.14991221, 0.73560538, 0.68169895],
#>       [0.06475313, 0.08516567, 0.06523326],
#>       [0.48031127, 0.00196387, 0.15264255],
#>       [0.36592999, 0.75706219, 0.96999586]])

## npr.randn()用于生成服从标准正态的随机数组
npr.randn(4,3)

## npr.randint()用于生成区间内的随机整数(同样左闭右开); size参数由元组控制,输出矩阵
npr.randint(3,43,size=(4,3))
#>array([[41, 35, 36],
#>       [36, 24, 11],
#>       [38, 41, 11],
#>       [19,  9, 36]])

## npr.choice()用于生成类似离散概率分布,支持标签; size参数的控制同上
npr.choice(['a','b','c'], size=(4,3),p=[0.3,0.4,0.3])
#>array([['b', 'a', 'a'],
#>       ['b', 'c', 'b'],
#>       ['b', 'a', 'a'],
#>       ['a', 'c', 'b']], dtype='<U1')

## npr.binomial()生成二项分布; 输出结果表示n次中p发生的次数
npr.binomial(n=5000,p=0.34,size=(4,3))


