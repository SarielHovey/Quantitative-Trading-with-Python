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


## Mini-batch Stochastic Gradient Descent
'''
$\hat{y} = w_1 x_1 + w_2 x_2 + b$, b is bias in estimation
Loss function: 
    $l_i(w_1,w_2,b) = 1/2 (\hat{y_i}-y_i)^2$
    $l(w_1,w_2,b) = 1/n * \sum^n_{i=1}{l_i(w_1,w_2,b)}$
Set $\eta$ as learning rate, $|B|$ as batch size for every random choose
Start Iteration:
\equation
w_1 \leftarrow w_1 - \frac{\eta}{|B|} \sum_{i \in B}{\frac{\partial l_i(w_1,w_2,b)}{\partial w_1}}
w_2 \leftarrow w_2 - \frac{\eta}{|B|} \sum_{i \in B}{\frac{\partial l_i(w_1,w_2,b)}{\partial w_2}}
b \leftarrow b - \frac{\eta}{|B|} \sum_{i \in B}{\frac{\partial l_i(w_1,w_2,b)}{\partial b}}
\equation
'''
from mxnet import nd, autograd
import random
num_inputs = 2; num_examples = 1000
true_w = [2,3.4]
true_b = 2.5
features = nd.random.normal(scale=1, shape=(num_examples, num_inputs)) # 1000x2 NDArray
labels = true_w[0]*features[:,0] + true_w[1]*features[:,1] + true_b
labels += nd.random.normal(scale=0.01,shape = labels.shape)
def data_iter(batch_size,features,labels):
    '''
    Function used to execute Mini-batch Stochastic Sampling
    '''
    num_examples = len(features)
    indices = list(range(num_examples))
    random.shuffle(indices) # set random sample reading order
    for i in range(0,num_examples,batch_size):
        j = nd.array(indices[i: min(i + batch_size,num_examples)])
        yield features.take(j), labels.take(j) # return element according to indices

for X, y in data_iter(10,features,labels):
    print(X,y)
'''
X: 10x2 NDArray
y: 10x1 NDArray
'''

w = nd.random.normal(scale=0.01,shape=(num_inputs,1))
b = nd.zeros(shape=(1,))
w.attach_grad(); b.attach_grad()

def linreg(X,w,b):
    return nd.dot(X,w) + b

def squared_loss(y_hat,y):
    return (y_hat - y.reshape(y_hat.shape)) ** 2 * .5

def sgd(params,lr,batch_size):
    '''
    Perform Gradient Descent on "params"
    [:] sets inplace change
    '''
    for param in params:
        param[:] = param - lr * param.grad / batch_size

lr = 0.03
num_epochs = 3
net = linreg
loss = squared_loss
batch_size = 10 # 如果batch_size不能整除num_examples, 则data_iter生成的最后一批样本数量将小于batch_size, 训练仍可正常运行
for epoch in range(num_epochs):
    for X, y in data_iter(batch_size, features, labels):
        with autograd.record():
            l = loss(net(X,w,b),y)
        l.backward()  # if without autograd.record() and backward() in advance, grad() method will return 0
        sgd([w,b],lr,batch_size)
    train_l = loss(net(features,w,b),labels)
    print('epoch %d, loss %f' % (epoch +1, train_l.mean().asnumpy()))    
'''
epoch 1, loss 0.016662
epoch 2, loss 0.000077
epoch 3, loss 0.000050
'''




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
'''
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
'''
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
'''
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
sgd_reg.intercept_, sgd_reg.coef_
best_model.predict([[1.5]])
'''
Definitely not ideal. With too many unneeded coef for poly, this method could not help
(array([3.5302907]),
 array([ 5.01682591e+00,  1.67919258e+00,  5.37535583e-01, -2.14422285e-01,
        -1.35550602e-01, -3.33127530e-01, -1.81939062e-01, -1.71302979e-01,
        -1.43526343e-01, -5.41116835e-03, -1.00043501e-01,  1.07502969e-01,
        -5.76154380e-02,  1.62940497e-01, -1.63372188e-02,  1.71845055e-01,
         2.16180354e-02,  1.49009197e-01,  5.34429849e-02,  1.08344030e-01,
         7.71358602e-02,  6.09825846e-02,  9.19265139e-02,  1.48434322e-02,
         9.81155517e-02, -2.50786053e-02,  9.67250490e-02, -5.61324239e-02,
         8.91613055e-02, -7.73845838e-02,  7.69582054e-02, -8.90636410e-02,
         6.16072588e-02, -9.21162832e-02,  4.44580885e-02, -8.78774350e-02,
         2.66692373e-02, -7.78391429e-02,  9.19206494e-03, -6.34977734e-02,
        -7.22507668e-03, -4.62596856e-02, -2.20212127e-02, -2.73885738e-02,
        -3.48014354e-02, -7.98128255e-03, -4.53135488e-02,  1.10377564e-02,
        -5.34248581e-02,  2.89105401e-02, -5.91003555e-02,  4.50328803e-02,
        -6.23829497e-02,  5.89384714e-02, -6.33760120e-02,  7.02817969e-02,
        -6.22282807e-02,  7.88212164e-02, -5.91210286e-02,  8.44030248e-02,
        -5.42573244e-02,  8.69469013e-02, -4.78531808e-02,  8.64329257e-02,
        -4.01303707e-02,  8.28901891e-02, -3.13106944e-02,  7.63869351e-02,
        -2.16114932e-02,  6.70221185e-02, -1.12422220e-02,  5.49182427e-02,
        -4.01908755e-04,  4.02153332e-02,  1.07226461e-02,  2.30659047e-02,
         2.19580649e-02,  3.63078900e-03,  3.31450936e-02, -1.79242959e-02,
         4.41389079e-02, -4.14315460e-02,  5.48091048e-02, -6.67233352e-02,
         6.50394512e-02, -9.36340253e-02,  7.47274469e-02, -1.22001396e-01,
         8.37837493e-02, -1.51667757e-01]))
