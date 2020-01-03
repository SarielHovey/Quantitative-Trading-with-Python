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
X, y = make_moons(n_samples=5000, noise=0.15)
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
This model could be parallel run
'''
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
bag_clf = BaggingClassifier(
    DecisionTreeClassifier(), n_estimators=500,
    max_samples=100, bootstrap=True,n_jobs=-1
) # automaticly use soft vote if algo used has predict_probab() method
bag_clf.fit(X_train,y_train)
y_pred = bag_clf.predict(X_val)
print(bag_clf.__class__.__name__, accuracy_score(y_val, y_pred))
'''
BaggingClassifier 0.979
'''