from scipy import *
from scipy.stats import rv_discrete 
import numpy,sys
import random
from copy import deepcopy
from mutator import *

class mater(object):
    qOfGeometricSeries=0.7
    rateOfCrossovers=1.0


    def __init__(self,dictGradeList):
        self.father=None
        self.mother=None

        while not self.mother:
            for candidatedict in dictGradeList:
                if random.randint(0,1):
                    self.mother=candidatedict[0]
                    #reducing the probability of a dict to be re-chosen by moving it to the end of the list:
                    dictGradeList.remove(candidatedict)
                    dictGradeList.append(candidatedict) 

        while not self.father:
            for candidatedict in dictGradeList:
                #further reduction of the option father=mother:
                if candidatedict==self.mother:
                    if random.randint(0,1):
                        continue
                if random.randint(0,1):
                    self.father=candidatedict[0]


        if random.randint(0,1): #replacing mother and father
                temp=self.mother
                self.father=self.mother
                self.mother=temp
        self.child=[]

    #def mate(self,percentageForOnlyOneParentInTheChild):
    #    #percentageForOnlyOneParentInTheChild is a number between 0 to 100
    #    if random.randint(0,100)<percentageForOnlyOneParentInTheChild:
    #        if random.randint(0,1): #0 is father, 1 is mother
    #            self.child=self.mother
    #        else:
    #            self.child=self.father
    #    else:
    #        self.makeCrossovers() #Applies crossovers to self.child


    def applyMutations(self,generationNum):
        self.child=mutator(self.child,generationNum).mutate()

    def getChild(self):
        return (self.child)


    def makeCrossovers(self,generationNum):
        """
            creates self.child -> self.dict[atom] = [parameter name, value, fraction of change]
        """   
        self.rateOfCrossovers=mater.rateOfCrossovers/generationNum
        counterAtomsLevel=0 #inside AtomsLevel
        counterDictLevel=0  #inside DictLevel
        counterParamLevel=0 

        atomSource=self.father #Take into account that father/mother are random chosen in the init function
        child=deepcopy(atomSource)
        placesForCrossoversInTheAtomDictLevel=self._getRandomCrossoversPlaces(len(self.father))
        #print(__file__.split('/')[-1]+':\t'+'numOfCrossovers\t'+str('1st level')+'\tchromeLen= '+str(len(self.father))+' q ')

        #print (__file__.split('/')[-1]+':\t'+'placesForCrossoversInTheAtomDictLevel: '+str(placesForCrossoversInTheAtomDictLevel))
        for atom in atomSource: #len(father) equals len(mother)
            if counterAtomsLevel in placesForCrossoversInTheAtomDictLevel: #There is a crossover
                if atomSource==self.father:
                    atomSource=self.mother
                elif atomSource==self.mother:
                    atomSource=self.father
                else:
                    print (__file__.split('/')[-1]+':\t'+'Error in choosing the source!')
                    sys.exit()
            counterAtomsLevel+=1
      
            dictSource=atomSource
            placesForCrossoversInTheChromoDictLevel=self._getRandomCrossoversPlaces(len(dictSource[atom]))
            #print(__file__.split('/')[-1]+':\t'+'numOfCrossovers\t'+str('2rd level')+'\tchromeLen= '+str(len(dictSource[atom]))+' q ')
            #print (__file__.split('/')[-1]+':\t'+'placesForCrossoversInTheChromoDictLevel: '+str(placesForCrossoversInTheChromoDictLevel))
            for idx in range(len(dictSource[atom])): #len(father) equals len(mother)
                # iterate through parameters under specific atom ("dict"). idx is the index of each dict               
                if counterDictLevel in placesForCrossoversInTheChromoDictLevel:
                    if dictSource==self.father:
                        dictSource=self.mother
                    elif dictSource==self.mother:
                        dictSource=self.father
                    else:
                        print (__file__.split('/')[-1]+':\t'+'Error in choosing the source!')
                        sys.exit()
                counterDictLevel+=1

                paramSource=dictSource
                nums=paramSource[atom][idx][1].split(',')
                if len(nums)==0 or len(nums)==1:
                    placesForCrossoversInsideEachParameter=[]
                else:
                    placesForCrossoversInsideEachParameter=self._getRandomCrossoversPlaces(len(nums))
                #print (__file__.split('/')[-1]+':\t'+'numOfCrossovers\t'+str('3rd level')+'\tchromeLen= '+str(len(nums))+' q ')
                #print (__file__.split('/')[-1]+':\t'+'placesForCrossoversInsideEachParameter: '+str(placesForCrossoversInsideEachParameter))
                for indx in range(len(nums)):
                    if counterParamLevel in placesForCrossoversInsideEachParameter:
                        if paramSource==self.father:
                            paramSource=self.mother
                        elif paramSource==self.mother:
                            paramSource=self.father
                        else:
                            print (__file__.split('/')[-1]+':\t'+'Error in choosing the source!')
                            sys.exit()
                    counterParamLevel+=1

                    nums=paramSource[atom][idx][1].split(',')
                    print (__file__.split('/')[-1]+':\t'+'\033[91m'+'Parameter is:   '+str(child)+'\033[0m')
                    child[atom][idx][1]=','.join(str(u) for u in nums)
                    #print (__file__.split('/')[-1]+':\t'+'\033[93m'+'Chiled par is:   '+str(child[atom][idx][1])+'\033[0m')
                    #print()
        #print (__file__.split('/')[-1]+':\t'+'\033[93m'+'Chiled par is:   '+str(child==self.father)+'\033[0m')
        self.child=child



    def _getRandomCrossoversPlaces (self,chromLen):
        if mater.rateOfCrossovers<random.random():
            return ([])
        chromLen=chromLen-1 #-1 for example: for len 2 maximum 1 crossover
        """
        #how many crossovers there are?
          We want the number of crossovers to be up to the (length of the chromosome)-1,
          with higher probability for lower rates. I've chosen a geometric series for that sake.
          For long chromosomes we can ignore the q**n so the sum is: s=a/(1-q) and for s=1
          a=1*(1-q). I assume that a "long chromosome" for that sake is just longer than 10.
          Starting with q=0.8, a=0.2.
          But since the chromosome isn't infinite in length, I'll take a that compensates q=>0.8.
        """
        q=mater.qOfGeometricSeries #0.8
        a=(1-q)/(1-(q**chromLen)) #(q**chromLen) goes to zero when chromLen goes to infinity
        
        # Array of chrossovers probability. The sum of its values is 1
        crossProbByIdx=numpy.zeros(chromLen)
        
        crossProbByIdx[0]=a #Initialization of the first value
        #Creating the geometric series
        for idx in xrange(1,chromLen): #xrange(1,3)=[1,2] 
            crossProbByIdx[idx]=crossProbByIdx[idx-1]*q
        #"stats.rv_discrete" funcion chooses from the first array a value according to the matching probability in the seccond array
        numOfCrossovers=rv_discrete(values=(range(1,chromLen+1),crossProbByIdx)).rvs()

        #choosing crossovers places. 0 for all chromosome1 chromLen+1 for all chromosome2
        crossoversPlaces=[]
        for i in range(numOfCrossovers):
            crossoversPlaces.append(random.randint(0,chromLen+1))
        crossoversPlaces=sorted(list(set(crossoversPlaces)))
        #set() removes duplicates

        
        #print crossProbByIdx
        return crossoversPlaces
        #Devision of the chromosome into parts and determining the division position:
##        positions=[]
##        for rate in crossoversRate:
##            positions.append(randint(0,len(chromosome1)-1))
##        positions=sorted(set(positions))
##        
##        
##        for positon in positions:

#dica={'a':[7,6,5,4]}
#dicb={'b':[5,5,6,6]}
#a=mater(dica,dicb)
#a.makeCrossovers()
#for i in range(100):
#    sm=a.getRandomCrossoversRate(100)
#    if sm>50:
#        print sm
#    print a.crossoversPlaces 
#    bb=3
#        
