if __name__ == "__main__":

    import sys
    # Without following 2 lines, I cannot do something like EPData[EPData['uid']==0] 
    # with a dataframe EPData
    # See http://stackoverflow.com/questions/28983608/how-to-create-a-pandas-dataframe-containing-columns-with-special-characters  for further explanation
    reload(sys)
    sys.setdefaultencoding('utf-8') 
    import pandas as pd
    import numpy as np
    dataWithUserIDs = pd.read_csv("/Users/dharshid/CDIPS_Project/data/First100000_with_id.csv")
    goodData = dataWithUserIDs[~(dataWithUserIDs['uid']==0)]
    goodData = goodData[goodData['certainty']==True]
    top50GroupFile = "/Users/dharshid/CDIPS_Project/data/top50groups.txt"
    top50Groups = np.loadtxt(top50GroupFile,comments="#",delimiter="\n",unpack=False)
    top50Groups = top50Groups.astype(int)
    top50GroupData = goodData[goodData['gid']==top50Groups[0]]
    for i in range(1,50):
        top50GroupData = top50GroupData.append(goodData[goodData['gid']==top50Groups[i]],ignore_index=True)
        
    import userGroupMatrix
    top50GroupSorted = top50GroupData.sort(columns='uid')
    topGroupSubset = top50GroupSorted.iloc[:,:]
    #topGroupSubset = top50GroupData.iloc[0:10000,:]
    uidColNum = 20
    gidColNum = 14
    nUsers = len(topGroupSubset['uid'].unique())
    
    (userGroupMat, userList) = userGroupMatrix.makeUserGroupMatrix(topGroupSubset, nUsers, top50Groups, uidColNum, gidColNum)
    
    np.savetxt("testMatrix.txt", userGroupMat, fmt="%d")
    
    print "Number of users is ", nUsers