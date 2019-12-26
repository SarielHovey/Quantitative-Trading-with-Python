from sklearn.datasets import fetch_openml
# Fetch MINST from web
mnist = fetch_openml('mnist_784', version=1)
from sklearn.externals import joblib
joblib.dump(mnist, 'MNIST.pkl')
mnist = joblib.load('MNIST.pkl')

import numpy as np; from matplotlib.pyplot import matshow
X, y = mnist['data'], mnist['target']
y = y.astype(int)
X_train, X_test, y_train, y_test = X[:60000], X[60000:], y[:60000], y[60000:]
temp = X_train[0].copy()
temp = temp.reshape(28,28)
matshow(temp) # Take a look at MNIST pixel images
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
0.8290505226480837 = $\frac{TP}{TP+FP}$
'''
recall_score(y_train_5, y_train_pred)
'''
Detection Rate for '5'
0.7022689540675152 = $\frac{TP}{TP+FN}$
'''
from sklearn.metrics import f1_score
f1_score(y_train_5, y_train_pred)
'''
f1 = $\frac{2}{1/precision + 1/recall}$
0.760411465095376
'''

## There's always a tradeoff between precision and recall
y_scores = cross_val_predict(sgd_clf, X_train, y_train_5, cv=3, method='decision_function')
from sklearn.metrics import precision_recall_curve
precision, recall, threshold = precision_recall_curve(y_train_5, y_scores)
import matplotlib.pyplot as plt
plt.plot(threshold, precision[:-1], 'b--', label='Precision')
plt.plot(threshold, recall[:-1], 'g-', label='Recall')
plt.xlabel('Threshold')
plt.title('Tradeoff Between Precision & Recall')
plt.legend(loc=0) # Could be interger 0-10

threshold_95_precision = threshold[np.argmax(precision >= .95)]
y_train_pred_95 = (y_scores >= threshold_95_precision)
precision_score(y_train_5, y_train_pred_95), recall_score(y_train_5, y_train_pred_95)
'''
With 90% Precision, Recall is 59.77%
With 95% Precision, Recall is 44.9%
With 99% Precision, Recall is 0.5534%
Obviously, A high Precision classifier tend to have a very low Recall(Detection Rate)
'''



# Use a Receiver Operating Characteristic Curve (ROC)
## PR Curve is preferred when (1) Positive Class is rare
##                            (2) False Positive is more important than FN
## $ROC = \frac{TP/(TP + FN)}{1 - TN/(FP+TN)}$
from sklearn.metrics import roc_curve
fpr, tpr, threshold = roc_curve(y_train_5, y_scores)
plt.plot(fpr, tpr, linewidth=2)
plt.plot([0,1],[0,1], 'k--', label= 'ROC of a purely random classifier')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Tradeoff between TPR & FPR')

from sklearn.metrics import roc_auc_score
roc_auc_score(y_train_5, y_scores)
'''
Area Under the Curve. [0.5, 1], 1 is the best.
0.9593580597259379
'''

## Random Forest Classifier
from sklearn.ensemble import RandomForestClassifier
forest_clf = RandomForestClassifier(random_state=43)
y_probas_forest = cross_val_predict(forest_clf, X_train, y_train_5, cv=3, method='predict_proba')
'''
Probability of not being 5; Probability of being 5
array([[0. , 1. ],
       [1. , 0. ],
       [1. , 0. ],
       ...,
       [0. , 1. ],
       [1. , 0. ],
       [0.8, 0.2]])
'''
y_scores_forest = y_probas_forest[:,1]
fpr_forest, tpr_forest, threshold_forest = roc_curve(y_train_5, y_scores_forest)
plt.plot(fpr, tpr, 'b:', label='SGD')
plt.plot(fpr_forest, tpr_forest, label='Random Forest')
plt.plot([0,1],[0,1], 'k--', label= 'ROC of a purely random classifier')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc=0)

roc_auc_score(y_train_5, y_scores_forest)
'''
Larger than SGD's 0.959358, an improvement
0.9931536262180866
'''



# Multiclass Classification
from sklearn.svm import SVC
svm_clf = SVC()
svm_clf.fit(X_train, y_train)
svm_clf.predict(X_train[0])

sample_score = svm_clf.decision_function([X_train[0]])
np.argmax(sample_score)
'''
'''
svm_clf.classes_
'''
List of target classes, ordered automatically
'''



# Error Analysis
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train.astype(np.float64))
cross_val_score(sgd_clf, X_train_scaled, y_train, cv=3, scoring='accuracy')
'''
array([0.90546891, 0.90819541, 0.9119868 ])
'''
y_train_pred = cross_val_predict(sgd_clf, X_train, y_train, cv=3)
conf_mx = confusion_matrix(y_train, y_train_pred)
'''
array([[5710,    1,   17,   28,   25,   52,   33,    4,   33,   20],
       [   1, 6387,   31,   70,   15,   24,    7,   22,  171,   14],
       [  94,  109, 4776,  341,  122,   71,  133,  100,  166,   46],
       [  43,   26,   73, 5356,   32,  227,   27,   84,  128,  135],
       [  18,   15,   33,   37, 5178,   27,   81,   29,  116,  308],
       [ 102,   14,   22,  374,   98, 4239,  114,   23,  327,  108],
       [  61,   28,   35,   19,   86,  172, 5459,    2,   53,    3],
       [  29,   19,   32,   37,   89,   16,    7, 5631,   40,  365],
       [  54,  195,   61,  288,  141,  461,   70,   55, 4246,  280],
       [  32,   22,   23,  110,  272,   82,    7,  353,   48, 5000]],
      dtype=int64)
'''
plt.matshow(conf_mx, cmap=plt.cm.gray) # Lighter the color, more values found
row_sums = conf_mx.sum(axis=1, keepdims=True)
norm_conf_mx = conf_mx / row_sums
'''
Alternatively:
conf_mx = np.matrix(conf_mx)
norm_conf_mx = conf_mx / conf_mx.sum(axis=1)
'''
np.fill_diagonal(norm_conf_mx, 0) # Only elements not on diagonal are error
plt.matshow(norm_conf_mx, cmap=plt.cm.gray)
plt.xlabel('Predicted Class')
plt.ylabel('Actual Class')
'''
After normalized, it shows:
(2,3),(5,3),(5,8),(7,9),(8,5) tend to be confused by classifier
Thus efforts could be spent on above to enhance classifierx
'''


