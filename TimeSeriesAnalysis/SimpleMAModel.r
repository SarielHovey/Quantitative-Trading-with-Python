# There is no ma(x) in R as ar(x). But we could set order in arima(x)
# order=c(0,0,3) means a simple MA(3) model
x.ma <- arima(x, order=c(0, 0, 3))
# It is suggested to use ARIMA instead of simple AR or MA model

