import datetime

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import (LinearDiscriminantAnalysis as LDA, QuadraticDiscriminantAnalysis as QDA)
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC, SVC

from create_lagged_series import create_lagged_series


if __name__ == "__main__":
    # Create a lagged series of the S&P500 US stock market index
    snpret = create_lagged_series("SPY", datetime.datetime(2016,1,10), datetime.datetime(2017,12,31), lags=5)

    # Use the prior three days of returns as predictor values, with direction as the response
    X = snpret[["Lag1","Lag2","Lag3"]]
    y = snpret["Direction"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=43)

    # Create the (parametrised) models
    print("Hit Rates/Confusion Matrices:\n")
    models = [("LR", LogisticRegression()),
        ("LDA", LDA()),
        ("QDA", QDA()),
        ("LSVC", LinearSVC()),
        ("RSVM", SVC(
            C=1000000.0, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0.0001, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False)
        ),
        ("RF", RandomForestClassifier(
            n_estimators=1000, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, max_features='auto', bootstrap=True, oob_score=False, n_jobs=1, random_state=None, verbose=0)
        )]

    # Iterate through the models
    for m in models:
        # Train each of the models on the training set
        m[1].fit(X_train, y_train)

        # Make an array of predictions on the test set
        pred = m[1].predict(X_test)

        # Output the hit-rate and the confusion matrix for each model
        print("%s:\n%0.3f" % (m[0], m[1].score(X_test, y_test)))
        print("%s\n" % confusion_matrix(pred, y_test))
