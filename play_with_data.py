import csv
import sys
import numpy as np

datafile = 'EP_data.csv'
csv.field_size_limit(sys.maxsize)

def csv_iterator(datafile):
    """Reads 1 row at a time from a csv file, yielding a dict with keys from the header row.
       Adds an 'id' field if there's not one."""
    rownum = 1
    for doc in csv.DictReader(open(datafile, 'rU')):
        id = doc.get('id', str(rownum))
        doc['id'] = id
        rownum += 1
        yield doc


if __name__ == "__main__":
    post_length_M = []
    post_length_F = []
    for doc in csv_iterator(datafile):
        if doc['gender'] == 'F':
            post_length_F.append(len(doc['content']))
        elif doc['gender'] == 'M':
            post_length_M.append(len(doc['content']))
        if int(doc['id']) % 10000 == 0:
            print doc['id']
        # print doc, '\n'
    print "median length of male post", np.median(np.array(post_length_M))
    print "median length of female post", np.median(np.array(post_length_F))
