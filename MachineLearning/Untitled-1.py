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
3    7236                                                                                                                          2    6581                                                                                                                          4    3639                                                                                                                          5    2362                                                                                                                          1     822                                                                                                                          Name: incomeCategory, dtype: int64
'''
## Use sklearn's function
from sklearn.model_selection import StratifiedShuffleSplit
