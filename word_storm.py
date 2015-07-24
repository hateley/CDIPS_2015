
# coding: utf-8

# In[214]:

#!/usr/bin/env python

"""
Create a word storm for the 50 most-posted-in groups.
Takes the EP_data.csv file.
"""

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords

datafile = pd.read_csv('EP_data.csv')

#get a list of the 50 groups with the most posts
group_count = pd.Series(datafile["gid"])
top50 = group_count.value_counts()[0:50]

#select only the useful data that we need: id and status content
data = datafile[['gid','content']]
#data = data.head(n=10000) #remove this line when doing whole dataset


# In[281]:

#make a dictionary of the top 50 groups, to which I can add all status words as lists
groups = dict(top50)
group_words = dict.fromkeys(groups)
for key in group_words:
    group_words[key] = []
#print group_words


# In[282]:

#create function to clean our statuses
def status_to_words( raw_status ):
    # Function to convert a raw status to a string of words
    # The input is a single string (a raw status update), and 
    # the output is a single string (a preprocessed status update)
    #
    # 1. Remove HTML
    status_text = BeautifulSoup(raw_status).get_text() 
    #
    # 2. Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", status_text)
    # remove http URLs
    letters_only = re.sub(r'^https?:\/\/.*[\r\n]*', '', letters_only)
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()                             
    #
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))
    #Remove 'm' and 'hasn' from the text
    stops = stops.union([u'hasn',u'm',u've',u'll',u're',u'didn',u'us',u'im',u'doesn',u'couldn',u'won',u'isn',u'http',u'www']) 
    # 
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]   
    #
    # 6. Join the words back into one string separated by space, 
    # and return the result.
    return( " ".join( meaningful_words ))

#Let's see an example of what status_to_words does
#clean_status = status_to_words( data['content'][1] )
#print (clean_status)


# In[223]:

#Now run status_to_words on all the statuses (or a subset) for preprocessing
print "Cleaning and parsing the status updates...\n"
i = 0
for index,row in data.iterrows():
        try:
            if( (i+1)%1000 == 0 ):
                print "Status %d of %d\n" % ( i+1, data.shape[0] )   
            key = row['gid']
            if key in group_words.keys():
                clean_status = status_to_words(row['content'])
                group_words[key].append(clean_status)
            i += 1
        except TypeError as detail:
                msg = "here's that error"
                continue
            
#join the seperate statuses into one for each group
for key in group_words:
    group_words[key] = " ".join(group_words[key])


# In[250]:

#These lines are for testing whether Bag o' words works.
#It uses a smaller dictionary to test.
#smalldict = {k: group_words[k] for k in (1728, 950)}
#print smalldict.keys()


# In[252]:

#for group in smalldict:
#    print group


# In[280]:

# create the Bag o' words. Each word that appears in the statuses after preprocessing gets a place
# in the bag (list). Each status gets a list denoting the number of times a particular word
# shows up in that status.  Check out 
# https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-1-for-beginners-bag-of-words

print "Creating the bags of words...\n"
from sklearn.feature_extraction.text import CountVectorizer

n = 0
with open('top50.csv', 'w') as out:
    out.write('These are the top 50 most-posted-in groups from Experience Project:\nFormat is >gid, followed by lines for each word sorted by frequency.\n\n\n')
    for group in group_words:
        n += 1
        out.write('>'+str(group)+'\n')
        print 'working on group %s' % group
        words = [group_words[group]]
        # Initialize the "CountVectorizer" object, which is scikit-learn's
        # bag of words tool. Note that some of the preprocessing steps above
        # can be done directly with this tool; we may want to do that.
        vectorizer = CountVectorizer(analyzer = "word",                                        tokenizer = None,                                         preprocessor = None,                                      stop_words = None,                                        max_features = 500) 

        # fit_transform() does two functions: First, it fits the model
        # and learns the vocabulary; second, it transforms our training data
        # into feature vectors. The input to fit_transform should be a list of 
        # strings.
        train_data_features = vectorizer.fit_transform(words)

        # Numpy arrays are easy to work with, so convert the result to an 
        # array
        train_data_features = train_data_features.toarray()

        vocab = vectorizer.get_feature_names()
        dist = np.sum(train_data_features, axis = 0)
        counted = zip(vocab, dist)
        for tag, count in sorted(counted, key=lambda counted: counted[1], reverse=True):
            out.write(tag+','+str(count)+'\n')
        print n
