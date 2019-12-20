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




# Gradient Descent
## Batch Gradient Descent
lnr = 0.1 # Learning Rate
n_iter = 1000
m = 100
theta_init = np.random.randn(2,1) # Random Initialization
for iteration in range(n_iter): # All data in training set is used
    gradient = 2/m * X_b.T * (X_b * theta_init - y)
    theta_init = theta_init - lnr * gradient
'''
matrix([[3.42673069],
        [4.05257131]])
'''

## Random Gradient Descent
n_epochs = 50; m = 100
def learning_schedule(t, t0=5, t1=50):
    '''
    t0 and t1 are learning schedule hyperparameters
    '''
    return t0 / (t + t1)
    
theta_init = np.random.randn(2,1)
for epoch in range(n_epochs):
    for i in range(m): # Make sure random, not choose from data still sorted by label
        random_index = np.random.randint(m)
        xi = X_b[random_index : random_index+1]
        yi = y[random_index : random_index+1]
        gradient = 2 * xi.T *(xi * theta_init - yi)
        lnr = learning_schedule(epoch *m + i)
        theta_init = theta_init - lnr * gradient
'''
matrix([[3.41881019],
        [4.05000377]])
'''
from sklearn.linear_model import SGDRegressor
sgd_reg = SGDRegressor(max_iter=10000, tol=1e-3, penalty=None, eta0=0.1) # eta0 is initial learning rate
sgd_reg.fit(X, y)
sgd_reg.intercept_, sgd_reg.coef_
'''
(array([3.43595316]), array([4.08850395]))
'''