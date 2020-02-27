from datetime import datetime as dt

from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

from create_lagged_series import create_lagged_series

if __name__ == "__main__":
    snpret = create_lagged_series( "SPY", dt(2015,1,10), dt(2019,12,31), lags=5)

    X = snpret[["Lag1","Lag2"]]
    y = snpret["Direction"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

    # Set the parameters by cross-validation
    tuned_parameters = [
        {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}
        ]
    
    model = GridSearchCV(SVC(C=1), tuned_parameters, cv=10)
    model.fit(X_train, y_train)

    print("Optimised parameters found on training set:")
    print(model.best_estimator_, "\n")

    print("Grid scores calculated on training set:")
    print(DataFrame(model.cv_results_)[['params','mean_test_score','std_test_score','rank_test_score']])