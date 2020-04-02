import random, math, logging 
from Gauss_connector import Gaussian_connector
from cclib.parser import ccopen
from copy import deepcopy
import AtomsParser

besten=-3.900
random.seed(3)
# This is an arbitrary value that the error_function aspires to. 


class generator(object):
    '''
        This is an abstract class. Its variables must be declared in an __init__ function in its childs.
        this class contain the error function and the connection to Gaussian.
    '''
    ccc=1
    logs=open('logs1.txt','w')
    changePar=AtomsParser.changeParser() # This is a dictionary that its last value of any parameter is the amount of change to this parameter. 
        
    def getMeanDeltaE(self): #returns mean of "deltaE" of MC
        if hasattr(generator,'firstemp'): #returns mean of "deltaE" of MC. The difference from the the next (default) return is that it only returns from the middle to the end and not the all DeltaE.
            return sum(self.deltaEs[int((len(self.deltaEs)-1)/2):])/len(self.deltaEs[int((len(self.deltaEs)-1)/2):])
        generator.firstemp=True # This will tell the next runs that it exists
        print 'FIRSTEMP does exists!!!'
        return sum(self.deltaEs)/len(self.deltaEs) # We are on the first run, thus need all the deltaE       

        
    #return True or false depends on the random number
    def weighter(self,yes,deltaE):
        print '\ngap is: %s, math.exp(-gap/temp) is %s, yes-0.5 is %s' %(self.gap,math.exp(-self.gap/self.temp),yes-0.5)
        return (random.random()-math.exp(-deltaE/self.temp))<(yes-0.5)

    #this function will change numbers according to the DISTance allowed:
    def randomChooser(self,number,var):
    #number is the number to change, var is number of how much to change this parameter.
        a=random.random()
        self.__class__.logs.write(str(a)+'  DIST  '+str(self.DIST)+'\n')
        
        return number+var*(a-0.5)*(number*self.DIST)

    def dictChanger(self):        
        """
            changes self.dict. self.dict[atom]-> [parameter name, value, fraction of change]
        """
        
        for atom in self.dict:
            self.b.write(str(self.ccc))
            generator.ccc+=1
            for idx in range(len(self.dict[atom])):
                nums=self.dict[atom][idx][1].split(',')
                var=self.changePar[atom][idx][2]
                self.b.write(str(nums)+'\t'+str(var)+'\n')
                for indx in range(len(nums)):
                    if '.' in nums[indx]:
                                 self.__class__.logs.write('Num: b\t'+str(nums[indx])+'var:'+str(var)+'\n')                                 
                                 nums[indx]=self.randomChooser(float(nums[indx]),var)
                                 self.__class__.logs.write('Num: a\t'+str(self.__class__.ccc)+'\t'+str(nums[indx])+'\n')
                                 #nums[indx]=float(nums[indx])+0.0001
                self.dict[atom][idx][1]=','.join(str(u) for u in nums)

    def accept(self,newdict):
        self.grade.append(self.gap) # appending the gap to all grades, so in the next line we can choose the best one
        self.dict=deepcopy(newdict) # This is assignment to dict is the new dict
        if self.gap<self.best[1]:
            self.bestDict=deepcopy(self.dict) 
            self.best=(self.filename,self.gap)
            self.best=self.best
        self.dictChanger() # This function changes self.dict with the right self.DIST . We can change the dict only after assignment to bestdict
        print '\nAccepted!\n'
        
    

    def extracter(self,trait):
        self.ccfile=ccopen(self.outFile) #opens the out file in cclib
        self.ccfile.logger.setLevel(logging.ERROR) # avoid printing to the screen all the data cclib wants to print
        data=self.ccfile.parse() # data contain anything cclib knows to extract
        return getattr(data,trait)
            
    def getDict(self):
        return self.dict

    def getBestDict(self):
        #print '\nBD: '+str(self.bestDict==self.dict)+'    Objects: '+str(self.dict.update)#+'   '+str(self.bestDict.update)+'   '+'\n'
        return deepcopy(self.bestDict)

    
    def __str__(self):
        self.b.close()
        self.__class__.logs.close()
        return '\n\n-------------------\n These are the results:'+'\nTemp Section:'+str(self.gradeTemp)+'\n\nRunning section'+str(self.grade)+'\nThe best is: \n'+str(self.best)




class generatorSingle(generator):

    bestDict={}
    def __init__(self):
        self.best=(None,1000)
        self.grade=[]
        self.gradeTemp=[]
        self.deltaEs=[]
        self.gauss= Gaussian_connector() # This object can send a run to Gaussian and return the out file
        self.got=False
        
        self.b=open('blogsin.txt','w')

        
    def generate(self,filename,newdict,olddict,DIST,temp,yes):
        self.filename=filename
        #DIST is a DISTance of a random walk step:
        self.DIST=DIST
        self.temp=temp
        self.outFile=self.gauss.runner(filename) # runner run the file and return the out file upon finish
        self.errorFunction() #Fires the error function
        
        self.got=True # If we will accept the dictionary from the last iteration, we will leave it.
        if not self.grade: # It is the first run
            self.accept(newdict)
            return newdict
        if self.gap<self.grade[-1]: # The dict from last change is better then that from its preceder
            self.accept(newdict)
        else:
            if self.weighter(yes,self.gap-self.grade[-1]): # weights the result in random way and returns True (=acception) or False (=rejection)
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

    #this function generates the temperature for the first time
    def generateTemp(self,filename,olddict,DIST):
            self.filename=filename
            #DIST is a DISTance of of random walk:
            self.DIST=DIST
            
            self.dict=deepcopy(olddict) # This is assignment to dict is the new dict
            
            self.outFile=self.gauss.runner(filename) # runner run the file and return the out file upon finish
            self.errorFunction() #Fires the error function        
            #if self.gradeTemp (and self.gap>self.gradeTemp[-1] ?? - no):
            if self.gradeTemp:
                      self.deltaEs.append(abs(self.gap-self.gradeTemp[-1]))
            

            if self.gap<self.best[1]:
    
                self.bestDict=deepcopy(self.dict)  #This bestDict will be the first dictionary for MC runs.
                self.best=(self.filename,self.gap)
           
            self.gradeTemp.append(self.gap) # appending the gap to all grades
            self.dictChanger()
            return  self.dict

    def errorFunction(self):
        # accordin to the paper, we sum the gaps of any trait, and gives any trait its weight
        self.gap=abs(besten-self.extracter('scfenergies')[0])

    
