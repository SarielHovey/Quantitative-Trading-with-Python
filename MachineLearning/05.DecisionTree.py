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
90% possibility in ClassII
obviously, this node is not pure -- maybe more sub classes could be divided
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


## Classification and Regression Tree (CART) Training Algorithm
'''
CART Cost function for classification:
    $J(k,t_k) = \frac{m_l}{m}G_l + \frac{m_r}{m}G_r$
    where $G_l$ or $G_r$ measures impurity of left/right subset;
        $m_l$ or $m_r$ is the number of instances in the left/right subset
$(k,t_k)$ minimize cost function for the current depth -- may not be global optimal
'''


## Entropy
'''
$H_i = - \sum^n_{k=1,p_ik\not=0} p_ik log_2(p_ik)$
For performance, use Gini
'''


## Regularization Hyperparameters
'''
Decision Tree is a typical nonparametric model, with few assemption about training data, and number of paras 
not pre-determined before training.
The model is prone to overfitting, thus needs regularization.
'''
tree_clf = DecisionTreeClassifier(max_depth=2,min_samples_leaf=2,min_samples_split=.2,min_weight_fraction_leaf=2,
max_leaf_nodes=50,max_features=50)
tree_clf.fit(X,y)



# Decision Tree Regression
'''
CART Cost function for regression:
    $J(k,t_k) = \frac{m_l}{m}MSE_l + \frac{m_r}{m}MSE_r$
    where $\hat{y}_{node} = mean_{node}(y_i)$; $MSE_{node} = \sum_{i in node}(\hat{y}_{node}-y_i)^2 $
'''
from sklearn.tree import DecisionTreeRegressor
import numpy as np
tree_reg = DecisionTreeRegressor(max_depth=2)
X = np.random.randn(200).reshape(200,1)
y = .5*X**2 + 3*X + np.random.randn(200)
y = y.reshape(200,1)
tree_reg.fit(X,y)
export_graphviz(
    tree_reg,
    out_file='tree_reg.dot',
    rounded=True,
    filled=True
)
tree_reg.predict([[.3],[.4],[.7]])
def f(x):
    return .5*x**2 + 3*x
[f(x) for x in [0.3,0.4,0.7]]
'''
Very bad regression, mean value is used on large range
array([-0.24079714, -0.24079714,  2.95530098])
Benchmk:[0.945, 1.2800000000000002, 2.3449999999999998]
'''
tree_reg2 = DecisionTreeRegressor()
tree_reg2.fit(X,y)
tree_reg2.predict([[.3],[.4],[.5]])
'''
Better, but severe overfit, since with no regularization,
regressor fit every sample
array([2.11641395, 0.57564429, 2.34127743])
Benchmk:[0.945, 1.2800000000000002, 2.3449999999999998]
'''
tree_reg3 = DecisionTreeRegressor(min_samples_leaf=10)
tree_reg3.fit(X,y)
tree_reg3.predict([[.3],[.4],[.5]])
'''
Set min samples every leaf to reduce overfit
array([1.02829425, 1.23962784, 1.23962784])
Benchmk:[0.945, 1.2800000000000002, 2.3449999999999998]
With 3 tree_reg, it could also be found that for predict x value away from training sample,
    the predicted y could be extremely wrong. Try tree_reg.predict([[3],[4],[7]])
    Besides, model is over sensitive to samples. Even the same samples could lead to different models.
'''
