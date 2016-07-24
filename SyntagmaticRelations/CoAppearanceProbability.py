import sys
sys.path.insert(0, '/../')
from WordFrequency import *
from includes import *
import json


# Returns text segments.d
def digestText(filePath,delim):
    return pd.read_csv(filePath, delimiter=delim, quoting=3, header=None)

def digestText_sentences(filePath):
    sents = None

    with open(filePath, 'r') as in_file:
        text = in_file.read()
        sents = np.array( text.split(".") )
        in_file.close()

    return sents

#CoAppearance Probability Matrix
#Each record of the text digest is assumed to be a segment.
def CAPM( textDigest ,dictionarySet, segmentSize ):
    ma         = textDigest
    nSegments  = textDigest.shape[0]

    #[word] = index in coOccurMatrix.
    wordIndex = dict()
    row = 0

    #Will be in the end: wordIndex X wordIndex
    #
    coOccurMatrix = np.zeros(shape=(len(dictionarySet),len(dictionarySet)))

    count = 0
    for word in dictionarySet:
        wordIndex[word] = count
        count += 1

    while row < nSegments+segmentSize:

        segmentRows = ma[row:row+segmentSize]

        # Segment will be a bag of words.
        segment = []
        cleanSegment = []

        # TODO: Remove clense from this function.
        # Do some data clensing and join all entries into one segment.
        for entry in segmentRows:
            # Data Cleanse
            segment += [x.lower() for x in entry.split()]


        for word in segment:
            # Clean word of punctuation.
            cleanSegment.append( word.translate(string.maketrans("", ""), string.punctuation) )


        segment = set( cleanSegment )
        segmentInner = segment.copy()

        for word1 in segment:
            if word1 in dictionarySet:
                for word2 in segmentInner:
                    if word2 in dictionarySet and word2 != word1:
                        coOccurMatrix[wordIndex[word1], wordIndex[word2]] += 1
                        coOccurMatrix[wordIndex[word2], wordIndex[word1]] += 1
                segmentInner.remove(word1)


        print(row,nSegments)
        row += segmentSize

    #Mirror over diagonal.
    segRange = range(len(dictionarySet))

    #
    #for word1 in dictionarySet:
    #    for word2Loc in segRange:
    #            coOccurMatrix[wordIndex[word1], wordIndex[segment[word2Loc]]] = 1
    #    segRange.pop(0)

    #for word in dictionarySet:
    #    wordIndex[word]

    return [wordIndex, coOccurMatrix]

def test1():
    name = "LeoTolstoy_WarAndPeace"
    filePath       = "../TextCorpus/Fiction/LeoTolstoy_WarAndPeace.txt"
    freqThreshold  = 10
    sentencesInSeg = 10

    dict = wordFrequencies(filePath, freqThreshold, True)
    [wordIndex, coMatrix] = CAPM( digestText_sentences(filePath ), dict, sentencesInSeg)


    coMatrix.tofile("MatrixData/"+name+"_"+str(freqThreshold)+"_"+str(sentencesInSeg)+".matrix.npy")
    json.dump(wordIndex, open("MatrixData/"+name+"_"+str(freqThreshold)+"_"+str(sentencesInSeg)+".dict.json", 'w'))

def test2():
    path = "../TextCorpus/Philosophy/Plato_Apology.txt"
    #path = "../TextCorpus/Misc/AR_BlogBlurb1.txt"
    #path = "../TextCorpus/Misc/OneSentence.txt"

    dict = wordFrequencies(path, 1 , returnOnlyDictionary=True)

    print("Dictionary size: ",len(dict) )

    [wordIndex, coMatrix ] = CAPM(digestText_sentences(path), dict, 10)

    print(dict)

    print(coMatrix)

    while( True ):
        word1 = raw_input("Word1: ")
        word2 = raw_input("Word2: ")

        try:
            print("Word1 index: ",wordIndex[word1],"Word2 index: ",wordIndex[word2])
            print( coMatrix[wordIndex[word1],wordIndex[word2]] )
        except:
            if not( word1 in dict ):
                print("%s not in dictionary."%word1)
            if not( word2 in dict ):
                print("%s not in dictionary."%word2)



    #coMatrix.tofile("MatrixData/Apology_50_20.np.matrix")

def matrixExplore():
    dict = json.load(open("MatrixData/LeoTolstoy_WarAndPeace_10_10.dict.json"))


    path = "MatrixData/LeoTolstoy_WarAndPeace_10_10.matrix.npy"
    mx = np.fromfile(path,dtype=float).reshape(len(dict),len(dict))

    #print("Size: ",mx.shape)

    inv_map = {v: k for k, v in dict.items()}

    while True:
        inWord = raw_input("Enter a word to explore it's associations: ")
        upperBound = raw_input("Upper freq bound: ")

        assoc = []
        col = 0
        try:
            for freq in mx[dict[inWord],:]:
                if(freq > 5) and (freq<=int(upperBound)):
                    assoc.append( (inv_map[col],freq) )

                col += 1

            print( sorted(assoc,key=( lambda(x): x[1] ),reverse=True) )
        except:
            print("%s not in text."%inWord)


#test1()
#test2()
matrixExplore()