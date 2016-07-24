import sys
sys.path.insert(0, '/../')
from WordFrequency import *
from includes import *

#AppearanceProbability
def AP( wordFreqMatrix ):
    totalWords = np.sum(wordFreqMatrix[:, 0])

    totalVector = np.zeros(shape=(wordFreqMatrix.shape[0],))
    totalVector.fill(totalWords)

    # Remove this word count from the total.
    totalVector -= wordFreqMatrix[:,0]

    wordFreqMatrix[:,1] = wordFreqMatrix[:,0] / totalVector

    return wordFreqMatrix

def test1():
    wf = wordFrequencies("../TextCorpus/Fiction/LeoTolstoy_WarAndPeace.txt", 5)
    print( AP( wf[1] ).shape)

