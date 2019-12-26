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
matrix([[3.5422845 ],
        [3.97416522]])
'''

## Linear Regression with Sckit-Learn
from sklearn.linear_model import LinearRegression
lin_reg = LinearRegression()
lin_reg.fit(X, y)
lin_reg.intercept_, lin_reg.coef_
'''
(array([3.5422845]), array([[3.97416522]]))
'''
lin_reg.predict(np.array([[1],[5]]))
'''
array([[ 7.51644971],
       [23.41311059]])
'''
## Least Squares
theta_best_svd, residual, rank, s = np.linalg.lstsq(X_b, y, rcond=1e-6)
'''
Same as above. LinearRegression() defaults lstsq method.
matrix([[3.5422845 ],
        [3.97416522]])
'''
## Pseudoinverse of X -- X_b
np.linalg.pinv(X_b).dot(y)
'''
based on SVD decomposion, preferred to Normal Equation
matrix([[3.5422845 ],
        [3.97416522]])
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
matrix([[3.5422845 ],
        [3.97416522]])
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
matrix([[3.55054384],
        [3.98230242]])
'''
from sklearn.linear_model import SGDRegressor
sgd_reg = SGDRegressor(max_iter=10000, tol=1e-3, penalty=None, eta0=0.1) # eta0 is initial learning rate
sgd_reg.fit(X, y)
sgd_reg.intercept_, sgd_reg.coef_
'''
(array([3.53459864]), array([3.97474713]))
'''

## Mini-batch Gradient Descent




# Polynomial Regression
m = 1000
X = 6 * np.random.rand(m,1) - 3
y = .5 * X **2 + 3 * X + 2 + np.random.randn(m,1)
from sklearn.preprocessing import PolynomialFeatures
poly_features = PolynomialFeatures(degree=2, include_bias=False) # plot(x,y) shows the pattern for degree 2
X_poly = poly_features.fit_transform(X)
X_poly[:7]
'''
         X             X^2 
array([[-1.03041035,  1.06174548],
       [-1.21462745,  1.47531984],
       [-0.64801849,  0.41992796],
       [-0.79582731,  0.6333411 ],
       [ 2.93309789,  8.60306322],
       [-0.8987783 ,  0.80780243],
       [ 2.07503555,  4.30577253]])
More columns if degree set to n>2
'''
lin_reg = LinearRegression()
lin_reg.fit(X_poly, y)
lin_reg.intercept_, lin_reg.coef_
'''
Result: $y = 2.0767 + 3.0159 * X + 0.4792 * X^2$
Underlying real model: $y = 2 + norm(0,1) + 3X + 0.5X^2$
(array([2.07674669]), array([[3.01589423, 0.47915133]]))
'''

## Learning curve for Overfitting detection
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
### Change list to np.array and use Numba if performance preferred
def plot_learning_curve(model, X, y):
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=.2)
    train_error, val_error = [], []
    for m in range(1, len(X_train)):
        model.fit(X_train[:m], y_train[:m])
        y_train_pred = model.predict(X_train[:m])
        y_val_pred = model.predict(X_val)
        train_error.append(mean_squared_error(y_train[:m], y_train_pred))
        val_error.append(mean_squared_error(y_val, y_val_pred))
    plt.plot(np.sqrt(train_error),'r-+',linewidth=2,label='train')
    plt.plot(np.sqrt(val_error),'b-',linewidth=3,label='val')
    plt.xlabel('Training Set Size')
    plt.ylabel('RMSE')
    plt.legend(loc=0)
    #plt.show()
'''
val: Model Performance on test set
train: Model Performance on train set
In this case RMSE for both val and train reaches a plateau of 2 quickly
A simple linear model underfits
'''
from sklearn.pipeline import Pipeline
polynomial_regression = Pipeline([
    ('poly_features',PolynomialFeatures(degree=10,include_bias=False)),
    ('lin_reg', LinearRegression())
])
plot_learning_curve(polynomial_regression, X, y)
'''
RMSE stables on a level lower than linear model
RMSE(val) >= RMSE(train)
RMSE for val approaches RMSE for train, gap diminishes with more sample
'''



# Reqularized Linear Model
## reduce the degrees of freedom of the model could reduce overfit

## Ridge Regression (Tikhonov regularization)
r'''
Ridge Regression cost function, used on re-scaled data
$J(\theta) = MSE(\theta) + \alpha * 0.5 * \sum^{n}_{i=1}{\theta_i}^2$
MSE adds a regularization term, consisting of model's $\theta$
Minimize J requires minimize model parameter for training
$0 <= \alpha <= 1$ is Hyperparameter: (1) $\alpha = 0$ degrade model to unregularized status
                                      (2) $\alpha = 1$ force all para to be 0 and take mean as model value
