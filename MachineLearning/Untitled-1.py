# Linear Regression
## The Normal Equation
import numpy as np
X = 3 * np.random.rand(100,1)
y = 3 + 4 * X + np.random.rand(100, 1)
X_b = np.c_[np.ones((100,1)),X] # Add 1 to every row of X
X_b = np.matrix(X_b)
y = np.matrix(y)
'''
Normal Equation: $\theta = (X^T X)^(-1) X^T y$
'''
theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
'''
matrix([[2.88706337],
        [4.10890596]])
'''

## Linear Regression with Sckit-Learn
from sklearn.linear_model import LinearRegression
lin_reg = LinearRegression()
lin_reg.fit(X, y)
lin_reg.intercept_, lin_reg.coef_
'''
(array([3.47443866]), array([[4.04315982]]))
'''
lin_reg.predict(np.array([[1],[5]]))
'''
array([[ 7.51759848],
       [23.69023775]])
'''
## Least Squares
theta_best_svd, residual, rank, s = np.linalg.lstsq(X_b, y, rcond=1e-6)
'''
Same as above. LinearRegression() defaults lstsq method.
matrix([[3.47443866],
        [4.04315982]])
'''
## Pseudoinverse of X -- X_b
np.linalg.pinv(X_b).dot(y)
'''
based on SVD decomposion, preferred to Normal Equation
matrix([[3.47443866],
        [4.04315982]])
'''


