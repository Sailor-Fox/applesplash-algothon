#My current applesplash.py
import numpy as np

nInst=50    #number of stocks
currentPos = np.zeros(nInst)    #we start with nothing
def getMyPosition (prcSoFar):
    print("-----------------------prcSoFar-----------------------")
    print(prcSoFar)
    print("------------------------------------------------------")
    global currentPos
    (nins,nt) = prcSoFar.shape    #nins = no. of rows = no. of instruments, nt = no. of columns = no. of days so far
    if (nt < 2):
        return np.zeros(nins)    #on day 1 you start with 0 stocks
   
    #arr = prcSoFar
    window_size = 20
    i=0
    moving_average = []
    while i < nt - window_size + 1:
        window = prcSoFar[i : i + window_size]
        window_average = sum(window)/window_size
        moving_average.append(window_average)
        i += 1
        print(moving_average)
       
  #  for i in range(nt - window_size + 1):
   #     window = prcSoFar[i : i + window_size]
    #    window_average = sum(window)/window_size
     #   moving_average.append(window_average)
      #  print(moving_average)
   
       
    BOLU = [x + np.std(prcSoFar, ddof = 2) for x in moving_average]
    BOLD = [x - np.std(prcSoFar, ddof = 2) for x in moving_average]
        #moving_average + np.std(prcSoFar, ddof = 2)
    #BOLD = moving_average - np.std(prcSoFar, ddof = 2)
    print("------------------------BOLU------------------------")
    print(BOLU)
    print("------------------------BOLD------------------------")
    print(BOLD)

    for j in range(nins):
        if prcSoFar[j] > BOLU[j]:
            prcSoFar[j] = 10*int(prcSoFar[j])
        elif prcSoFar[j] < BOLD[j]:
            prcSoFar[j] = 20*int(prcSoFar[j])
        else:
            prcSoFar[j] = prcSoFar[j]
        return prcSoFar
