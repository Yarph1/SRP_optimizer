import random, math, logging,sys
from copy import deepcopy
import AtomsParser


class mutator(object):

    def __init__(self,chromoDict,generationNum,DIST=0.03,rateChromo=0.27,rateGene=0.27):
        #rateGene and rateChromo are the rates for mutations in genes and chromosomes
        #DIST Long step for arbitrary search for the mean.
        self.dict=deepcopy(chromoDict)
        self.DIST=DIST 
        print (generationNum)
        self.rateCromo=rateChromo/math.log(float(generationNum)+1) # a number in the range [0,1]
        self.rateGene=rateGene/math.log(float(generationNum)+1)    
        if random.randint(0,1):
            self.rateCromo=0.05
        if random.randint(0,1):
            self.rateGene=0.05
        self.changePar=AtomsParser.changeParser() # This is a dictionary that its last value of any parameter is the amount of change to this parameter. 
                

    def _randomChooser(self,number,var):
        '''
        This function will change numbers according to the DISTance allowed
        Number is the number to change, var is number of how much to change this parameter.
        '''
        a=random.random()
        #self.__class__.logs.write(str(a)+'  DIST  '+str(self.DIST)+'\n')
        
        return number+var*(a-0.5)*(number*self.DIST)

    def mutate(self):        
        """
            changes self.dict -> self.dict[atom] = [parameter name, value, fraction of change]
            and return a new dict that contains the mutations
        """   
        for atom in self.dict:

            randNum=random.random()
            print ('***********Mutator: self.rateCromo='+str(self.rateCromo)+' self.rateGene '+str(self.rateGene)+' rand '+str(randNum))
            if randNum>self.rateCromo:
                continue #rateChromo is the mutation acceptance rate for the entire chromosome

            for idx in range(len(self.dict[atom])):
                #idx is the index of each chromosome
                nums=self.dict[atom][idx][1].split(',')
                var=self.changePar[atom][idx][2]
                #self.b.write(str(nums)+'\t'+str(var)+'\n')
                for indx in range(len(nums)):
                    
                    if random.random()>self.rateGene:
                        continue #rateGene is the mutation acceptance rate for some specific gene = a specific parameter
                    #print('****Mutation!!****: '+ str(self.rateGene))

                    if '.' in nums[indx]:
                        #self.__class__.logs.write('Num: b\t'+str(nums[indx])+'var:'+str(var)+'\n')
                        nums[indx]=self._randomChooser(float(nums[indx]),var)
                        #self.__class__.logs.write('Num: a\t'+str(self.__class__.ccc)+'\t'+str(nums[indx])+'\n')
                        #nums[indx]=float(nums[indx])+0.0001
                self.dict[atom][idx][1]=','.join(str(u) for u in nums)
        return self.dict

 
class monteCarloMutator(mutator):
    ccc=1
    logs=open('logs1.txt','w')
        
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
            
    def getDict(self):
        return self.dict

    def getBestDict(self):
        #print '\nBD: '+str(self.bestDict==self.dict)+'    Objects: '+str(self.dict.update)#+'   '+str(self.bestDict.update)+'   '+'\n'
        return deepcopy(self.bestDict)
    
    def __str__(self):
        self.b.close()
        self.__class__.logs.close()
        return '\n\n-------------------\n These are the results:'+'\nTemp Section:'+str(self.gradeTemp)+'\n\nRunning section'+str(self.grade)+'\nThe best is: \n'+str(self.best)


    def monteCarloMutation(self,newdict,olddict,temp,chooseYes):
        
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
                print ('\nDeclined!\n')
                self.deltaEs.append(self.gap-self.grade[-1])
                #return olddict # We do not change the dict! This is not efficient, so we return the olddict (=the last good one) changed:
                self.dict=deepcopy(olddict)
                self.dictChanger()
                self.got=False # We DON'T accept the dictionary from the last iteration.
        return self.dict

    def generateTempFirst(self):
        self.errorFunction() #Fires the error function        
        if self.gradeTemp:
            self.deltaEs.append(abs(self.gap-self.gradeTemp[-1]))
        
        if self.gap<self.__class__.best[1]:

            self.__class__.bestDict=deepcopy(self.dict)  #The bestDict will be the first dictionary for MC runs.
            self.__class__.best=[str(self.reacFiles+self.prodFiles),self.gap]
       
        self.gradeTemp.append(self.gap) # appending the gap to all grades
        self.dictChanger()
        return self.dict        
    def accept(self,newdict):
        self.grade.append(self.gap) # appending the gap to all grades, so in the next line we can choose the best one
        self.dict=deepcopy(newdict) # This is assignment to dict is the new dict
        if self.gap<self.__class__.best[1]:
            self.__class__.bestDict=deepcopy(self.dict) #if bestDict is a class member
            self.filename=str(self.prodInputs+self.reacInputs) # in case of reaction
            self.__class__.best=(self.filename,self.gap)
        self.dictChanger() # This function changes self.dict with the right self.DIST . We can change the dict only after assignment to bestdict
        print ('\nAccepted!\n')
    def grade(self,newdict,olddict,DIST,temp,chooseYes):
        self.temp=temp
        self.errorFunction() #Fires the error function
        return self.gap
      


if __name__=='__main__':

    pass
    
