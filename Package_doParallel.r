# the package is used to speed up calculation in R for multi-core PCs
library(doParallel)
workers <- 6
# Set up how many threads to run. Im running a 6-core PC(AMD Ryzen 2600)
registerDoParallel( cores = workers )

m <- matrix(rnorm(34000), 1000, 34)
# Parallel-process to get matrix m normalized
m <- foreach(i=1:nrow(m), .combine=rbind) %dopar% (m[i,] / mean(m[i,]))

# Define a function to help Integer Mapping, from 'Chris Conlan, Automated Trading with R, 10.1007/978-1-4842-2178-5_6'
# To mimic 'rollapply', remember to add $k - 1$ rows of NA to beginning of output
# i is the object to process; n = nrow(i); k == windowsize; p == workers
delegate <- function( i = i, n = n, k = k, p = workers ){
  # A right-aligned time series computation with window size k on n rows of input returns $n_o = n-k+1$ rows of output
  nOut <- n - k + 1
  # A properly dispatched set of p processes will compute a maximum of $\left\rceil{\frac{n_o}{p}}\right\rceil$ rows of output per process 
  # and a minimum of $\left\lceil{\frac{n_o}{p}}\right\rceil -p+1$ rows of output per process.
  nProc <- ceiling( nOut / p )
  return( (( i - 1 ) * nProc + 1) : min(i * nProc + k - 1, n) )
}

# Example
lapply(1:6, function(i) delegate(i, n=100, k=5, p = 6))
#[[1]]
 #[1]  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20
#[[2]]
# [1] 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36
#[[3]]
# [1] 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52
#[[4]]
# [1] 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68
#[[5]]
# [1] 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84
#[[6]]
# [1]  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98
#[19]  99 100  

# Example 2
lapply(1:4, function(i) delegate(i, n=100, k=5, p = 6))
#[[1]]
# [1]  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20

#[[2]]
# [1] 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36

#[[3]]
# [1] 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52

#[[4]]
# [1] 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68
       
