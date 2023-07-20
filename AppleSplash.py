#!/usr/bin/env python

import numpy as np

nInst=50    #number of stocks
currentPos = np.zeros(nInst)    #we start with nothing
def getMyPosition (prcSoFar):
    global currentPos
    (nins,nt) = prcSoFar.shape    #nins = no. of rows = days passed so far, nt = no. of columns = 50
    if (nt < 2):
        return np.zeros(nins)    #on day 1 you start with 0 stocks
    lastRet = np.log(prcSoFar[:,-1] / prcSoFar[:,-2])    #creates an array of the percentage change in each stock this new day
    rpos = np.array([int(x) for x in 2000000 * lastRet / prcSoFar[:,-1]])    #some random formula they've given us to decide to buy new stocks
    currentPos = np.array([int(x) for x in currentPos+rpos])    #updating with the stocks it decided to buy
    return currentPos
