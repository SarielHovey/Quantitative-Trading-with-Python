# Linear SVM Classification
'''
Linear SVM Classifier Prediction:
$\hat{y} = 0$ if $w^T x + b < 0$
$\hat{y} = 1$ if $w^T x + b >= 0$
'''

## Hard Margin Classification
'''
Hard Margin Linear SVM classifier objective: (an instance of Quadratic Programming problem)
    $t_i = -1$ if $\hat{y}=0$, $t_i = 1$ if $\hat{y}=1$
    $min_{w,b} \frac{1}{2} w^T w$
      subject to $t_i * (w^T x_i +b) >= 1$ for i = 1,2,...,m
$w$ is the slope of $(x,wx)$. smaller $w$ means wider margin for x
This means no outlier on the svm margin, which may not be possible
'''

## Soft Margin Classification
'''
Soft Margin Linear SVM classifier objective:
    $t_i = -1$ if $\hat{y}=0$, $t_i = 1$ if $\hat{y}=1$
    $min_{w,b,\zeta} \frac{1}{2} w^T w + C \sum_i^m{\zeta_i}$
      subject to $t_i * (w^T x_i +b) >= 1 - \zeta_i$ and $\zeta >=0$ for i = 1,2,...,m
$\zeta_i$ controls how much the ith instance is allowed to violate the margin
'''
import numpy as np
from sklearn import datasets
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

iris = datasets.load_iris()
X = iris['data'][:,(2,3)] # petal length and petal width
y = (iris['target']==2).astype(np.float64) # type 2 is Iris virginica
svm_clf = Pipeline([
    ('scaler',StandardScaler()),
    ('linear_svc',LinearSVC(C=1,loss='hinge')) # lower C means wider margin and larger margin violations
])
svm_clf.fit(X,y)
svm_clf.predict([[5.8,1.5]])
'''
array([1.])
'''




## Nonlinear SVM Classification with linear Kernal
'''
Common Kernels: 
    Linear: $K(a,b) = a^T b$
    Polynomial: $K(a,b) = (\gamma a^T b + r)^d$
    Gaussian RBF: $K(a,b) = exp(-\gamma||a-b||^2)$
    Sigmoid: $K(a,b) = tanh(\gamma a^T b + r)$
$K(a,b)=\phi(a)^T \phi(b)$. With kernel, the product could be computed directly even $\phi(x)$ is unknown
'''
from sklearn.datasets import make_moons
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures

X, y = make_moons(n_samples=5000, noise=0.15)
import matplotlib.pyplot as plt
plt.plot(X[:,0][y==0],X[:,1][y==0],'bs')
plt.plot(X[:,0][y==1],X[:,1][y==1],'g^')
plt.axis([-1.5,2.5,-1,1.5])
plt.grid(True,which='both')
plt.xlabel('$X_1$',fontsize=14); plt.ylabel('$X_2$',fontsize=14,rotation=0) # shows pattern of degree 3
'''
Hinge Loss: $max(0,1-t)$
'''
polynomial_svm_clf = Pipeline([
    ('poly_features',PolynomialFeatures(degree=3)),
    ('scaler',StandardScaler()),
    ('svm_clf',LinearSVC(C=10,loss='hinge'))
])
polynomial_svm_clf.fit(X,y)

def plot_dataset(X, y, axes):
    '''
    Require matplotlib.pyplot as plt
    axes is a 4 element list, specifying range on X, Y axis
    y is classified into 2 categories
    '''
    plt.plot(X[:, 0][y==0], X[:, 1][y==0], "bs")
    plt.plot(X[:, 0][y==1], X[:, 1][y==1], "g^")
    plt.axis(axes)
    plt.grid(True, which='both')
    plt.xlabel(r"$x_1$", fontsize=14)
    plt.ylabel(r"$x_2$", fontsize=14, rotation=0)

def plot_predictions(clf, axes):
    '''
    Require matplotlib.pyplot as plt
    axes is a 4 element list, specifying range on X, Y axis
    For modify, x0s & x1s length should = sample length in plot_dataset()
    '''
    x0s = np.linspace(axes[0], axes[1], 5000)
    x1s = np.linspace(axes[2], axes[3], 5000)
    x0, x1 = np.meshgrid(x0s, x1s) # x0.shape: (5000,5000), both 5000^2 elements in total
    X = np.c_[x0.ravel(), x1.ravel()] # X shape: (5000^2,2), degrade x0 and x1 to 1-stage-vector and in 2 columns
    y_pred = clf.predict(X).reshape(x0.shape) # predicted type based on model
    y_decision = clf.decision_function(X).reshape(x0.shape) # score of every sample in X
    plt.contourf(x0, x1, y_pred, cmap=plt.cm.brg, alpha=0.2)
    plt.contourf(x0, x1, y_decision, cmap=plt.cm.brg, alpha=0.1)

plot_dataset(X,y,[-1.5,2.5,-1,1.5]); plot_predictions(polynomial_svm_clf,[-1.5,2.5,-1,1.5])



## Polynomial Kernel
from sklearn.svm import SVC
poly_kernel_svm_clf = Pipeline([
    ('scaler',StandardScaler()),
    ('svm_clf',SVC(kernel='poly',degree=3,coef0=1,C=5)), # coef0 controls how much the model is influenced by high-degree polynomials
])
poly_kernel_svm_clf.fit(X,y)



## Gaussian RBF Kernel
'''
Gaussian Radial Basis Function: a bell shape curve. when $\gamma$ increases, the curve narrows
$\phi_{\gamma}(x,l) = exp(- \gamma ||x-l||^2)$
l is landmark.
'''
rbf_kernel_svm_clf = Pipeline([
    ('scaler',StandardScaler()),
    ('svm_clf',SVC(kernel='rbf',gamma=5,C=0.001)) # smaller gamma will cause smoother boundary
])
rbf_kernel_svm_clf.fit(X,y)




# SVM Regression
X = np.random.randn(100,1)
y = np.random.randn(100,1) + 2*X + 3*X**2
from sklearn.svm import LinearSVR
svm_reg = LinearSVR(epsilon=1.5) # larger epsilon means wider street
svm_reg.fit(X,y)
temp = np.linspace(-1.5,2.5,100).reshape(100,1)
y_pred = svm_reg.predict(temp)
plt.plot(temp, y_pred)
plt.plot(temp, y_pred + svm_reg.epsilon, "k--")
plt.plot(temp, y_pred - svm_reg.epsilon, "k--")
plt.scatter(X,y) # Obviously, for a quardic relationship, liner SVM does poorly
'''
for Polynomial Situation
'''
from sklearn.svm import SVR
svm_poly_reg = SVR(kernel='poly',degree=2,C=100,epsilon=0.1)
svm_poly_reg.fit(X,y)
temp = np.linspace(-1.5,2.5,100).reshape(100,1)
y_pred = svm_poly_reg.predict(temp)
plt.plot(temp, y_pred)
plt.plot(temp, y_pred + svm_poly_reg.epsilon, "k--")
plt.plot(temp, y_pred - svm_poly_reg.epsilon, "k--")
plt.scatter(X,y)

svm_poly_reg2 = SVR(kernel='poly',degree=3,C=100,epsilon=0.1) # delibreately overfit
svm_poly_reg2.fit(X,y)
temp = np.linspace(-1.5,2.5,100).reshape(100,1)
y_pred = svm_poly_reg2.predict(temp)
plt.plot(temp, y_pred)
plt.plot(temp, y_pred + svm_poly_reg2.epsilon, "k--")
plt.plot(temp, y_pred - svm_poly_reg2.epsilon, "k--")
plt.scatter(X,y)
