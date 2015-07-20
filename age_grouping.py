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
    
    for bin_size in bin_seq:
        age_group = (np.array(Data['age'])-age_range[0])/bin_size
        # if bin_size is 5, age groups will be 13 - 17, 18 -22, 23-27,...; 
        # if bin_size is 10, age groups will be 13 - 22, 23- 32, 33 - 42,...
        Data['age_group'] = age_group
        # Calculate F statistic using ordinary least square method
        lF = 0
        ## Add up the log transformed (more readable) F statistic for all target variables
        for target in var_target:
            formula = target + '~ C(age_group)'
            lm = ols(formula, data=Data).fit()
            lF = lF + np.log(lm.fvalue)
        
        support.append(lF)
        print "bin size = ", bin_size, "log(F) = ",lF
        
    return bin_seq,support

if __name__ == '__main__':
    # Read in data from the directory where you keep it
    EPData = pd.read_csv("../EP_with_age.csv")
    # I have written age as a column into the file 
    # so I am reading it directly from the data.
    # If you haven't done so you need to calculate it first (refer to age.py).
    age = EPData['age']
    
    # var_target specifies a list of variables we want to maximize the F statistics for. 
    var_target = ['num_friends','num_groups']
    # You can use all available numeric variables but it's slow:
    # var_target = ['num_friends','num_fans','num_groups','num_logins','votes','num_comments']
    
    # The maximal bin size in years
    bin_max = 20
    # The range of reasonable age to be taken into calculation
    age_range = [13,80]
    grouping_result = age_grouping(age,EPData,var_target,bin_max,age_range)    

    # Plot log(F) against the bin size
    plt.plot(grouping_result[0],grouping_result[1])
    plt.xlabel('bin size')
    plt.ylabel('log(F)')
    plt.show()
    
    # Sort the bin size by their F score
    # sorted_result = zip(grouping_result[0],grouping_result[1])
	#for bin_size, F in sorted(sorted_result, key=lambda sorted_result:sorted_result[1],reverse=True):
    	#print bin_size, F