require(fBasics)
GDX <- read_csv("GDX.csv", col_types = cols(Date = col_date(format = "%Y-%m-%d")))
# %d 数字表示的日期（0~31） 例如01~31
# %a 缩写的星期名 例如Mon
# %A 非缩写的星期名 例如Monday
# %m 月份（00~12） 例如00~12
# %b 缩写的月份 例如Jan
# %B 非缩写的月份 例如January
# %y 两位数的年份 例如07
# %Y 四位数的年份  例如2007



dim(GDX)
#> [1] 504   7
## GDX is a Tibble with 504 rows and 7 columns
GDX[1,]
#> A tibble: 1 x 7
#>  Date        Open  High   Low Close `Adj Close`    Volume
#>  <date>     <dbl> <dbl> <dbl> <dbl>       <dbl>     <dbl>
#>1 2017-06-14  23.4  23.4  22.1  22.2        21.9 107805400

gdx <- GDX[,6]
basicStats(gdx)
#>               Adj.Close
#>nobs          504.000000          样本总体数量
#>NAs             0.000000          Number of NAs in data
#>Minimum        17.477526
#>Maximum        25.152903
#>1. Quartile    20.837447          1/4 percentile
#>3. Quartile    22.582217          3/4 percentile
#>Mean           21.611396
#>Median         21.967809
#>Sum         10892.143806
#>SE Mean         0.066741
#>LCL Mean       21.480271          平均值的95%置信区间下界
#>UCL Mean       21.742522          平均值的95%置信区间上界
#>Variance        2.245009
#>Stdev           1.498335
#>Skewness       -0.709157
#>Kurtosis        0.043401          Caution: This is Excess Kurtosis, $ K(x)-3 $

s_gdx <- skewness(gdx)
#> -0.7091571 
# 正态假定下偏度渐进服从方差为$6/{样本数}$的正态分布;超额峰度渐进服从方差为$24/{样本数}$的正态分布
# 此二者的标准化的平方之和为JB检验
t_s_gdx <- s_gdx/sqrt(6/504)
# Hand-made P value for t-test of s_gdx
p_t_s_gdx <- 2*(1-pnorm(t_s_gdx))
#> 2            GDX的Adj Close显著负偏

require(dplyr)
# set gdx to be a vector, not a tibble
gdx <- pull(GDX, 'Adj Close')
t.test(gdx)
#>	One Sample t-test
#>
#>data:  gdx
#>t = 323.81, df = 503, p-value < 2.2e-16
#>alternative hypothesis: true mean is not equal to 0
#>95 percent confidence interval:
#> 21.48027 21.74252
#>sample estimates:
#>mean of x 
#>  21.6114 
normalTest(gdx, method='jb')
#>Title:
#> Jarque - Bera Normalality Test

#>Test Results:
#>  STATISTIC:
#>    X-squared: 42.5611
#>  P VALUE:
#>    Asymptotic p Value: 5.728e-10         Obviously, Adj Close for GDX is of non-normality
#>
#>Description:
#> Mon Jul 15 10:56:09 2019 by user: sariel





# Now get to example for Foreign Exchange Rate USD/EUR
setwd("Z:/linshi")
useu <- read.table('d-useu.txt',header = T)
head(d.useu)
#>  Date Mon Day  Value
#>1 2000   1   4 1.0309
#>2 2000   1   5 1.0335
#>3 2000   1   6 1.0324
#>4 2000   1   7 1.0294
#>5 2000   1  10 1.0252
#>6 2000   1  11 1.0322

d.useu$ri <- as.Date(paste(d.useu$Date,d.useu$Mon,d.useu$Day,sep='.'), 
                      format = "%Y.%m.%d")
head(d.useu)
#>  Date Mon Day  Value         ri
#>1 2000   1   4 1.0309 2000-01-04
#>2 2000   1   5 1.0335 2000-01-05
#>3 2000   1   6 1.0324 2000-01-06
#>4 2000   1   7 1.0294 2000-01-07

fx_useu <- xts(d.useu$Value, order.by = d.useu$ri)
head(fx_useu)
#>             [,1]
#>2000-01-04 1.0309
#>2000-01-05 1.0335
#>2000-01-06 1.0324
#>2000-01-07 1.0294
#>2000-01-10 1.0252
#>2000-01-11 1.0322

df_useu <- diff(fx_useu)
## r_useu is the daily return rate for fx_useu
r_useu <- df_useu/fx_useu
## 对数化收益率
r_useu <- log(1+r_useu)
basicStats(r_useu)
#>                      x
#>nobs        2323.000000
#>NAs            1.000000
#>Minimum       -0.030961
#>Maximum        0.044167
#>1. Quartile   -0.003409
#>3. Quartile    0.003780
#>Mean           0.000067
#>Median         0.000075
#>Sum            0.156002
#>SE Mean        0.000136
#>LCL Mean      -0.000199
#>UCL Mean       0.000333
#>Variance       0.000043
#>Stdev          0.006535
#>Skewness       0.033960
#>Kurtosis       2.597988

## 由于diff(), r_useu的第一个元素为NA
r_useu[1] <- 0
## 画出对数收益率对时间的关系图
plot(r_useu,type='l')
## 画出自相关图, 范围为700天
acf(r_useu, lag=700)
