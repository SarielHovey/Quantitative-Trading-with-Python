#library(reticulate)        以下Python3代码均在R下的reticualte环境中运行,目的在于能够同时使用Python的数据清洗与R的数据分析
#repl_python()      启动R下的Python解释器,输入exit则退出
#>Python 3.7.3 (C:\PROGRA~3\ANACON~1\python.exe)
#>Reticulate 1.12 REPL -- A Python interpreter in R.

import pandas as pd

# Pandas Series
## Pandas的Series与R中带names()向量类似,均支持标签索引与数字索引
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
#   >>>require(reticulate)
#   >>>py$arr
#>A B C D 
#>1 2 3 4
#   >>>is.vector(py$arr)
#>FALSE
#   >>>is.array(py$arr)
#>TRUE
### 而py中的字典在R中引用会转化为列表(list)
#   >>>py$arr_dic
#>$A
#>[1] 1
#>$B
#>[1] 2
#>$C
#>[1] 3
#>$D
#>[1] 4



# Pandas DataFrame
## pd DataFrame与R中的DataFrame等价,在reticulate环境下可以直接相互引用
### 首先在R环境下建立一个数据框da
###   >>>A <- 1:4
###   >>>B <- 5:8
###   >>>C <- 9:12
###   >>>da <- data.frame(A,B,C, row.names = c('Yesterday','Today','Tomorrow','Day3'))
#>          A B  C
#>Yesterday 1 5  9
#>Today     2 6 10
#>Tomorrow  3 7 11
#>Day3      4 8 12

### 进入repl_python()环境并引用
### 引用结果为一个pd DataFrame
da = r.da
#>           A  B   C
#>Yesterday  1  5   9
#>Today      2  6  10
#>Tomorrow   3  7  11
#>Day3       4  8  12


## pd的输出格式设置
import pandas as pd
pd.set_option("display.max_rows",1000)
pd.set_option("display.max_columns",34)
pd.set_option('precision',7)
pd.set_option('large_repr','truncate')


## 基于pd的read与write操作
### 此步可通过RStudio自带的数据读入操作进行, 输出为DataFrame
DATA = pd.read_csv("Z:/linshi/GLD.csv",encoding='ANSI',dtype={'Date':str})
DATA.head(6)
#>          Date        Open        High         Low       Close   Adj Close       Volume  
#>0  2017-06-14  121.510002  121.879997  119.570000  119.820000  119.820000       21124800
#>1  2017-06-15  119.220001  119.500000  119.129997  119.320000  119.320000       6796700
#>2  2017-06-16  119.349998  119.500000  119.239998  119.339996  119.339996       6435700
#>3  2017-06-19  118.739998  118.839996  118.330002  118.430000  118.430000       6787000  
#>4  2017-06-20  118.419998  118.459999  118.070000  118.180000  118.180000       4617400  
#>5  2017-06-21  118.150002  118.660004  118.150002  118.519997  118.519997       4723700
### 如前所述,在R环境中可无损转换为R的DataFrame
###     >>>DA_GLD <- py$DATA
### to_excel()方法可将数据写入xls文件(推荐使用to_csv()方法)
DATA.to_excel('GLD_AdjClose')


## 基于pd的描述统计
### ".T"表示数据含Title行
DATA.describe().T
#>           count           mean            std            min            25%  \
#>Open       504.0  1.2103413e+02  4.1339436e+00  1.1146000e+02  1.1813250e+02   
#>High       504.0  1.2139177e+02  4.1567055e+00  1.1188000e+02  1.1844750e+02   
#>Low        504.0  1.2066873e+02  4.0992161e+00  1.1106000e+02  1.1783250e+02   
#>Close      504.0  1.2102550e+02  4.1410327e+00  1.1110000e+02  1.1812500e+02   
#>Adj Close  504.0  1.2102550e+02  4.1410327e+00  1.1110000e+02  1.1812500e+02   
#>Volume     504.0  7.3884798e+06  3.1298984e+06  1.7797000e+06  5.1573250e+06   

#>                     50%            75%            max  
#>Open       1.2148000e+02  1.2433500e+02  1.2869000e+02  
#>High       1.2192500e+02  1.2467000e+02  1.2951000e+02  
#>Low        1.2118000e+02  1.2396250e+02  1.2823000e+02  
#>Close      1.2156000e+02  1.2433750e+02  1.2883000e+02  
#>Adj Close  1.2156000e+02  1.2433750e+02  1.2883000e+02  
#>Volume     6.7689000e+06  8.6750750e+06  2.6810900e+07  

### 显示DATA的属性
DATA.info()
#><class 'pandas.core.frame.DataFrame'>
#>RangeIndex: 504 entries, 0 to 503
#>Data columns (total 7 columns):
#>Date         504 non-null object
#>Open         504 non-null float64
#>High         504 non-null float64
#>Low          504 non-null float64
#>Close        504 non-null float64
#>Adj Close    504 non-null float64
#>Volume       504 non-null int64
#>dtypes: float64(5), int64(1), object(1)
#>memory usage: 27.6+ KB


## pd DataFrame的map映射
### Initiazlize a data.frame in R, and transfer to python
da = r.da
da
#>           A  B   C    D
#>Yesterday  1  5   9  0.0
#>Today      2  6  10  1.0
#>Tomorrow   3  7  11  0.0
#>Day3       4  8  12  1.0
### 新建一个字典用于map()方法
b = {0: 'Here', 1:'There'}
### 在da中新建一列用于存储映射的结果
da['Location'] = da.D.map(b)
da
#>           A  B   C    D Location
#>Yesterday  1  5   9  0.0     Here
#>Today      2  6  10  1.0    There
#>Tomorrow   3  7  11  0.0     Here
#>Day3       4  8  12  1.0    There


## pd DataFrame按列排序
da.sort_values(by=['Location','A'],ascending=[True,False],inplace=True)
da
#>           A  B   C    D Location
#>Tomorrow   3  7  11  0.0     Here
#>Yesterday  1  5   9  0.0     Here
#>Day3       4  8  12  1.0    There
#>Today      2  6  10  1.0    There


## pd DataFrame重复项的处理
xy = r.xy
xy
#>  k1   k2
#>0  x  3.0
#>1  x  2.0
#>2  x  1.0
#>3  y  4.0
#>4  y  3.0
#>5  y  4.0
### drop_duplicates()方法默认去除完全相同的行(原数据框不变)
xy.drop_duplicates()
#>  k1   k2
#>0  x  3.0
#>1  x  2.0
#>2  x  1.0
#>3  y  4.0
#>4  y  3.0
### subset参数确定按某一列去重, keep参数设置保留的元素
xy.drop_duplicates(subset='k1',keep='last')
#>  k1   k2
#>2  x  1.0
#>5  y  4.0
### 可以查看完全重复的行
xy[xy.duplicated()]
#>  k1   k2
#>5  y  4.0


## 







