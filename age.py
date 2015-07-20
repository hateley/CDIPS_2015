
# The following line is from converting this from an iPython Notebook
# coding: utf-8

from dateutil.parser import parse
from datetime import datetime, date

    
def calculate_age(birthdateStr):
    """ Calculates the age from a string containing the birthdate.
    birthdateStr must have the format "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"
    
    Error checking:
    This code also checks that birthdateStr can be parsed using dateutil's parse.
    If birthdateStr is not a true string and can't be parsed (parse gives an AttributeError), 
    this code catches that error, prints an error message, and returns a 0.  
    It doesn't catch other types of errors.
    """
    
    # Some of the birthdates from EP_data.csv couldn't be parsed
    # This try, except catches those birthdates to prevent the program
    # from crashing.  
    try:
        # parse takes a date in the format "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"
        # and parses it into a Python datetime object, which is very useful for
        # working with dates
        birthdate = parse(birthdateStr).date()
    except AttributeError:
        print "Could not parse birthdateStr ", birthdateStr
        return 0
    today = date.today()
    hasBirthdayNotPassed = ((today.month, today.day) < (birthdate.month, birthdate.day))
    # Use fact that FALSE converts to 0 and TRUE converts to 1 to subtract 1 if birthday
    # has NOT passed.
    return today.year - birthdate.year - int(hasBirthdayNotPassed)


import numpy as np
import matplotlib.pyplot as plt

def drawHistogram(dataArray):
    """
        This function takes in a numpy array and draws the histogram for that array.
        It prints out the total number of data points to check that histogram has binned
        every possible data point.
        
        To use in iPython Notebook, make sure the following line is included, so matplotlib
        plots inside the notebook:
        
        %matplotlib inline
        
    """
    hist, bins = np.histogram(dataArray)
    print "Total number of data points = ", sum(hist)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()


if __name__ == "__main__":
    
    # keep track of the number of missing values, i.e. empty birthdate strings
    nMissing = 0

    # Some users have put in a false birthdate, so we have to filter out
    # the "legitimate" ages.
    # The minimum age for using ExperienceProject is 13, so it is legitAgeMin
    # The maximum age is more arbitrary.  100 seems reasonable.
    legitAgeMin = 13 
    legitAgeMax = 100

    # contains all data, including missing or corrupt values (which are assigned an age of 0)
    # and ages outside the range [legitAgeMin, legitAgeMax].
    allAgeList = [] 
    
    # only contains ages within [legitAgeMin, legitAgeMax]
    legitAgeList = [] 

    # CHANGE THIS TO YOUR LOCATION OF THE DATA FILE
    dataFilePath = "../EP_data.csv"
    import pandas as pd
    EPData = pd.read_csv(dataFilePath)
    
    for irow in range(0,EPData.shape[0]):
        if EPData.loc[irow,'birthdate']=="":
            age = 0
            nMissing += 1
            allAgeList.append(age)
        else:
            age = calculate_age(EPData.loc[irow,'birthdate'])
            if age > legitAgeMax or age < legitAgeMin:
                allAgeList.append(age)
            else:
                allAgeList.append(age)
                legitAgeList.append(age)

        # print info every several iterations to make sure code is running
        if irow % 10000 == 0:
            print "birthdate for row ", irow, " is ", EPData.loc[irow,'birthdate']
            print "age for row ", irow, " is ", age

    print "Number of missing values is ", nMissing

    # If you run this code in iPython Notebook, uncomment next line or matplotlib won't plot within iPython Notebook
    # %matplotlib inline
    drawHistogram(np.array(legitAgeList))
    EPData['age'] = allAgeList
    EPData.to_csv("../EP_with_age.csv")




