import datetime

#1. strptime方法可将字符串转为datetime object
A = datetime.datetime.strptime('2019-07-29', '%Y-%m-%d')
B = datetime.datetime.strptime('2019-06-29', '%Y-%m-%d')

A-B
#>datetime.timedelta(days=30)

A>B
#>True
#-------------------------------------------------------------------------------

#2. strftime方法可将datetime object转为str
datetime.datetime.now()
#>datetime.datetime(2019, 7, 29, 11, 35, 53, 70233)

C = datetime.datetime.now()
C.strftime('%Y-%B-%d %a %H:%M:%S')
#>'2019-July-29 Mon 11:38:05'

## strftime参数速查手册:
## %a 星期几的简写;如 星期三为Web 
## %A 星期几的全称;如 星期三为Wednesday 
## %b 月份的简写; 如4月份为Apr 
## %B 月份的全称; 如4月份为April 
## %c 标准的日期的时间串;（如： 04/07/10 10:43:39） 
## %C 年份的后两位数字 
## %d 十进制表示的每月的第几天 
## %D 月/天/年 
## %e 在两字符域中，十进制表示的每月的第几天 
## %F 年-月-日 
## %g 年份的后两位数字，使用基于周的年 
## %G 年分，使用基于周的年 
## %h 简写的月份名 
## %H 24小时制的小时 
## %I 12小时制的小时 
## %j 十进制表示的每年的第几天 
## %m 十进制表示的月份 
## %M 十时制表示的分钟数 
## %n 新行符 
## %p 本地的AM或PM的等价显示 
## %r 12小时的时间 
## %R 显示小时和分钟：hh:mm 
## %S 十进制的秒数 
## %t 水平制表符 
## %T 显示时分秒：hh:mm:ss 
## %u 每周的第几天，星期一为第一天 （值从0到6，星期一为0） 
## %U 第年的第几周，把星期日做为第一天（值从0到53） 
## %V 每年的第几周，使用基于周的年 
## %w 十进制表示的星期几（值从0到6，星期天为0） 
## %W 每年的第几周，把星期一做为第一天（值从0到53） 
## %x 标准的日期串 
## %X 标准的时间串 
## %y 不带世纪的十进制年份（值从0到99） 
## %Y 带世纪部分的十制年份 
## %z，%Z 时区名称，如果不能得到时区名称则返回空字符。 
## %% 百分号
#-------------------------------------------------------------------------

#3. parse()的用法
## parse函数能够解析str, 返回datetime object
from dateutil.parser import parse

D = '2019 Aug 01 10:34:43am'
parse(D)
#>datetime.datetime(2019, 8, 1, 10, 34, 43)

E = '2019 Aug 01 10:34:43pm'
parse(E)
#>datetime.datetime(2019, 8, 1, 22, 34, 43)



