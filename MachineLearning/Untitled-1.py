# Linear SVM Classification
## Soft Margin Classification
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




# Nonlinear SVM Classification
from sklearn.datasets import make_moons
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures

X, y = make_moons(n_samples=5000, noise=0.15)
polynomial_svm_clf = Pipeline([
    ('poly_features',PolynomialFeatures(degree=3)),
    ('scaler',StandardScaler()),
    ('svm_clf',LinearSVC(C=10,loss='hinge'))
])
polynomial_svm_clf.fit(X,y)