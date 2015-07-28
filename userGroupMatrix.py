import sys
# Without following 2 lines, I cannot do something like EPData[EPData['uid']==0] 
# with a dataframe EPData
# See http://stackoverflow.com/questions/28983608/how-to-create-a-pandas-dataframe-containing-columns-with-special-characters  for further explanation
reload(sys)
sys.setdefaultencoding('utf-8') 
import numpy as np

def makeUserGroupMatrix(data, nUsers, groupIDList, userIDCol, groupIDCol):
    # make a dictionary with group id as key and index of group in userGroupMatrix as value
    groupIDToIndex = {}
    index = 0
    for gid in groupIDList:
        groupIDToIndex[gid] = index
        index += 1
    
    data = data.sort(columns='uid')
    userGroupMatrix = np.zeros((nUsers, len(groupIDList)), dtype=np.int)
    uIndex = 0
    userID = data.iloc[0,userIDCol]
    userList = [userID]
    for i in range(0,len(data)):
        currentUserID = data.iloc[i,userIDCol]
        if userID != currentUserID:
            userID = currentUserID
            uIndex += 1
            userList.append(userID)
        groupID = data.iloc[i,groupIDCol]
        gIndex = groupIDToIndex[groupID]
        userGroupMatrix[uIndex, gIndex] += 1
    
    return (userGroupMatrix, userList)

if __name__ == "__main__":
    import pandas as pd
    dataWithUserIDs = pd.read_csv("/Users/dharshid/CDIPS_Project/data/First100000_with_id.csv")
    goodData = dataWithUserIDs[~(dataWithUserIDs['uid']==0)]
    goodData = goodData[goodData['certainty']==True]
    top50GroupFile = "/Users/dharshid/CDIPS_Project/data/top50groups.txt"
    top50Groups = np.loadtxt(top50GroupFile,comments="#",delimiter="\n",unpack=False)
    top50Groups = top50Groups.astype(int)
    
    top7Groups = top50Groups[0:7]
    top7GroupData = goodData[goodData['gid']==top7Groups[0]]
    for i in range(1,7):
        top7GroupData = top7GroupData.append(goodData[goodData['gid']==top7Groups[i]],ignore_index=True)  
        
    top7GroupSorted = top7GroupData.sort(columns='uid')
    topGroupSubset = top7GroupSorted.iloc[0:20,:]
    uidColNum = 20
    gidColNum = 14
    nUsers = len(topGroupSubset['uid'].unique())
    
    (userGroupMat, userList) = makeUserGroupMatrix(topGroupSubset, nUsers, top7Groups, uidColNum, gidColNum)
    
    print "The data is "
    print topGroupSubset[['gid','uid']]
    
    print "The number of users is "
    print nUsers
    
    print "The user-group matrix is "
    print userGroupMat
    
    print "The user list is "
    print userList
    
    print "The group list is "
    print top7Groups
    
    np.savetxt("testMatrix.txt", userGroupMat, fmt="%d")