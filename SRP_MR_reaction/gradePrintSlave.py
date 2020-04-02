from cclib.parser import *
import logging,math





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
        gap=abs(self.extracter('scfenergies',outProd)[-1]-self.extracter('scfenergies',outReac)[-1]-0.7285026668)*1 # for example, (computed_energy-ref_energy)*its_weight . summing it all..
        
        return gap

    def extracter(self,trait,filer):
        self.ccfile=ccopen(filer) #opens the out file in cclib
        self.ccfile.logger.setLevel(logging.ERROR) # avoid printing to the screen all the data cclib wants to print
        data=self.ccfile.parse() # data contain anything cclib knows to extract
        return getattr(data,trait) #getattr is like returning data.trait

    def energy(self):
        en=0.0
        count=0
		# The energy in cclib is presented in electron volts (eV)
        # accordin to the paper, we sum the gaps of any trait, and gives any trait its weight
        for filer in self.prodOuts:
            en+=self.extracter('scfenergies',filer)[-1] #prodStoich[count][0] is the stoich of the first reaction.
        for filer in self.reacOuts:
            en-=self.extracter('scfenergies',filer)[-1]
        print ('ENNNNNNNNNNN'+str(en))
        return en

    
if __name__=='__main__':
    grader.traits=[['energy']]
    grad=grader()
    for i in range(1,600):
        a='GaussFiles/reactants/reactants_'+str(i)+'.out'
        b='GaussFiles/TS_state/TS_state_'+str(i)+'.out'
        print(str(i)+'\t'+str(grad.getDictGrade([a],[b])))
        
