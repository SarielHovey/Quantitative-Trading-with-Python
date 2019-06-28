# the package is used to speed up calculation in R for multi-core PCs
library(doParallel)
threads <- 6
# Set up how many threads to run. Im running a 6-core PC(AMD Ryzen 2600)
registerDoParallel( cores = threads )

m <- matrix(rnorm(34000), 1000, 34)
# Parallel-process to get matrix m normalized
m <- foreach(i=1:nrow(m), .combine=rbind) %dopar% (m[i,] / mean(m[i,]))
