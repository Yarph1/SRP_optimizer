from cclib.parser import ccopen
import logging,math

class errorFunction(object):
    '''
        This class contain optional configurations of the error fucntions
    '''
    #traits is:[trait,weight,value]
    def __init__(self,traits,reacStoich,prodStoich):
        #reacStoich and prodStoich contains number that is the number of the occurance of that reactant or product in the reaction
        self.traits=traits
        self.reacStoich=reacStoich
        self.prodStoich=prodStoich
        print 'The traits this module will find are:\n'+str(self.traits)
        
        
    
    def extracter(self,trait,filer):
        self.ccfile=ccopen(filer) #opens the out file in cclib
        self.ccfile.logger.setLevel(logging.ERROR) # avoid printing to the screen all the data cclib wants to print
        data=self.ccfile.parse() # data contain anything cclib knows to extract
        return getattr(data,trait) #getattr is like returning data.trait

    def energy(self):
        en=0.0
        count=0
        # accordin to the paper, we sum the gaps of any trait, and gives any trait its weight
        for filer in self.outProd:
            en+=self.extracter('scfenergies',filer)[0]*self.prodStoich[count][0] #prodStoich[count][0] is the stoich of the first reaction.
            count+=1

        count=0
        
        for filer in self.outReac:
            en-=self.extracter('scfenergies',filer)[0]*self.reacStoich[count][0]
            count+=1
            
        return en
        
    def getError(self,outReac,outProd):
        gap=0
        self.outReac=outReac
        self.outProd=outProd
        for i in range(len(self.traits)):
            gap+=abs(getattr(self,self.traits[i][0])()-self.traits[i][2])*self.traits[i][1] # for example, (computed_energy-ref_energy)*its_weight . summing it all..
        return gap


    
if __name__=='__main__':
    n=errorFunction(3)
    n.call()
    
