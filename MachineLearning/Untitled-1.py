# Voting Classifier
'''
Use a group of different algorithms on the same training set
Hard Vote: aggreate predictions of each classifier and predict the class with most votes
Soft Vote: predict the class with highest probability, need all clf have predict_proba() method
'''
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from sklearn.model_selection import train_test_split
from sklearn.datasets import make_moons
X, y = make_moons(n_samples=500, noise=0.15)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=.2)

log_clf = LogisticRegression()
rnd_clf = RandomForestClassifier()
svm_clf = SVC()
voting_clf = VotingClassifier(
    estimators=[('lr',log_clf),('rf',rnd_clf),('svc',svm_clf)],voting='hard'
)
voting_clf.fit(X_train, y_train)

from sklearn.metrics import accuracy_score
for clf in (log_clf, rnd_clf, svm_clf, voting_clf):
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_val)
    print(clf.__class__.__name__, accuracy_score(y_val, y_pred))
'''
Compared with hard vote:
LogisticRegression 0.893
RandomForestClassifier 0.986
SVC 0.988
VotingClassifier 0.986
'''

log_clf = LogisticRegression()
rnd_clf = RandomForestClassifier()
svm_clf = SVC(probability=True) # change default so svm has predict_probab() method
voting_clf = VotingClassifier(
    estimators=[('lr',log_clf),('rf',rnd_clf),('svc',svm_clf)],voting='soft'
)
for clf in (log_clf, rnd_clf, svm_clf, voting_clf):
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_val)
    print(clf.__class__.__name__, accuracy_score(y_val, y_pred))
'''
Compared with soft vote:
LogisticRegression 0.893
RandomForestClassifier 0.988
SVC 0.988
VotingClassifier 0.984
'''



# Bagging and Pasting
'''
Use the same training algorithm on different random subsets of the training set
Bootstrap aggregating: sample with replacement 有放回
Pasting: sample without replacement 无放回
Prediction is made by aggregating the predictions of all predictors
e.g. below is an ensemble of 500 Decision Trees
This model could be parallel run
'''
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
bag_clf = BaggingClassifier(
    DecisionTreeClassifier(), n_estimators=500,
    max_samples=100, bootstrap=True,n_jobs=-1
) # automaticly use soft vote if algo used has predict_probab() method
# n_jobs is the number of cpu cores to use. -1 means all
bag_clf.fit(X_train,y_train)
y_pred = bag_clf.predict(X_val)
print(bag_clf.__class__.__name__, accuracy_score(y_val, y_pred))
'''
BaggingClassifier 0.974
'''
pas_clf = BaggingClassifier(
    DecisionTreeClassifier(), n_estimators=500,
    max_samples=100, bootstrap=False,n_jobs=-1
)
pas_clf.fit(X_train,y_train)
y_pred = pas_clf.predict(X_val)
print('PassingClassifier ', accuracy_score(y_val, y_pred))
'''
PassingClassifier 0.976
'''


## Out-of-Bag Evaluation
'''
With bagging, some instances in training set may never be chosen for training
Thus they could be used for model evaluation
'''
bag_clf = BaggingClassifier(
    DecisionTreeClassifier(), n_estimators=500,
    max_samples=100, bootstrap=True,n_jobs=-1,oob_score=True
)
bag_clf.fit(X_train,y_train)
bag_clf.oob_score_
'''
Out-of-Bag evaluation: 0.975
'''
y_pred = bag_clf.predict(X_val)
accuracy_score(y_val, y_pred)
'''
BaggingClassifier: 0.976
'''
bag_clf.oob_decision_function_
'''
class probability for each training instance
shape: (4000,2) # 5000*.8=4000
array([[1.        , 0.        ],
       [0.05590062, 0.94409938],
       [0.01629328, 0.98370672],
       ...,
       [0.9958159 , 0.0041841 ],
       [1.        , 0.        ],
       [0.01229508, 0.98770492]])
'''



