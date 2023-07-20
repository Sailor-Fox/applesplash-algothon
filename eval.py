#!/usr/bin/env python

import numpy as np
import pandas as pd
from AppleSplash import getMyPosition as getPosition

nInst = 0    #will be used for number of stocks
nt = 0    #will be used for the number of days later
commRate = 0.0010    #commission rate
dlrPosLimit = 10000 #the cap in $ for having one stock

#this function imports the prices and sets the number of stocks and days to the right values
def loadPrices(fn):
    global nt, nInst
    #df=pd.read_csv(fn, sep='\s+', names=cols, header=None, index_col=0)
    df=pd.read_csv(fn, sep='\s+', header=None, index_col=None)
    nt, nInst = df.values.shape
    return (df.values).T

pricesFile="./prices.txt"
prcAll = loadPrices(pricesFile)
print ("Loaded %d instruments for %d days" % (nInst, nt))

currentPos = np.zeros(nInst)

def calcPL(prcHist):
    #start all the money and stuff at 0
    cash = 0
    curPos = np.zeros(nInst)
    totDVolume = 0
    totDVolumeSignal = 0
    totDVolumeRandom = 0
    value = 0
    todayPLL = []
    (_,nt) = prcHist.shape
    for t in range(1,251): 
        prcHistSoFar = prcHist[:,:t]    #imports the prices of the stocks up until day t
        newPosOrig = getPosition(prcHistSoFar)    #inputs those prices into our bot
        curPrices = prcHistSoFar[:,-1]    #prcHist[:,t-1] takes the last day of prices? (not 100% sure on that)
        
        #enforcing the $10,000 cap below this
        posLimits = np.array([int(x) for x in dlrPosLimit / curPrices])
        clipPos = np.clip(newPosOrig, -posLimits, posLimits)    
        newPos = np.array([np.trunc(x) for x in clipPos])
        
        deltaPos = newPos - curPos    #finds the difference from day before to this day (so it can work out the trade costs)
        dvolumes = curPrices * np.abs(deltaPos)    #price of each trade as a vector (50 elements, one for each stock)
        dvolume = np.sum(dvolumes)    #total price of trades for the dat
        totDVolume += dvolume    #keeps track of total volume traded over all days
        comm = dvolume * commRate    #finds the commission price for the day
        cash -= curPrices.dot(deltaPos) + comm    #updates the cash position based on how much the day's trades cost
        curPos = np.array(newPos)    #updates our position (how many of each stock we have)
        posValue = curPos.dot(curPrices)    #updates our current value (number of each stock times the value of the each stock)
        todayPL = cash + posValue - value    #today's PL = cash spent/gained + valuation of current stocks - the previous total value
        todayPLL.append(todayPL)    #adds on today's PL to the array storing the PL of each day (this gets used for scoring later on)
        value = cash + posValue    #updates the total value
        ret = 0.0    #restore daily return to default
        if (totDVolume > 0): #if no trades have ever been made then return is 0 (basically on day 1 the return is 0)
            ret = value / totDVolume    #find the return (of current value divided by money spent on trades (excluding the commission)
        print ("Day %d value: %.2lf todayPL: $%.2lf $-traded: %.0lf return: %.5lf" % (t,value, todayPL, totDVolume, ret))    #print the day's metrics
    
    pll = np.array(todayPLL)    #stores the matrix with every day's PLL as pll
    (plmu,plstd) = (np.mean(pll), np.std(pll)) #obtain the scoring metrics from the pll matrix
    annSharpe = 0.0    #set as default value
    if (plstd > 0):    #if your standard deviation is 0, then annSharpe = 0
        annSharpe = np.sqrt(250) * plmu / plstd    #calculate annSharpe
    return (plmu, ret, plstd, annSharpe, totDVolume)    #the function calcPL returns the metrics used in scoring



(meanpl, ret, plstd, sharpe, dvol) = calcPL(prcAll)
score = meanpl - 0.1*plstd
print ("=====")
print ("mean(PL): %.1lf" % meanpl)
print ("return: %.5lf" % ret)
print ("StdDev(PL): %.2lf" % plstd)
print ("annSharpe(PL): %.2lf " % sharpe)
print ("totDvolume: %.0lf " % dvol)
print ("Score: %.2lf" % score)


