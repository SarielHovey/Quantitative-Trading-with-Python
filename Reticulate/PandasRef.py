#library(reticulate)        以下Python3代码均在R下的reticualte环境中运行,目的在于能够同时使用Python的数据清洗与R的数据分析
#repl_python()      启动R下的Python解释器,输入exit则退出
#>Python 3.7.3 (C:\PROGRA~3\ANACON~1\python.exe)
#>Reticulate 1.12 REPL -- A Python interpreter in R.

import pandas as pd

# Pandas Series
## Pandas的Series与R中的一维数组类似,均支持标签索引与数字索引
## 建立时可用index= 参数直接制定index(R中为dimnames,不要混淆)
arr = pd.Series([1,2,3,4], index=['A','B',"C",'D'])
arr
#>A  1
#>B  2
#>C  3
#>D  4
#>dtype: int64

## 获取标签部分
arr.index
Index(['A', 'B', 'C', 'D'], dtype='object')
## 获取数据部分
arr.values
#>array([1, 2, 3, 4], dtype=int64)
## 与R相同, pd Series支持以逻辑筛选进行切片
arr[arr >= 2]
#>B    2
#>C    3
#>D    4
#>dtype: int64

## 可对pd Series使用各种方法,下例为进行基本统计描述(R中为summary()函数,不要混淆)
## RStudio中Tab补全仍可用
arr.describe()
#>count    4.000000
#>mean     2.500000
#>std      1.290994
#>min      1.000000
#>25%      1.750000
#>50%      2.500000
#>75%      3.250000
#>max      4.000000
#>dtype: float64

## 特别的,pd Series有转化为字典的方法
arr_dic = arr.to_dict()
arr_dic
#>{'A': 1, 'B': 2, 'C': 3, 'D': 4}
### 对于reticulate包而言,在R中引用pd Series会转化为带标签的一维数组(array)而不是向量(vector)
py$arr
#>A B C D 
#>1 2 3 4
is.vector(py$arr)
#>FALSE
is.array(py$arr)
#>TRUE
### 而py中的字典在R中引用会转化为列表(list)
py$arr_dic
#>$A
#>[1] 1
#>$B
#>[1] 2
#>$C
#>[1] 3
#>$D
#>[1] 4








