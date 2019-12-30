# Decision Tree
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
iris = load_iris()
X = iris['data'][:,2:]
y = iris['target']

tree_clf = DecisionTreeClassifier(max_depth=2)
tree_clf.fit(X,y)
'''
Gini impurity:
    $G_i = 1 - \sum_{k=1}^n{p_{i,k}^2}$
$p_{i,k}$ is (instances of class K)/(training instances in i-th node)
    in other words, the probability that the predicted instance in class K
if Gini is 0, then all instances in the node are in same class, thus it's pure
'''
tree_clf.predict_proba([[5,1.5]])
tree_clf.predict([[5,1.5]])
'''
90% possibility in ClassII, obviously, this node is not pure -- maybe more sub classes could be divided
Probability: array([[0., 0.90740741, 0.09259259]])
Prediction: array([1])
'''
from sklearn.tree import export_graphviz
export_graphviz(
    tree_clf,
    out_file='iris_tree.dot',
    feature_names=iris.feature_names[2:],
    class_names=iris.target_names,
    rounded=True,
    filled=True
)
'''
Execute the following command in Linux:
sudo apt install graphviz
dot -Tpng iris_tree.dot -o iris_tree.png
'''