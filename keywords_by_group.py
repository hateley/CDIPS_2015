import random_forest as rf
import pandas as pd

def keyword_by_group(Data,group_var,text_var,nfeature,noun,write):
    group = list(set(Data[group_var]))
    result_list = []
    for i in range(len(group)):
        print group_var,group[i]
        result = rf.text_feature(Data.loc[Data[group_var]==group[i],],text_var,
                             nfeature,noun,silence=True)
        wordsorts = zip(result['word'], result['counts'])
        wordsorts = sorted(wordsorts, key=lambda wordsorts: wordsorts[1], reverse=True)
        for word, count in wordsorts:
            print count, word
        wordsorts = pd.DataFrame(wordsorts)
        wordsorts.columns = ['word','counts']
        wordsorts['group'] = group[i]
        result_list.append(wordsorts)
    output = pd.concat(result_list)
    if write:
        if noun:
            note = 'noun'
        else:
            note = 'all'
        filename = "../"+text_var+"_"+group_var+"_"+note+".csv"
        output.to_csv(filename)
    return output

if __name__=="__main__":
    import pandas as pd
    import age_grouping as ag
    import warnings
    warnings.filterwarnings("ignore")
    
    # Get data ready
    EPData = pd.read_csv("../First100000.csv")
    age_range = [13,78]
    bin_size = 11
    Data = ag.age_filtering(EPData,age_range)
    Data = ag.age_grouping(Data,bin_size,age_range)
    group = list(set(Data['age_group']))
    
    nfeature = 20
    # Extract word features for all words in statuses by age groups
    result1 = keyword_by_group(Data,'age_group','content',nfeature,False,True)
    # Extract word features for nouns only in group names by gender groups
    result2 = keyword_by_group(Data,'gender','gn',nfeature,True,True)