#MODEL 3 WIP 

#!/usr/bin/env python

import numpy as np #testying
import statistics as statistics

nInst=50    #number of stocks
dlrPosLimit = 10000 #the cap in $ for having one stock
initialQuantity = 1000
incrementQuantity = 1000

myPositions = np.zeros(nInst)    #we start with nothing
myPosForStock = []

class posAndPrices:
    def printStatistics(self):
        VolumeBought = 0
        VolumeSold = 0
        Profit = 0
        VolumeUnsold = 0
        for i in range(len(self.ledger)):
            if self.ledger[i,1] > 0:
                VolumeBought += self.ledger[i,1]*self.ledger[i,0] #total volume bought
            #if self.ledger[i,2] > 0:
            VolumeSold += self.ledger[i,1]*self.ledger[i,2] #total volume sold 
            Profit += (self.ledger[i,2]-self.ledger[i,0])*self.ledger[i,1] #profit
           # if self.ledger[i,2] < 0:
                #Loss += (self.ledger[i,2]-self.ledger[i,0])*self.ledger[i,1] #loss?
            if self.ledger[i,1] > 0 and self.ledger[i,2] == 0:
                VolumeUnsold += self.ledger[i,1]*self.ledger[i,0] #unsold
        print("Volume Bought: $%.2lf, Volume Sold: $%.2lf, Profit: $%.2lf, Volume Unsold: $%.2lf" % (VolumeBought, VolumeSold, Profit, VolumeUnsold))
    
    def printSelf(self):
        #print("Ledger :", self.ledger)
        print("Max %.2lf, Min %.2lf, Total %.2lf, Avg %.2lf, Margin %.2lf" % (self.max, self.min, self.total, self.avg, self.margin))
        
    def getNumberofStocks(self):
        return (np.sum(self.ledger[:,1]))
    
    def getNumberofStocksforPrice(self, price):
        number_of_stocks = 0
        for i in range(len(self.ledger)):
            if (price - self.ledger[i,0]) >= self.margin and self.ledger[i,1] > 0:
                number_of_stocks += self.ledger[i,1]
                self.ledger[i,2] = price #updating selling price
        return number_of_stocks
            
    def addPosAndPrice(self, price, position):
        temp_ledger = np.zeros((1, 3))
        temp_ledger[0, 0] = price
        temp_ledger[0, 1] = position
        temp_ledger[0,2] = 0 
        self.ledger = np.append(self.ledger, temp_ledger, axis=0)
        if (self.max < price):
            self.max = price
        if (self.min > price):
            self.min = price
        self.total += price
        self.avg = self.total/len(self.ledger)
        self.std = np.std(self.total)
        self.margin = self.std # in cents #############################

    def __init__(self, price, position):
        self.ledger = np.zeros((1, 3))
        self.ledger[0, 0] = price #buying price
        self.ledger[0, 1] = position #no. of stocks
        self.ledger[0,2] = 0 #selling price
        self.max = price
        self.min = price
        self.avg = price
        self.total = price
        self.margin = 0
        
        
def getMyPosition (prcSoFar):
    #print("================================")
    #print("prcSoFar: ", prcSoFar)
    global myPositions
    global myPosForStock
    
    (nins,nt) = prcSoFar.shape    #nins = no. of rows = days passed so far, nt = no. of columns = 50
    #if (nt == 207 or nt == 145):
        #print("rows = ", nins, " columns =", nt, " currentPos :", myPositions)
        
    if (nt < 2):
        myPositions = np.array([int(x) for x in initialQuantity / prcSoFar[:, -1]])
        for position in range(nInst):
            myPosForStock.append(posAndPrices(prcSoFar[position, -1], myPositions[position]))

        #print("first day positions :", myPositions)
        #for position in range(nInst):
        #    print("first day myPosForStock [", position, "] = ", myPosForStock[position].ledger)

        return myPositions
    
    change_in_price = prcSoFar[:,-1] - prcSoFar[:,-2]
    #if (nt == 207 or nt == 145):
        #print("Change in Price:", change_in_price)
    
    for position in range(nInst):
        posAndPricesObj = myPosForStock[position]
        stocksToSell = posAndPricesObj.getNumberofStocksforPrice(prcSoFar[position,-1])
        if stocksToSell > 0:
            myPositions[position] -= int(stocksToSell)
        else:
            myPositions[position] += int(incrementQuantity/prcSoFar[position,-1])
           
    curPrices = prcSoFar[:,-1]
    posUpperLimits = np.array([int(x) for x in dlrPosLimit / curPrices])
    posLowerLimits = np.zeros(nInst)
    clipPos = np.clip(myPositions, posLowerLimits, posUpperLimits)    
    #if (nt == 207 or nt == 145):
        #print("myPositions: ", myPositions)
        #print("posUpperLimits: ", posUpperLimits)
        #print("posLowerLimits: ", posLowerLimits)
        #print("clipped positions: ", clipPos)

    myPositions = np.array([np.trunc(x) for x in clipPos])
    #if (nt == 207 or nt == 145):
        #print("my new positions :", myPositions)

    for position in range(nInst):
        posAndPricesObj = myPosForStock[position] 
        price = prcSoFar[position, -1]
        stockPosition = myPositions[position] - posAndPricesObj.getNumberofStocks()
        posAndPricesObj.addPosAndPrice(price, stockPosition)
        #if (position == 3):
        #    posAndPricesObj.printSelf()
            
        if (nt == 250):
            print("Stock: ", position)
            posAndPricesObj.printStatistics()
            
    return myPositions
