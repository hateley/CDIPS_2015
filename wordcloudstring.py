def wordCloudString(wordsData, nFeatures, groupNum):
    wordCloudStr = ""
    startIndex = 20*groupNum  
    for i in range(0,nFeatures):
        word=wordsData.loc[startIndex+i,'word']
        for j in range(0,int(wordsData.loc[startIndex+i,'counts'])):
            wordCloudStr += word
            wordCloudStr += " "
    return wordCloudStr
            
if __name__=="__main__":
    import pandas as pd
    ageGroupFeatures = pd.read_csv("/Users/dharshid/CDIPS_Project/data/gn_age_group_all.csv")
    nFeatures = 20
    wordCloudList = []
    for i in range(0,6):
        wordCloudList.append(wordCloudString(ageGroupFeatures, nFeatures, i))
        print wordCloudList[i]