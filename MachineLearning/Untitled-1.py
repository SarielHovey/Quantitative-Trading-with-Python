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

