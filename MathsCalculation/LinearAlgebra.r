# Coumput Rank r(A) for a Matrix    基于QR分解计算矩阵的秩
A <- matrix(rnorm(24), 4,6, byrow = TRUE)
qr(A)
#>$qr       对A进行QR分解
#>           [,1]        [,2]       [,3]        [,4]       [,5]        [,6]
#>[1,]  1.0076877 -1.06344618 -0.2845626  0.48679555 -1.2529613 -2.41440347
#>[2,]  0.7687548 -0.97822844  1.0572336 -0.07054892 -1.8920650  2.04010614
#>[3,] -0.5018130  0.08548922  0.9759549 -0.21604167 -2.0292557  0.02553151
#>[4,]  0.1586750 -0.22089548 -0.3397707  0.53805089 -0.4584865  0.24745286

#>$rank
#>[1] 4

#>$qraux
#>[1] 1.3633483 1.9715435 1.9405083 0.5380509 0.4584865 0.2474529

#>$pivot
#>[1] 1 2 3 4 5 6

#>attr(,"class")
#>[1] "qr"
qr(A)$rank
#>[1] 4         r(A)=4



# Solve Linear Equation    线性方程组求解
A <- matrix(c(2,-4,2,7,
             3,-6,4,3,
             5,-10,4,25),3,4, byrow=TRUE)
b <- matrix(numeric(3),3,1)
## Caution: Only when A is square matrix--
solve(A, b)
## In this case, we have to use SVD     使用SVD分解法
## Caution: rank(A)=rank(A|b) < n=4; we have infinite solutions here
T <- svd(A)
#>$d
#>[1] 2.958899e+01 5.787175e+00 2.318302e-15

#>$u
#>           [,1]       [,2]       [,3]
#>[1,] -0.2868398  0.1698058 -0.9428090
#>[2,] -0.2134672  0.9480908  0.2357023
#>[3,] -0.9338922 -0.2688676  0.2357023

#>$v
#>           [,1]       [,2]        [,3]
#>[1,] -0.1988423  0.3178660  0.92705000
#>[2,]  0.3976845 -0.6357320  0.30256774
#>[3,] -0.1744945  0.5281514 -0.21948717
#>[4,] -0.8785559 -0.4646096 -0.02926496

## We can get A back: $ A = U*D*{V^T} $
T$u %*% diag(T$d) %*% t(T$v) - A
#>              [,1]          [,2]         [,3]         [,4]
#>[1,] -1.110223e-15  0.000000e+00 4.440892e-16 0.000000e+00
#>[2,] -1.021405e-14 -5.329071e-15 3.552714e-15 2.220446e-15
#>[3,]  2.042810e-14  0.000000e+00 8.881784e-16 3.552714e-15

## T$v[,3] is the solution for $ AX = 0 $
A %*% T$v[,3] - b
              [,1]
[1,]  6.661338e-16
[2,]  1.343370e-14
[3,] -1.099121e-14


## If b is not a 0 vector, then
require(MASS)
## ginv() gives out Moore-Penrose Inverse, A^{+}    广义逆矩阵
A_p <- ginv(A)
X <- A_p %*% b


