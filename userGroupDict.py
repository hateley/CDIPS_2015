import sys
# Without following 2 lines, I cannot do something like EPData[EPData['uid']==0] 
# with a dataframe EPData
# See http://stackoverflow.com/questions/28983608/how-to-create-a-pandas-dataframe-containing-columns-with-special-characters  for further explanation
reload(sys)
sys.setdefaultencoding('utf-8') 
import numpy as np

def makeUserGroupDict(data, uidCol, gidCol):
    print "starting function"
    sys.stdout.flush()
    data = data.sort(columns='uid')
    print "Finished sorting!"
    sys.stdout.flush()
    userDict = {}
    dictUID = data.iloc[0,uidCol]
    userDict[dictUID] = {}
    print "Starting to fill dict"
    sys.stdout.flush()
    groupList = []
    for irow in range(0,data.shape[0]):
        if irow%100 == 0:
            print "Row number is ", irow, " of ", data.shape[0]
            sys.stdout.flush()
        currentUID = data.iloc[irow,uidCol]
        if dictUID != currentUID:
            dictUID = currentUID
            userDict[dictUID] = {}
        gid = data.iloc[irow,gidCol]
        groupList.append(gid)
        if gid in userDict[dictUID]:
            userDict[dictUID][gid] += 1
        else:
            userDict[dictUID][gid] = 1
            
    print "Total number of unique groups is ", len(set(groupList))
            
    return userDict

def makeUserGroupMatrix(userGroupDict, groupList):
    # First make a dictionary to relate group ids to the index in the groupList
    groupIndexDict = {}
    for i in range(0,len(groupList)):
        groupIndexDict[groupList[i]] = i   
    
    nGroups = len(groupList)
    userList = userGroupDict.keys()
    nUsers = len(userList)
    userGroupMatrix = np.zeros((nUsers,nGroups),dtype=np.int)
    for i in range(0,nUsers):
        ukey = userList[i]
        for gkey in userGroupDict[ukey]:
            nPosts = userGroupDict[ukey][gkey]
            userGroupMatrix.itemset((i,groupIndexDict[gkey]),nPosts)
            
    return (userGroupMatrix, userList)
        
    
if __name__ == "__main__":
    import pandas as pd
    dataFileWithUserIDs = "/Users/dharshid/CDIPS_Project/data/First100000_with_id.csv"
    dataWithUserIDs = pd.read_csv(dataFileWithUserIDs)
    goodData = dataWithUserIDs[~(dataWithUserIDs['uid']==0)]
    goodData = goodData[goodData['certainty']==True]
    gidCol = 14 # column number for gid column
    uidCol = 20 # column number for uid column
    goodDataSorted = goodData.sort(columns = 'uid')
    goodDataSubset = goodDataSorted.iloc[0:100,:]
    userDict = makeUserGroupDict(goodDataSubset, 20, 14)
    
    # check that userDict contains the same number of data points as goodDataSubset
    totalEntries = 0
    for ukey in userDict.keys():
        for gkey in userDict[ukey].keys():
            totalEntries += userDict[ukey][gkey] 
    print "Total number of posts is ", totalEntries, " and it should be ", len(goodDataSubset)
    
    totalGroups = 0
    for key in userDict.keys():
        totalGroups += len(userDict[key])
    print "Total number of non-unique groups (i.e. counting groups each time a unique user posts in it) is ", totalGroups
    
    print "Number of users is ", len(userDict)
    
    print "Average number of groups per users ", totalGroups/float(len(userDict))
    
    
