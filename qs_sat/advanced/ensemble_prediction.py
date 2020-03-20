import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sklearn
from sklearn.ensemble import ( BaggingRegressor, RandomForestRegressor, AdaBoostRegressor)
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from sklearn.tree import DecisionTreeRegressor

plt.style.use('seaborn')

from create_lagged_series import create_lagged_series



if __name__ == '__main__':
    # We could see how bagging, boosting could imporve MSE gradually
    # Set the random seed, number of estimators and the "step factor" used to plot the graph of MSE for each method
    random_state = 42
    n_jobs = 6 # Parallelisation factor for bagging, random forests
    n_estimators = 1000
    step_factor = 10
    axis_step = int(n_estimators/step_factor)

    # CS adjusted closing prices
    start_date = datetime.datetime(2010, 1, 1)
    end_date = datetime.datetime(2020, 3, 19)
    cs = create_lagged_series('CS',start_date,end_date, lags=3)
    cs.dropna(inplace=True)

    # Use the first three daily lags of CS closing prices and scale the data to lie within -1 and +1 for comparison
    X = cs[['Lag1', 'Lag2', 'Lag3']]
    y = cs['Today']
    X = scale(X)
    y = scale(y)

    # Use the training-testing split with 70% of data in the training data with the remaining 30% of data in the testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # Pre-create the arrays which will contain the MSE for each particular ensemble method
    estimators = np.zeros(axis_step)
    bagging_mse = np.zeros(axis_step)
    rf_mse = np.zeros(axis_step)
    boosting_mse = np.zeros(axis_step)

    # Estimate the Bagging MSE over the full number of estimators, across a step size ("step_factor")
    for i in range(0, axis_step):
        print("Bagging Estimator: %d of %d..." % (step_factor*(i+1), n_estimators))
        bagging = BaggingRegressor(
            DecisionTreeRegressor(), n_estimators=step_factor*(i+1), n_jobs=n_jobs
        )
        bagging.fit(X_train, y_train)
        mse = mean_squared_error(y_test, bagging.predict(X_test))
        estimators[i] = step_factor*(i+1)
        bagging_mse[i] = mse

    # Estimate the Random Forest MSE over the full number of estimators, across a step size ("step_factor")
    for i in range(0, axis_step):
        print("Random Forest Estimator: %d of %d..." % (step_factor*(i+1), n_estimators))
        rf = RandomForestRegressor(
            n_estimators=step_factor*(i+1), n_jobs=n_jobs
        )
        rf.fit(X_train, y_train)
        mse = mean_squared_error(y_test, rf.predict(X_test))
        estimators[i] = step_factor*(i+1)
        rf_mse[i] = mse

    # Estimate the AdaBoost MSE over the full number of estimators, across a step size ("step_factor")
    for i in range(0, axis_step):
        print("Boosting Estimator: %d of %d..." % (step_factor*(i+1), n_estimators))
        boosting = AdaBoostRegressor(
            DecisionTreeRegressor(), n_estimators=step_factor*(i+1), learning_rate=0.01
        )
        boosting.fit(X_train, y_train)
        mse = mean_squared_error(y_test, boosting.predict(X_test))
        estimators[i] = step_factor*(i+1)
        boosting_mse[i] = mse

    # Plot the chart of MSE versus number of estimators
    # Caution: Boosting could lead to significant oveffit, as shown
    plt.figure(figsize=(8, 8))
    plt.title('Bagging, Random Forest and Boosting comparison')
    plt.plot(estimators, bagging_mse, 'b-', color="black", label='Bagging')
    plt.plot(estimators, rf_mse, 'b-', color="blue", label='Random Forest')
    plt.plot(estimators, boosting_mse, 'b-', color="red", label='AdaBoost')
    plt.legend(loc='upper right')
    plt.xlabel('Estimators') 
    plt.ylabel('Mean Squared Error')
    plt.show()