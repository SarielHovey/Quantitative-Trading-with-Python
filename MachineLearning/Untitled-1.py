from sklearn.datasets import fetch_openml
# Fetch MINST from web
mnist = fetch_openml('mnist_784', version=1)
from sklearn.externals import joblib
joblib.dump(mnist, 'MNIST.pkl')

