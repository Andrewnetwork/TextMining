# WordFrequency.py
# Andrew Ribeiro
# July 23, 2016
#    _           _
#   /_\  _ _  __| |_ _ _____ __ __
#  / _ \| ' \/ _` | '_/ -_) V  V /
# /_/ \_\_||_\__,_|_| \___|\_/\_/
#
# Note:
# This software is provided to you on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied.
###################################
# Given a text file, produce a file in ascending order of words and frequencies.
# For every word, there's a line:
# word | frequency
#

import sys
sys.path.insert(0, '/../')
from includes import *

# Returns: [rowLabels , sortedCountMatrix]
def wordFrequencies(filePath, countThreshold, returnOnlyDictionary=False):
    text = pd.read_csv(filePath,delimiter="\n",quoting=3,header=None)

    ma         = text.as_matrix()[:,0]
    wfDict     = set()
    freq       = dict()
    threshDict = set()

    for line in ma:
        words = [ x.lower() for x in line.split() ]
        for word in words:
            word = word.translate(string.maketrans("",""), string.punctuation)
            if word in wfDict:
                freq[word] += 1
            else:
                freq[word] = 1
                wfDict.add(word)


    threshold = countThreshold

    # Leave blank column for future apperance probabity and entropy calculation.
    sortedCountMatrix = np.zeros(shape=(0,3))
    rowLabels = []

    for key, value in sorted(freq.iteritems(), key=lambda (k,v): (v,k)):
        if value >= threshold:
            rowLabels.append(key)
            threshDict.add(key)
            sortedCountMatrix = np.vstack( [sortedCountMatrix, [ float(value), 0, 0] ]  )

    if( returnOnlyDictionary ):
        return threshDict
    else:
        return [rowLabels , sortedCountMatrix]

def test1():
    labels,wf = wordFrequencies("../TextCorpus/Fiction/LeoTolstoy_WarAndPeace.txt",5)
    usefulWordCount = wf.shape
    print("Useful word count %s" % usefulWordCount[0])

