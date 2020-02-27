# Caution: K-fold-cross-validation should not be used on time series since the order matters
from datetime import datetime as dt

import pandas as pd
import sklearn
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.model_selection import KFold

from create_lagged_series import create_lagged_series

if __name__ == "__main__":
    snpret = create_lagged_series( "SPY", dt(2016,1,10), dt(2017,12,31), lags=5)

    X = snpret[["Lag1","Lag2"]]
    y = snpret["Direction"]

    # Create a k-fold cross validation object
    kf = KFold(n_splits=10, shuffle=True, random_state=42)

    # Use the kf object to create index arrays that state which elements have been retained 
    # for training and which elements have beenr retained for testing
    #  for each k-element iteration
    for train_index, test_index in kf.split(X):
        X_train = X.loc[X.index[train_index]]
        X_test = X.loc[X.index[test_index]]
        y_train = y.loc[y.index[train_index]]
        y_test = y.loc[y.index[test_index]]

        print("Hit Rate/Confusion Matrix:")
        model = SVC(
            C=1000000.0, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0.0001, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False
            )
        
        model.fit(X_train, y_train)
        pred = model.predict(X_test)

        print("%0.3f" % model.score(X_test, y_test))
        print("%s\n" % confusion_matrix(pred, y_test))