# Random Forest
'''
Random Forest is an ensemble of Decision Trees, with max_samples = size of training set
'''
from sklearn.ensemble import RandomForestClassifier
rnd_clf = RandomForestClassifier(n_estimators=500,max_leaf_nodes=16,n_jobs=-1)
rnd_clf.fit(X_train,y_train)
y_pred = rnd_clf.predict(X_val)
accuracy_score(y_val, y_pred)
'''
Random Forest Classifier: 0.986
the same could be achieved by bag_clf
bag_clf = BaggingClassifier(
    DecisionTreeCalssifier(splitter='random',max_leaf_nodes=16),
    n_estimators=500,max_samples=1.0,bootstrap=True,n_jobs=-1
)
'''
## Extremely Randomized Tree
'''
Use random threshold for each feature rather than find the best threshold
'''
from sklearn.ensemble import ExtraTreesClassifier
ext_clf = ExtraTreesClassifier(n_estimators=500,max_leaf_nodes=16,n_jobs=-1)
ext_clf.fit(X_train,y_train)
y_pred = ext_clf.predict(X_val)
accuracy_score(y_val,y_pred)
'''
0.972
'''


## Feature Importance
from sklearn.datasets import load_iris
iris = load_iris()
rnd_clf = RandomForestClassifier(n_estimators=500,n_jobs=-1)
rnd_clf.fit(iris['data'],iris['target'])
for name, score in zip(iris['feature_names'], rnd_clf.feature_importances_):
    print(name, score)
'''
features that reduce more tree node impurity on average are more important
e.g. in below iris case, petal length and petal width are more important
sepal length (cm) 0.09689148671472861
sepal width (cm) 0.02361549853925849
petal length (cm) 0.4537043793462725
petal width (cm) 0.42578863539974043
'''



# Boosting (Hypothesis Boosting)
'''
Train predictors sequentially, each trying to correct the previous one
'''

## AdaBoost
'''
Train and evaluate the 1st predictor, then increase the relative weight of misclassified training instances for the next predictor.
Weighted error rate of the j-th predictor:
    $r_j = \sum^m_{i=1, \hat{y_ij}!=y_i}w_i / \sum^m_i{w_i}$
    $\hat{y_ij}$ is the j-th predictor's prediction for the i-th instance

Predictor weight:
    $\alpha_j = \eta log(\frac{1-r_j}{r_j})$
    $\eta$ is learning rate hypermeter(default 1)
    better predictor j will have higher alpha

Weight update rule:
    Initial weight for i-th instance: $1/m$
    for j = 1:
        for i = 1 to m:
            if $\hat{y_ij} == y_i$, $w_i = w_i$
            if $\hat{y_ij} != y_i$, $w_i = w_i*exp(\alpha_j)$
            $w_i / \sum^m_i{w_i}$ to normalize
            j += 1

AdaBoost Predictions:
    $\hat{y}(x) = argmax_k \sum^N_{j=1,\hat{y_j}(x)=k}\alpha_j$
'''
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_moons
X, y = make_moons(n_samples=5000, noise=0.15)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=.2)

from sklearn.ensemble import AdaBoostClassifier
ada_clf = AdaBoostClassifier(
    DecisionTreeClassifier(max_depth=1), n_estimators=200,
    algorithm='SAMME.R',learning_rate=.5
)
ada_clf.fit(X_train,y_train)
y_pred = ada_clf.predict(X_val)
accuracy_score(y_pred,y_val)
'''
0.99
'''


