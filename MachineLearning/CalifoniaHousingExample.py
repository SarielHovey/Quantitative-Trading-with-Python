import pandas as pd; import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
housing = pd.read_csv('housing.csv')



housing.describe()
housing.hist(bins=50)
# In Linux without GUI, save the pic to current path
plt.savefig('temp.png')




# Pure Random Sampling
def test_set_check(identifier, test_ratio):
    '''
    Count Hash Value for elements in data to make sure same test set used
    '''
    from zlib import crc32
    return crc32(np.int64(identifier)) & 0xffffffff < test_ratio * 2**32

def split_train_test(data, test_ratio, id_column):
    '''
    Used to divid between Test and Train Set
    Parameter: data -- the Pandas DataFrame containing the data
        test_ratio -- double, the percentage of total data to use for Test Set
        id_column -- string, unique and immutable label in data, the Primary Key
    Return: 2 DataFrames, 1st is Train Set; 2nd is Test Set
    -------------------------------------------------------
    '''
    ids = data[id_column]
    in_test_set = ids.apply(lambda id_: test_set_check(id_, test_ratio))
    return data.loc[~in_test_set], data.loc[in_test_set]

# Use House's Longitude and Latitude as Primary Key
housing['houseID'] = housing.longitude * 1000 + housing.latitude

trainSet, testSet = split_train_test(housing, 0.2, 'houseID')
len(trainSet),len(testSet),len(housing)
'''
(16322, 4318, 20640)
'''



# Stratified Sampling
housing['incomeCategory'] = pd.cut(housing.median_income, bins=[0.,1.5,3.0,4.5,6.,np.Inf], labels=[1,2,3,4,5])
plt.cla()
housing.incomeCategory.hist()
plt.savefig('temp.png')
housing.incomeCategory.value_counts()
'''
3    7236
2    6581
4    3639
5    2362
1     822
Name: incomeCategory, dtype: int64
'''
## Use sklearn's function
from sklearn.model_selection import StratifiedShuffleSplit
split = StratifiedShuffleSplit(1,0.2,random_state=43)
for trainIndex, testIndex in split.split(housing, housing.incomeCategory):
    trainSet = housing.loc[trainIndex]
    testSet = housing.loc[testIndex]

len(trainSet), len(testSet), len(housing)
'''
(16512, 4128, 20640)
'''

trn = trainSet.copy()
plt.cla()
trn.plot(kind='scatter', x='longitude',y='latitude',alpha=0.4,s=trn.population/100,label='population',figsize=(10,7),c='median_house_value',cmap=plt.get_cmap('jet'),colorbar=True)

corrMatrix = trn.corr()
corrMatrix.median_house_value.sort_values(ascending=False)
'''
latitude             -0.148121
houseID              -0.040516
longitude            -0.040318
population           -0.024069
total_bedrooms        0.050002
households            0.066341
housing_median_age    0.107099
total_rooms           0.135290
median_income         0.690551
median_house_value    1.000000
Name: median_house_value, dtype: float64
'''

from pandas.plotting import scatter_matrix
attributes = ['median_house_value','median_income','total_rooms','housing_median_age']
plt.cla()
scatter_matrix(trn[attributes], figsize=(12,8))
plt.savefig('temp.png')
# Obvious Trend found between median_house_value and median_income
plt.cla()
plt.plot(kind='scatter',y='median_house_value',x='median_income',alpha=0.1)



# Deal with NaN values in data
median = housing['total_bedrooms'].median()
housing.total_bedrooms.fillna(median, inplace=True)


# median_house_value is the target we would like to predict based on other data
housing = trainSet.drop('median_house_value',axis=1)
housing_labels = trainSet.median_house_value.copy()


# Transform string values into categorical attribute
housing.ocean_proximity.value_counts()
'''
<1H OCEAN     7310
INLAND        5234
NEAR OCEAN    2142
NEAR BAY      1822
ISLAND           4
Name: ocean_proximity, dtype: int64
'''
housing_cat = housing[['ocean_proximity']]
from sklearn.preprocessing import OrdinalEncoder
ordinal_encoder = OrdinalEncoder()
housing_cat_encoded = ordinal_encoder.fit_transform(housing_cat)
print(housing_cat_encoded[:5])
'''
[[0.]
 [0.]
 [0.]
 [0.]
 [3.]]
'''
ordinal_encoder.categories_
'''
[array(['<1H OCEAN', 'INLAND', 'ISLAND', 'NEAR BAY', 'NEAR OCEAN'],  dtype=object)]
'''
## In case of Dummy Variables
from sklearn.preprocessing import OneHotEncoder
dummy_encoder = OneHotEncoder()
housing_cat_dummy = dummy_encoder.fit_transform(housing_cat)
housing_cat_dummy
'''
<16512x5 sparse matrix of type '<class 'numpy.float64'>'
        with 16512 stored elements in Compressed Sparse Row format>
'''
housing_cat_dummy.toarray()
'''
array([[1., 0., 0., 0., 0.],
       [1., 0., 0., 0., 0.],
       [1., 0., 0., 0., 0.],
       ...,
       [0., 0., 0., 1., 0.],
       [1., 0., 0., 0., 0.],
       [1., 0., 0., 0., 0.]])
'''
dummy_encoder.categories_
'''
[array(['<1H OCEAN', 'INLAND', 'ISLAND', 'NEAR BAY', 'NEAR OCEAN'],  dtype=object)]
'''
