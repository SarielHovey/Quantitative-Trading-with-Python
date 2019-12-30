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
if Gini is 0, then all instances in the node are in same class, thus it's pure
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