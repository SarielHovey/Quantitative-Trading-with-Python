# Used to initialize Python in R
install.packages("reticulate")
library(reticulate)
# In the case of using Anaconda:
use_condaenv("C:/Program Data/Anaconda3")
# Check Python status in system
py_config()
# Check if Pandas is installed for Python
py_module_available("pandas")

# Import Python module into R
os <- import("os")

os$getcwd()
#> "C:\\Program Files\\R\\bin"

# Import Numpy
np <- import("numpy")
y <- array(1:4, c(2, 2))
#> y
#>     [,1] [,2]
#>[1,]    1    3
#>[2,]    2    4

## after Importing, numpy functions can be used in R
x <- numpy$array(y)
#>x
#>     [,1] [,2]
#>[1,]    1    3
#>[2,]    2    4

x <- numpy$where(x>0, 1, -1)

# Use Python console in R
repl_python()
#> Python 3.7.3 (C:\PROGRA~3\ANACON~1\python.exe)
#> Reticulate 1.12 REPL -- A Python interpreter in R.
    dictionary = {'alpha': 1, 'beta': 2}
exit
# 'exit' is needed to exit repl
# 'py$x' would access an 'x' variable created within Python from R
py$dictionary
#>$alpha
#>[1] 1

#>$beta
#>[1] 2



