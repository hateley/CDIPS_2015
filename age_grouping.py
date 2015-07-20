import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
#%matplotlib inline

def age_grouping(age,data,var_target,bin_max,age_range):
    """ Choose the bin size for age grouping by maximizing the 
    F statistic, i.e. the ratio between cross-group variation 
    and within-group variation, of the target variable (var_target).
    
    bin_max specifies the maximal bin size to be considered.
    
    age_max specifies the maximal age to be considered."""
    
    # Select data with age under the maximal age
    
    Data = data
    Data['age'] = age
    Data = Data.loc[Data['age'] < age_range[1],]
    Data = Data.loc[Data['age'] > age_range[0],]
    
    # Create a sequence of bin size for trial
    bin_seq = range(1,bin_max)
    # Create a list to contain the F statistics for the given sequence of bin size
    support = [] 
    
    for bin in bin_seq:
        age_group = (np.array(Data['age'])-age_range[0])/bin
        # if bin is 5, age groups will be 13 - 17, 18 -22, 23-27,...; 
        # if bin is 10, age groups will be 13 - 22, 23- 32, 33 - 42,...
        Data['age_group'] = age_group
        print set(age_group)
        # Calculate F statistic using ordinary least square method
        formula = var_target + '~ C(age_group)'
        lm = ols(formula, data=Data).fit()
        support.append(lm.fvalue)
        print "bin size = ", bin, "F = ",lm.fvalue
        
    # Order the bin size by their F statistic (from the highest to the lowest)
    result = zip(bin_seq,support)
    return result

if __name__ == '__main__':
    # Read in data from the directory where you keep it
    EPData = pd.read_csv("../EP_with_age.csv")
    # I have written age as a column into the file 
    # so I am reading it directly from the data.
    # If you haven't done so you need to calculate it first (refer to age.py).
    age = EPData['age']
    var_target = 'num_friends'
    bin_max = 20
    age_max = 80
    grouping_result = age_grouping(age,EPData,var_target,bin_max,age_max)
    for bin, F in sorted(group_result, key=lambda group_result:group_result[1],reverse=True):
    print bin, F
    plt.plot(grouping_result['bin'],grouping_result['F'])
    plt.show()