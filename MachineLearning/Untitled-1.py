from sklearn.datasets import fetch_openml
# Fetch MINST from web
mnist = fetch_openml('mnist_784', version=1)
from sklearn.externals import joblib
joblib.dump(mnist, 'MNIST.pkl')
mnist = joblib.load('MNIST.pkl')

import numpy as np
X, y = mnist['data'], mnist['target']
y = y.astype(int)
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
## cross-validation with K-fold
from sklearn.model_selection import cross_val_score
cross_val_score(sgd_clf, X_train, y_train_5, cv=3, scoring='accuracy')
'''
array([0.9662 , 0.96045, 0.9534 ])
'''
## Actually, if the algo sets all predictions as non-5, then the accuracy is 90%
## Thus accuracy is not an ideal standard for classification

## A Cunfusion Matrix is a better way for this purpose
from sklearn.model_selection import cross_val_predict
y_train_pred = cross_val_predict(sgd_clf, X_train, y_train_5, cv=3)
from sklearn.metrics import confusion_matrix
confusion_matrix(y_train_5, y_train_pred)
'''
        True Negative, False Positive
array([[53794,         785],
       [ 1614,         3807]], dtype=int64)
       False Negative, True Positive
'''
from sklearn.metrics import precision_score, recall_score
precision_score(y_train_5, y_train_pred)
'''
Probability of correct when make a Positive prediction
0.8290505226480837 = \frac{TP}{TP+FP}
'''
recall_score(y_train_5, y_train_pred)
'''
Detection Rate for '5'
0.7022689540675152 = \frac{TP}{TP+FN}
'''