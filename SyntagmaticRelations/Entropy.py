import sys
sys.path.insert(0, '/../')
from AppearanceProbability import *
from includes import *
import matplotlib.ticker as ticker

# Entropy H(X==1)
def H( p1 ):
    # Given the probability of a random distribution variable(p1) that represents
    # it's probabilty of it appearing.
    p0 = 1 - p1
    logP0 = np.log2(p0)
    logP1 = np.log2(p1)

    if(p0 == 0):
        logP0 = 0
    if(p1 == 0):
        logP1 = 0

    return  abs( (-p0*logP0)+(-p1*logP1) )

# Assumes the structure [word freq, p(W == 1), entropy ]
def H_matrix( matrix ):
    outMatrix = np.zeros(shape=matrix.shape)

    r = 0
    for row in matrix:
        outMatrix[r,:] = H(row[1])
        r += 1

    return outMatrix

def test1():
    [labels,wf] = wordFrequencies("../TextCorpus/Fiction/LeoTolstoy_WarAndPeace.txt", 5)
    freqMatrix = AP( wf )
    lastRowP1 = freqMatrix[freqMatrix.shape[0]-1,1]

    print( H(lastRowP1) )

    tst = H_matrix(freqMatrix)

    print(tst)

    inp = None

    print("Word Entropy Lookup. Type '/' to end. ")
    while inp != "/":
        inp = raw_input("Enter word: ")

        for idx, label in enumerate(labels):
            if inp == label:
                print("Entropy of %s: %f" % (label,tst[idx,2]))
                break




def test2():
    [labels, wf] = wordFrequencies("../TextCorpus/Fiction/LeoTolstoy_WarAndPeace.txt", 5)
    entropyMatrix = H_matrix( AP(wf) )

    testStr1 = "The dog walked the cat and that was very good"
    ta1 = [x.lower() for x in testStr1.split()]

    print(ta1)

    testStr1Entropy = []

    for word in ta1:
        for idx,label in enumerate( labels ):
            if word == label:
                testStr1Entropy.append( entropyMatrix[idx,2] )
                break

    print(testStr1Entropy)

    for word,ent in zip( ta1,testStr1Entropy ):
        print("%s: %f" % (word,ent) )

#test2()

def test3():
    # Plot verifiation of H.
    dat = []
    for i in np.arange(0,1,0.001):
        dat.append( H(i) )

    print(dat)

    plt.title('Entropy V.S. Probability of Word Appearing')
    plt.xlabel('P(W=ddd=1)')
    plt.ylabel('Entropy')
    plt.plot(np.arange(0,1,0.001), dat)

    plt.xticks(np.arange(0,1.1,0.1), rotation='vertical')

    # Tweak spacing to prevent clipping of tick-labels

    plt.grid(True)
    plt.show()



#test2()
test1()