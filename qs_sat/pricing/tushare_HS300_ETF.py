from datetime import datetime as dt, timedelta as td
import os
import sys
sys.path.append(os.path.join('..','pricing'))

import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import ( LinearDiscriminantAnalysis as LDA, QuadraticDiscriminantAnalysis as QDA )
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC, SVC

from tu_share import TuShare

def create_lagged_series(Vendor, symbol, start_date, end_date, lags=5):
    """
    This creates a Pandas DataFrame that stores the
    percentage returns of the adjusted closing value of
    a stock obtained from Tushare, along with a
    number of lagged returns from the prior trading days
    (lags defaults to 5 days). Trading volume, as well as
    the Direction from the previous day, are also included.

    Parameters
    ----------
    tu : 'TuShare' The Tushare API instance used to obtain pricing
    symbol : 'str' The ticker symbol to obtain from Tushare
    start_date : 'datetime' The starting date of the series to obtain
    end_date : 'datetime' The ending date of the the series to obtain
    lags : 'int', optional The number of days to 'lag' the series by, default is 5

    Returns
    -------
    'pd.DataFrame' Contains the Adjusted Closing Price returns and lags
    """
    # Obtain stock pricing from Tushare
    adj_start_date = start_date - td(days=365)
    adj_start_date = adj_start_date.strftime('%Y%m%d')
    end_date = end_date.strftime('%Y%m%d')

    ts = Vendor.get_daily_historic_data(symbol, adj_start_date, end_date, asset='FD', adj=None)
    print(ts.head(10))
    # Create the new lagged DataFrame
    tslag = pd.DataFrame(index=ts.index)
    tslag['Today'] = ts['close'] * ts['adj_factor']
    tslag['Volume'] = ts['vol']
    print(tslag.head(10))
    # Create the shifted lag series of prior trading period close values
    for i in range(0, lags):
        tslag['Lag%s' % str(i+1)] = tslag['Today'].shift(i+1)

    # Create the returns DataFrame
    tsret = pd.DataFrame(index=tslag.index)
    tsret['Volume'] = tslag['Volume']
    tsret['Today'] = tslag['Today'].pct_change() * 100.0

    # If any of the values of percentage returns equal zero, set them to a small number (stops issues with QDA model in scikit-learn)
    tsret.loc[tsret['Today'].abs() < 0.0001, ['Today']] = 0.0001

    # Create the lagged percentage returns columns
    for i in range(0, lags):
        tsret['Lag%s' % str(i+1)] = tslag['Lag%s' % str(i+1)].pct_change() * 100.0

    # Create the "Direction" column (+1 or -1) indicating an up/down day
    tsret['Direction'] = np.sign(tsret['Today'])
    tsret = tsret[tsret.index >= dt(2016,1,20)]
    print(tsret.head(10))
    return tsret

if __name__ == "__main__":
    # Create an Tushare API instance
    tu = TuShare()

    # Download the HS300 ETF time series
    start_date = dt(2016, 1, 1)
    end_date = dt(2020, 2, 14)

    # Create a lagged series of the HS300 China stock market index ETF
    hsret = create_lagged_series(tu, '510300', start_date, end_date, lags=5)

    # Use the prior two days of returns as predictor values, with direction as the response
    X = hsret[['Lag1', 'Lag2']]
    y = hsret['Direction']

    # The test data is split into two parts: Before and after 1st Jan 2017.
    start_test = dt(2018, 12, 31)

    # Create training and test sets
    X_train = X[X.index < start_test]
    X_test = X[X.index >= start_test]
    y_train = y[y.index < start_test]
    y_test = y[y.index >= start_test]

    # Create the (parametrised) models
    print('Hit Rates/Confusion Matrices:\n')
    models = [
        ('LR', LogisticRegression(solver='liblinear')),
        ('LDA', LDA(solver='svd')),
        ('QDA', QDA()),
        ('LSVC', LinearSVC(max_iter=10000)),
        ('RSVM', SVC(
            C=1000000.0, cache_size=200, class_weight=None,
            coef0=0.0, degree=3, gamma=0.0001, kernel='rbf',
            max_iter=-1, probability=False, random_state=None,
            shrinking=True, tol=0.001, verbose=False)
        ),
        ('RF', RandomForestClassifier(
            n_estimators=1000, criterion='gini',
            max_depth=None, min_samples_split=2,
            min_samples_leaf=1, max_features='auto',
            bootstrap=True, oob_score=False, n_jobs=1,
            random_state=None, verbose=0)
        )
    ]

    # Iterate through the models
    for m in models:
        # Train each of the models on the training set
        m[1].fit(X_train, y_train)

        # Make an array of predictions on the test set
        pred = m[1].predict(X_test)

        # Output the hit-rate and the confusion matrix for each model
        print('%s:\n%0.3f' % (m[0], m[1].score(X_test, y_test)))
        print('%s\n' % confusion_matrix(pred, y_test))


