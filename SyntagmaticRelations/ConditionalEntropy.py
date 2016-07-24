import sys
sys.path.insert(0, '/../')
from AppearanceProbability import *
from includes import *

#H( p(X1==1), p(X2==1) )
# Where X1 and X2 are two words.
def H_cond(p1, p2):
    p10 = 1 - p1
    p20 = 1 - p2

    si0 = -
    ( (p2 *()) + (p20*()))