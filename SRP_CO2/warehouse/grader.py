from extractor import *

class grader(generator):
    def __init__(self,reacFiles,prodFiles,DIST,globalDict):
        '''
        each reactat & product is list of the names of the reactants or products
        '''       
        self.reacFiles=reacFiles
        self.prodFiles =prodFiles
        #self.chanReac=deepcopy(reactants)
        #self.chanProd=deepcopy(products)
        gauss=Gaussian_connector() # This object can sends a run to Gaussian and return the out file
        self.reacOuts=[gauss.runner(reaci) for reaci in reacFiles]  # runner run the file and return the out file upon finish
        self.prodOuts=[gauss.runner(prodi) for prodi in prodFiles]  # runner run the file and return the out file upon finish





    def errorFunction(self):
        #This function return the gap. gap is the deviation from the referrence values.
        self.gap=abs(besten-self.extracter('scfenergies')[0])

if __name__=='__main__':  
    pass