'''
from sklearn.linear_model import Ridge
ridge_reg = Ridge(alpha=1, solver='cholesky')
ridge_reg.fit(X, y)
ridge_reg.predict([[1.5]])
'''
Closed-form solution:
    $\theta = (X^T X + \alpha A)^{-1} X^T y$
array([[8.06299998]])
'''

sgd_reg = SGDRegressor(penalty='l2')
sgd_reg.fit(X, y)
sgd_reg.predict([[1.5]])
'''
Stochastic Gradient Descent solution:
    l2 penalty means regularization term is 0.5 * square of paras
array([8.10229213])
'''


## Lasso Regression (Lease Absolute Shrinkage and Selection Operator Regression)
r'''
Lasso Regression cost function:
$J(\theta) = MSE(\theta) + \alpha * \sum^n_{i=1}{abs(\theta_i)}$
The model performs feature selection, para for not important feature will be set to almost zero
'''
from sklearn.linear_model import Lasso
lasso_reg = Lasso(alpha=0.1)
lasso_reg.fit(X, y)
lasso_reg.predict([[1.5]])
'''
array([8.0150082])
With SGDRegressor(penalty='l1'), predict is array([7.9381351])
'''


## Elastic Net
r'''
Elastic Net Cost Function:
$J(\theta) = MSE(\theta) + r\alpha \sum^n_{i=1}abs(\theta_i) + \frac{1-r}{2} \alpha sum^n_{i=1}\theta^2_i$
r is mix ratio. $r=0$:Ridge Regression; $r=1$:Lasso Regression
'''
from sklearn.linear_model import ElasticNet
elastic_net = ElasticNet(alpha=0.1,l1_ratio=0.6) # r=0.5
elastic_net.fit(X, y)
elastic_net.predict([[1.5]])
'''
array([7.97596988])
'''


## Early Stopping
### Stop training once validation error(Validation Set) reaches a minimum
from sklearn.base import clone
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
poly_scaler = Pipeline([
    ('poly_features',PolynomialFeatures(degree=90,include_bias=False)),
    ('std_scaler',StandardScaler())
])
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=.2)
X_train_poly_scaled = poly_scaler.fit_transform(X_train)
X_val_poly_scaled = poly_scaler.transform(X_val)
# warm_start 'True' will keep record of previous training, and continue it for next training
sgd_reg=SGDRegressor(max_iter=1,tol=-np.infty,warm_start=True,penalty=None,learning_rate='constant',eta0=0.0005)
min_val_error = float('inf')
best_epoch = None; best_model = None
for epoch in range(1000):
    sgd_reg.fit(X_train_poly_scaled,y_train)
    y_val_pred = sgd_reg.predict(X_val_poly_scaled)
    val_err = mean_squared_error(y_val, y_val_pred)
    if val_err < min_val_error:
        min_val_error = val_err
        best_epoch = epoch
        best_model = clone(sgd_reg)
'''
best_epoch: 297
best_model: SGDRegressor(alpha=0.0001, average=False, early_stopping=False, epsilon=0.1,
       eta0=0.0005, fit_intercept=True, l1_ratio=0.15,
       learning_rate='constant', loss='squared_loss', max_iter=1,
       n_iter=None, n_iter_no_change=5, penalty=None, power_t=0.25,
       random_state=None, shuffle=True, tol=-inf, validation_fraction=0.1,
       verbose=0, warm_start=True)
'''
best_model.fit(X, y)
best_model.predict([[1.5]])
'''
Definitely not ideal
array([4.93216085])
'''