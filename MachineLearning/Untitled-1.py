from sklearn.datasets import fetch_openml
# Fetch MINST from web
mnist = fetch_openml('mnist_784', version=1)
from sklearn.externals import joblib
joblib.dump(mnist, 'MNIST.pkl')
mnist = joblib.load('MNIST.pkl')

import numpy as np
y = y.astype(int)
X, y = mnist['data'], mnist['target']
X_train, X_test, y_train, y_test = X[:60000], X[60000:], y[:60000], y[60000:]
y_train_5 = (y_train == 5)
y_test_5 = (y_test ==5)
'''
array([ True, False, False, ...,  True, False, False])
'''

# Use a Stochastic Gradient Descent classifier to run a naive classification
from sklearn.linear_model import SGDClassifier
sgd_clf = SGDClassifier(random_state=43)
sgd_clf.fit(X_train, y_train_5)