array([4.93216085])
'''




# Logistic Regression
'''
Logistic Regression Model estimated probability:
$\hat{p} = h_{\theta}(x) = \sigma(x^T \theta)$
$\sigma(t) = \frac{1}{1+ exp(-t)}$
$\hat{y} = 0$ if $\hat{p}<0.5$; $hat{y} = 1$ if $\hat{p}>=0.5$

Single training cost function:
$c(\theta) = -log(\hat{p})$ if $y=1$. cost high when y=1 but p is near 0
$c(\theta) = -log(1 - \hat{p})$ if $y=0$. cost high when y=0 but p is near 1

Logistic Regression cost function:
J(\theta) = - \frac{1}{m} \sum^m_{i=1}[y_i*log(\hat{p_i}) + (1-y_i)*log(1-\hat{p_i})]
no closed-form resolution, but the function is convex

Logistic Cost function partial derivatives:
$\frac{\partial}{\partial\theta_j}J(\theta) = (1/m)\sum^m_{i=1}((\sigma(\theta^T*x_i)-y_i)x_ji)$
'''
## Decision Boundaries (example with iris plant)
from sklearn import datasets
iris = datasets.load_iris()
[iris.keys()]
'''
[dict_keys(['data', 'target', 'target_names', 'DESCR', 'feature_names', 'filename'])]
'''
### Train a model to classify Iris Virginica based on petal width
X = iris['data'][:,3:]
y = (iris['target']==2).astype(np.int)

from sklearn.linear_model import LogisticRegression
log_reg = LogisticRegression()
log_reg.fit(X, y)

X_new = np.linspace(0,3,1000).reshape(-1,1)
y_proba = log_reg.predict_proba(X_new)
plt.plot(X_new, y_proba[:,1],'g-',label='Iris Virginica')
plt.plot(X_new,y_proba[:,0],'b--',label='Not Iris Virginica')
plt.xlabel('Petal width(cm)'); plt.ylabel('Probability')
plt.title('Estimated probabilities and decision boundary')
plt.legend(loc=0)
'''
There is a Decision Boundary around 1.61cm, where both probability is 0.50
Near 1.61cm, the classifier cannot clearly divide between 2 categories
'''
log_reg.predict([[1.60],[1.62]])
'''
a difference of 2mm in width leads to 2 categories:
array([0, 1])
Of course, more paras are needed to enhance the classifier
'''


## Softmax Regression (Multinomial Logistic Regression)
'''
Softmax score for class k: (k is independent variable)
$s_k(x)=x^T*\theta_k$
$\theta_k$ is parameter vector of class k

Softmax function: (estimated probability that x belongs to class k, based on softmax score)
$\hat{p_k} = \sigma(s(x))_k = \frac{exp(s_k(x))}{\sum^K_{j=1}exp(s_j(x))}$
K is number of classes

Softmax Regression classifier prediction:
$\hat{y} = argmax_k \sigma(s(x))_k = argmax_k s_k(x) = argmax_k(\theta_k^T * x)$
argmax returns k that maxmizes $\sigma(s(x))_k$
The prediction returns the most possible category

Cross Entropy Cost Function:
$J(\Theta) = (1/m) \sum^m_{i=1} \sum^K_{k=1}(y_ki log(\hat{p_ki}))$
$y_ki$ is target probability that i-th instance belongs to class k

Cross Entropy Gradient Vector for class k:
$\nabla_{\theta_k} J(\Theta) = (1/m) \sum^m_{i=1}{(\hat{p_ki}-y_ki)x_i}$
'''
### Use petal length, petal width to predict multi-classes
X = iris['data'][:,(2,3)]
y = iris['target']
softmax_reg = LogisticRegression(multi_class='multinomial',solver='lbfgs',C=10) # $C = 1/{\alpha}$
softmax_reg.fit(X,y)
softmax_reg.predict([[5,2]]);softmax_reg.predict_proba([[5,2]])
'''
array([2])
array([[6.38014896e-07, 5.74929995e-02, 9.42506362e-01]])
'''
