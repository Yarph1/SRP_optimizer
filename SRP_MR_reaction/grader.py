from cclib.parser import ccopen
import logging,math
from outExtractor import extractor


class grader(object):
    '''
        This class contain optional configurations of the error fucntions
    '''
    traits=None
    #reacStoich and prodStoich contains number that is the number of the occurance of that reactant or product in the reaction
    reacStoich=None
    prodStoich=None
    def __init__(self):
        # self.reacStoich=reacStoich
        # self.prodStoich=prodStoich
        #print ('The traits this module will find are:\n'+str(self.traits))
        #This variable should be initialize in the main file after parsing the preffereces file
        assert self.__class__.traits !=None

        
        


#    def errorFunction(self):
#        #This function return the gap. gap is the deviation from the referrence values.
#        self.gap=abs(besten-self.extracter('scfenergies')[0])


    ##############polimorphism###############

    def getDictGrade(self,outReac,outProd):
        gap=0
        self.extractor=extractor(outReac,outProd)
        print(__file__.split('/')[-1]+':\t'+str(self.traits))
        for i in range(len(self.traits)):
            gap+=abs(getattr(self.extractor,self.traits[i][0])()-self.traits[i][2])*self.traits[i][1] # for example, (computed_energy-ref_energy)*its_weight . summing it all..
        return gap


    
if __name__=='__main__':
    n=grader(3)
    n.call()
    #print ('\033[92m'+str(dir(self))+'\033[0m')
