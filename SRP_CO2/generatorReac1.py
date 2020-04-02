from outExtractor import extractor
from copy import deepcopy
from multiprocessing import Queue
from Gauss_connector import Gaussian_connector as runner


#class generatorReac(generatorSingle):
class generatorReac(object):
    bestDict={}
    best=((None,None),1000) #This tuple contain the best (products,reactants) set and the best gap related to that set.
    grade=[]
    gradeTemp=[]
    deltaEs=[]   
    errorHand=None
    b=open('blogreac.txt','w')
    ccc=1
    logs=open('logs2.txt','w')

    def __init__(self,reacInputs,prodInputs,globalDict):
        '''
        each reactat & product is list of the names of the reactants or products
        '''

        self.dict=globalDict
        self.reacInputs=reacInputs
        self.prodInputs =prodInputs
        #self.chanReac=deepcopy(reactants)
        #self.chanProd=deepcopy(products)
        #gauss=Gaussian_connector() # This object can sends a run to Gaussian and return the out file
        qur,qup=Queue(),Queue() # These two queues for prods and reacs, they can put and get things.
        reacJobs=[runner(reaci,qur) for reaci in reacInputs]  #Creation of Process object that can start(). It comunicates via a Queue object
        prodJobs=[runner(prodi,qup) for prodi in prodInputs]  #Creation of Process object that can start(). It comunicates via a Queue object

        for job in reacJobs+prodJobs: job.start()# The job in the gaussian_connector class starts.
        self.reacOuts,self.prodOuts=[],[]
        for job in reacJobs: self.reacOuts.append(open(qur.get())) # return, via quer the out file
        for job in prodJobs: self.prodOuts.append(open(qup.get())) # return, via quep the out file
        for job in reacJobs+prodJobs: job.join()
        qup.close(); qur.close()
        
    def getReacOutFilenames(self):
        return (self.reacOuts)
    def getProdOutFilenames(self):
        return (self.prodOuts)

    def getBestDict(self):
        #print '\nBD: '+str(self.bestDict==self.dict)+'    Objects: '+str(self.dict.update)#+'   '+str(self.bestDict.update)+'   '+'\n'
        return deepcopy(self.bestDict)
    
    def __str__(self):
        self.b.close()
        self.__class__.logs.close()
        return ('\n\n-------------------\n These are the results:'+'\nTemp Section:'+str(self.gradeTemp)+'\n\nRunning section'+str(self.grade)+'\nThe best is: \n'+str(self.best))


 

        
if __name__=='__main__':
    
    a=generReaction(2,3)
    a.bestDict=7
    print (generReaction.bestDict)
    print (a.bestDict)    
    print (a.best)
