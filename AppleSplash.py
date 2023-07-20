#!/usr/bin/env python

import numpy as np

nInst=50
currentPos = np.zeros(nInst) #we start with nothing
def getMyPosition (prcSoFar):
    global currentPos
    (nins,nt) = prcSoFar.shape #nins = no. of rows = days passed so far, nt = no. of columns = 50
    if (nt < 2):
        return np.zeros(nins)
    lastRet = np.log(prcSoFar[:,-1] / prcSoFar[:,-2])
    rpos = np.array([int(x) for x in 2000000 * lastRet / prcSoFar[:,-1]])
    currentPos = np.array([int(x) for x in currentPos+rpos])
    return np.ones(50)