import pandas as pd
import numpy as np
from scipy import stats

def non_para(data,var,cat,method='Wilcoxon'):
    """Do non-parametric test comparing values for a given variable (specified by argument 'var') between data grouped by a given category (specified by argument 'cat'); data can be a pandas DataFrame or a dictionary.
    There are two method options: Wilcoxon and Kruskal.
    Two matrices are returned, the first one containing p-value of the test (and therefore is symmetric), the second containing difference between median of the two categories (row minus column)."""
    cats = list(set(data[cat]))
    p_value = np.zeros((len(cats),len(cats)))
    diff = np.zeros((len(cats),len(cats)))
    for i1 in range(len(cats)):
        for i2 in range(len(cats)):
            if method=='Wilcoxon':
                p_value[i1,i2] = round(stats.ranksums(data[var][data[cat]==cats[i1]],data[var][data[cat]==cats[i2]])[1],3)
            elif method=='Kruskal':
                p_value[i1,i2] = round(stats.kruskal(data[var][data[cat]==cats[i1]],data[var][data[cat]==cats[i2]])[1],3)
            else:
                print 'No such method'
                return 
            diff[i1,i2] = data[var][data[cat]==cats[i1]].median()-data[var][data[cat]==cats[i2]].median()
    p_value = pd.DataFrame(p_value,index=cats,columns=cats)
    diff = pd.DataFrame(diff,index=cats,columns=cats)
    result = {'p':p_value,'med_diff':diff}
    return result

if __name__=='__main__':
    EP = pd.read_csv("EP_data.csv").dropna()
    variable = 'num_friends'
    category = 'gender'
    method='Wilcoxon'
    Result = non_para(EP,variable,category,method)
    print 'p-value matrix \n', Result['p']
    print 'median difference matrix \n', Result['med_diff']