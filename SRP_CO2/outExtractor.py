import random, math, logging 
from Gauss_connector import Gaussian_connector
from cclib.parser import ccopen
from copy import deepcopy
import AtomsParser

besten=-3.900
random.seed(3)
# This is an arbitrary value that the error_function aspires to. 


class extractor(object):
    '''
        This is an abstract class. Its variables must be declared in an __init__ function in its childs.
        this class contain the error function and the connection to Gaussian.
    '''
    def __init__(self,reacOuts,prodOuts):
        self.prodOuts=reacOuts
        self.reacOuts=prodOuts
        #These 2 variables should be initialize in the main file after parsing the preffereces file
        assert self.__class__.reacStoich !=None
        assert self.__class__.prodStoich !=None


    def extracter(self,trait,filer):
        self.ccfile=ccopen(filer) #opens the out file in cclib
        self.ccfile.logger.setLevel(logging.ERROR) # avoid printing to the screen all the data cclib wants to print
        data=self.ccfile.parse() # data contain anything cclib knows to extract
        return getattr(data,trait) #getattr is like returning data.trait

    def energy(self):
        en=0.0
        count=0
        # accordin to the paper, we sum the gaps of any trait, and gives any trait its weight
        for filer in self.prodOuts:
            en+=self.extracter('scfenergies',filer)[-1]*self.prodStoich[count][0] #prodStoich[count][0] is the stoich of the first reaction.
            count+=1
        count=0        
        for filer in self.reacOuts:
            en-=self.extracter('scfenergies',filer)[-1]*self.reacStoich[count][0]
            count+=1
        return en

    def atomcharges(self):
        en=0.0
        count=0
        # accordin to the paper, we sum the gaps of any trait, and gives any trait its weight
        for filer in self.prodOuts:
            charges=self.extracter('atomcharges',filer)['mulliken']
            print (charges)
            count+=1
        count=0        
        for filer in self.reacOuts:
            charges=self.extracter('atomcharges',filer)['mulliken']
            print (charges)

            count+=1
        exit('END')
        return en

        exit("these where the charges")


    def structure(self):
        totalRMSD=0
        for filer in self.prodOuts:
            # Extract the coordinates from a geometry optimization
            p = ccopen(filer)
            data = p.parse()

            # Use the bridge to create two lists of Biopython atoms
            from cclib.bridge import makebiopython
            initial = makebiopython(data.atomcoords[0] , data.atomnos)
            final =   makebiopython(data.atomcoords[-1], data.atomnos)

            # Use Biopython to superimpose the two geometries and calculate the RMS
            from Bio.PDB.Superimposer import Superimposer
            superimposer = Superimposer()
            superimposer.set_atoms(initial, final)
            totalRMSD+= superimposer.rms
            print ('RMSD'+str(superimposer.rms))
        for filer in self.reacOuts:
            # Extract the coordinates from a geometry optimization
            p = ccopen(filer)
            data = p.parse()

            # Use the bridge to create two lists of Biopython atoms
            from cclib.bridge import makebiopython
            initial = makebiopython(data.atomcoords[0] , data.atomnos)
            final =   makebiopython(data.atomcoords[-1], data.atomnos)

            # Use Biopython to superimpose the two geometries and calculate the RMS
            from Bio.PDB.Superimposer import Superimposer
            superimposer = Superimposer()
            superimposer.set_atoms(initial, final)
            totalRMSD+= superimposer.rms
            print ('RMSD'+str(superimposer.rms))
        return (totalRMSD)

    def getDict(self):
        return self.dict


