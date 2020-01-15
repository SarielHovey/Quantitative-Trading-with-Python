# Principal Component Analysis (PCA)
'''
Find the axis that accounts for the largest variance in the training set to reduce dimention
i-th axis is the i-th Principal Component(PC) of the data
Singular Value Decomposition(SVD) could be used for this purpose
    $X = U \Sigma V^T$
    $V = (c_1,c_2,...,c_n)$ contains unit vectors that define all PCs
'''
import numpy as np
X = np.random.randn(100)
X = X.reshape((10,10))
X = np.matrix(X)
X = X * 5 + 20
X_centered = X - X.mean(axis=0) # PCA works on centered data. Scikit-Learn will do this automatically
U, s, Vt = np.linalg.svd(X_centered)
c1, c2 = Vt.T[:,0], Vt.T[:,1]
'''
matrix([[ 0.23914461,  0.42634911],
        [-0.13740109,  0.27116828],
        [ 0.08670662,  0.11882321],
        [ 0.34953329, -0.02270431],
        [ 0.56395714, -0.225988  ],
        [ 0.40709142,  0.06633158],
        [ 0.09224857, -0.11305618],
        [ 0.19889756,  0.72568501],
        [ 0.5073696 , -0.23719314],
        [-0.07052806, -0.28094179]])
'''
## Projecting Down to d Dimensions
'''
$X_{d-projection} = XW_d$
    X is training set; $W_d$ is the matrix containing the first d columns of V
'''
W2 = Vt.T[:,:2]
X2D = X_centered.dot(W2)
## Scikit-Learn's example
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X2D = pca.fit_transform(X)
pca.components_.T
'''
Same as above manual result, since they are technically the same
array([[-0.23914461,  0.42634911],
       [ 0.13740109,  0.27116828],
       [-0.08670662,  0.11882321],
       [-0.34953329, -0.02270431],
       [-0.56395714, -0.225988  ],
       [-0.40709142,  0.06633158],
       [-0.09224857, -0.11305618],
       [-0.19889756,  0.72568501],
       [-0.5073696 , -0.23719314],
       [ 0.07052806, -0.28094179]])
'''
## Explained Variance Ration
pca.explained_variance_ratio_
'''
1st PC takes 32.35% of data's variance
2nd PC takes 25.30% of data's variance
array([0.3235398 , 0.25302504])
'''

## Find the Appropriate Number of Dimensions
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
mnist = joblib.load('MNIST.pkl')
X = mnist['data']; y = mnist['target']
X_train, X_test, y_train, y_test = train_test_split(X, y)
pca1 = PCA()
pca1.fit(X_train)
cumsum = np.cumsum(pca1.explained_variance_ratio_)
d = np.argmax(cumsum >= .95) + 1 # Find the number of dimensions that consists of 95% of data variance
### Or technically equivalent
pca2 = PCA(n_components=.95)
X_reduced = pca2.fit_transform(X_train)
### Plot cumsum to get relationship between Explained Variance and Demensions
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
plt.plot(cumsum)
plt.xlabel('Number of Dimensions'); plt.ylabel('Explained Variance')
plt.axis([-0.1, 800, 0, 1.12])
plt.plot([d, d], [0, 0.95], "k:")
plt.plot([0, d], [0.95, 0.95], "k:")
plt.plot(d, 0.95, "ko")
X.shape
'''
X has 784 features
With d = 154, the Explained Variance already reaches 0.95 level
Increase d to 700 only makes an increase of 0.05
Obviously, reduce X's dimension to 154 will keep most features of original data
'''
### PCA for Compression
'''
Recover the originate dimensions (inevitable decrease in quality)
$X_{recovered} = X_{d-projection}W_d^T $
'''
pca = PCA(n_components=154)
X_reduced = pca.fit_transform(X_train)
X_recovered = pca.inverse_transform(X_reduced)
### Randomized PCA
'''
Quickly approximate the first d PCs, rather than compute the whole SVD
If fully compute required:
    PCA(n_components=154, svd_solver='full')
'''
rnd_pca = PCA(n_components=154, svd_solver='randomized')
X_reduced = rnd_pca.fit_transform(X_train)



# Invremental PCA
'''
Instead of loading whole training set into memory, incremental PCA could read partial data everytime
'''
from sklearn.decomposition import IncrementalPCA
n_batches = 100
inc_pca = IncrementalPCA(n_components=154)
for X_batch in np.array_split(X_train,n_batches):
    inc_pca.partial_fit(X_batch)
X_reduced = inc_pca.transform(X_train)
'''
X.shape: (52500, 154)
Or technically equivalently use np.memmap
'''
m, n = 52500, 784
X_mm = np.memmap('data', dtype='float32',mode='readonly',shape=(m,n))
batch_size = m // n_batches
inc_pca = IncrementalPCA(n_components=154, batch_size=batch_size)
inc_pca.fit(X_mm)




# Kernel PCA
from sklearn.decomposition import KernelPCA
rbf_pca = KernelPCA(n_components=2, kernel='rbf', gamma=0.04)
rbf2_pca = KernelPCA(n_components=2, kernel='sigmoid', gamma=0.001)
from sklearn.datasets import make_swiss_roll
DATA = make_swiss_roll(n_samples=5000, noise=0.15)
X = DATA[0]; y = DATA[1]
X_reduced = rbf_pca.fit_transform(X)
'''
Use RBF Kernel to reduce the 3 dimensions of a Swiss Roll to 2 dimensions
Please be noticed this is unsupervised learning, and this is in data processing stage
X shape: (5000,3)
X_reduced shape: (5000,2)
'''
## (1) Use Grid Search to find best kernel and parameter
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
clf = Pipeline([
    ('kpca',KernelPCA(n_components=2)),
    ('log_reg',LogisticRegression()),
])
param_grid = [{
    'kpca_gamma':np.linspace(0.03,0.05,10),
    'kpca_kernel':['rbf','sigmoid']
}]
grid_search = GridSearchCV(clf, param_grid, cv=3)
grid_search.fit(X,y)
grid_search.best_params_
'''

'''