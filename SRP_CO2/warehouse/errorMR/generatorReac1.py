from generatorSingle import *
from multiprocessing import Queue
from Gauss_connector1 import Gaussian_connector as runner

class generatorReac(generator):
    bestDict={}
    best=((None,None),1000) #This tuple contain the best (products,reactants) set and the best gap related to that set.
    grade=[]
    gradeTemp=[]
    deltaEs=[]   
    errorHand=None
    b=open('blogreac.txt','w')
    ccc=1
    logs=open('logs2.txt','w')

    def __init__(self,reacFiles,prodFiles,DIST,globalDict):
        '''
        each reactat & product is list of the names of the reactants or products
        '''

        self.dict=globalDict
        self.DIST=DIST  #DIST is a DISTance of a random walk step:       
        self.reacFiles=reacFiles
        self.prodFiles =prodFiles
        #self.chanReac=deepcopy(reactants)
        #self.chanProd=deepcopy(products)
        #gauss=Gaussian_connector() # This object can sends a run to Gaussian and return the out file
        qur,qup=Queue(),Queue() # These two queues for prods and reacs, they can put and get things.
        reacJobs=[runner(reaci,qur) for reaci in reacFiles]  #Creation of Process object that can start(). It comunicates via a Queue object
        prodJobs=[runner(prodi,qup) for prodi in prodFiles]  #Creation of Process object that can start(). It comunicates via a Queue object

        for job in reacJobs+prodJobs: job.start()# The job in the gaussian_connector class starts.
        self.reacOuts,self.prodOuts=[],[]
        for job in reacJobs: self.reacOuts.append(open(qur.get())) # return, via quer the out file
        for job in prodJobs: self.prodOuts.append(open(qup.get())) # return, via quep the out file
        for job in reacJobs+prodJobs: job.join()
        qup.close(); qur.close()
        

    def generateTemp(self):
                   

        self.errorFunction() #Fires the error function        
        if self.gradeTemp:
            self.deltaEs.append(abs(self.gap-self.gradeTemp[-1]))
        
        if self.gap<self.__class__.best[1]:

            self.__class__.bestDict=deepcopy(self.dict)  #The bestDict will be the first dictionary for MC runs.
            self.__class__.best=[str(self.reacFiles+self.prodFiles),self.gap]
       
        self.gradeTemp.append(self.gap) # appending the gap to all grades
        self.dictChanger()
        return self.dict        


    def generate(self,newdict,olddict,DIST,temp,chooseYes):
        
        #DIST is a DISTance of a random walk step:
        self.DIST=DIST
        self.temp=temp
        self.errorFunction() #Fires the error function
        
        self.got=True # If we will accept the dictionary from the last iteration, we will leave it.
        if not self.grade: # It is the first run
            self.accept(newdict)
            return newdict
        if self.gap<self.grade[-1]: # The dict from last change is better then that from its preceder
            self.accept(newdict)
        else:
            if self.weighter(chooseYes,self.gap-self.grade[-1]): # weights the result in random way and returns True (=acception) or False (=rejection)
                self.deltaEs.append(self.gap-self.grade[-1])
                self.accept(newdict)
            else:
                print '\nDeclined!\n'
                self.deltaEs.append(self.gap-self.grade[-1])
                #return olddict # We do not change the dict! This is not efficient, so we return the olddict (=the last good one) changed:
                self.dict=deepcopy(olddict)
                self.dictChanger()
                self.got=False # We DON'T accept the dictionary from the last iteration.
        return self.dict
    

    def errorFunction(self):
        #This function return the gap. gap is the deviation from the referrence values.
        self.gap=self.errorHand.getError(self.reacOuts,self.prodOuts)


    ##############polimorphism###############
        
    def getBestDict(self):
        return deepcopy(self.__class__.bestDict)

    def accept(self,newdict):
        self.grade.append(self.gap) # appending the gap to all grades, so in the next line we can choose the best one
        self.dict=deepcopy(newdict) # This is assignment to dict is the new dict
        if self.gap<self.__class__.best[1]:
            self.__class__.bestDict=deepcopy(self.dict) #if bestDict is a class member
            self.filename=str(self.prodFiles+self.reacFiles) # in case of reaction
            self.__class__.best=(self.filename,self.gap)
        self.dictChanger() # This function changes self.dict with the right self.DIST . We can change the dict only after assignment to bestdict
        print '\nAccepted!\n'
                    
 

        
if __name__=='__main__':
    
    a=generReaction(2,3)
    a.bestDict=7
    print generReaction.bestDict
    print a.bestDict    
    print a.best
