# Asscess mkt data from tuShare Pro
import tushare as ts
print(ts.__version__)
#>1.2.39

# Set token here, only needed for the 1st time
ts.set_token('Token Value')
# Use pro API
pro = ts.pro_api()