## Gradient Boosting
'''
fit new predictor to residual errors made by the previous predictor
'''
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
tree_reg1 = DecisionTreeRegressor(max_depth=2)
tree_reg1.fit(X_train,y_train)
y_pred1 = tree_reg1.predict(X_val)
mean_squared_error(y_pred1,y_val)
y2_train = y_train - tree_reg1.predict(X_train)
tree_reg2 = DecisionTreeRegressor(max_depth=2)
tree_reg2.fit(X_train, y2_train)
y_pred2 = sum(tree.predict(X_val) for tree in (tree_reg1,tree_reg2))
mean_squared_error(y_pred2,y_val)
y3_train = y2_train - tree_reg2.predict(X_train)
tree_reg3 = DecisionTreeRegressor(max_depth=2)
tree_reg3.fit(X_train, y3_train)
y_pred3 = sum(tree.predict(X_val) for tree in (tree_reg1,tree_reg2,tree_reg3))
mean_squared_error(y_val,y_pred3)
'''
Theoretically, score should increase by stage
1st-stage RMSE: 0.07250688154031396
2nd-stage RMSE: 0.06358319167774763
3rd-stage RMSE: 0.05591011157360547
Or use the provided class in sklearn
'''
from sklearn.ensemble import GradientBoostingRegressor
gbrt = GradientBoostingRegressor(max_depth=2, n_estimators=3, learning_rate=1.0)
gbrt.fit(X_train,y_train)
y_pred = gbrt.predict(X_val)
mean_squared_error(y_pred,y_val)
'''
RMSE: 0.05591011157360515
Notice that this almost equals 3rd-stage RMSE above since these 2 ways are equivalent
'''
gbrt2 = GradientBoostingRegressor(max_depth=2, n_estimators=300, learning_rate=0.1)
gbrt2.fit(X_train,y_train)
y_pred2 = gbrt2.predict(X_val)
mean_squared_error(y_pred2,y_val)
gbrt3 = GradientBoostingRegressor(max_depth=2, n_estimators=3, learning_rate=0.1)
gbrt3.fit(X_train,y_train)
y_pred3 = gbrt3.predict(X_val)
mean_squared_error(y_pred3,y_val)
'''
gbrt RMSE: 0.05591011157360515
gbrt2 RMSE: 0.014771576749491906
gbrt3 RMSE: 0.1671436853369599
Higher Learning Rate requires less trees, but may cause underfit
Lower Learning Rate need more trees to fit the model, but may cause overfit
'''

### Try Gradiant Boosting with early stopping
### increase n_estimators if len(error) == np.argmin(errors)
import numpy as np
gbrt = GradientBoostingRegressor(max_depth=2,n_estimators=1200)
gbrt.fit(X_train,y_train)
errors = [mean_squared_error(y_val, y_pred) for y_pred in gbrt.staged_predict(X_val)]
bst_n_estimators = np.argmin(errors) +1
'''
Error should decrease with increase of number of estimators, then increase again
len(errors):1200
best_number_of_estimators:900
'''
gbrt_best = GradientBoostingRegressor(max_depth=2,n_estimators=bst_n_estimators)
gbrt_best.fit(X_train,y_train)
[mean_squared_error(y_val, y_pred) for y_pred in [gbrt.predict(X_val),gbrt_best.predict(X_val)]]
'''
We see a decrease in RMSE (almost)
0.012676838548715512
0.012269630397207795
Alternatively, use warm_start param
'''
gbrt = GradientBoostingRegressor(max_depth=2, warm_start=True)
min_val_error = float('inf')
error_going_up = 0
for n_estimators in range(1,1200):
    gbrt.n_estimators = n_estimators
    gbrt.fit(X_train,y_train)
    y_pred = gbrt.predict(X_val)
    val_err = mean_squared_error(y_val,y_pred)
    if val_err < min_val_error:
        min_val_error = val_err
        error_going_up = 0
    else:
        error_going_up += 1
        if error_going_up == 10:
            break
'''
error_going_up = 5:
    gbrt.n_estimators: 627
    RMSE: 0.012722023493901148
With error_going_up = 5, we may be trapped in a local min
If ignore overfit, 10 may be the best choice
error_going_up = 10:
    gbrt.n_estimators: 707
    RMSE: 0.012564108480654278
error_going_up = 20:
    gbrt.n_estimators: 717
    RMSE: 0.01256978293815527
'''
## For Performance, use xgboost for Extreme Gradiant Boosting
import xgboost
xgb_reg = xgboost.XGBRegressor()
xgb_reg.fit(X_train,y_train)
y_pred = xgb_reg.predict(X_val)
mean_squared_error(y_pred,y_val)
xgb_reg.fit(X_train,y_train,eval_set=[(X_val, y_val)],early_stopping_rounds=3)
y_pred = xgb_reg.predict(X_val)
mean_squared_error(y_pred,y_val)
'''
RMSE: 0.01322858967276241
RMSE with early stopping: 0.01322858967276241
'''



# Stacking
