from Input import Input
import os,time,re,multiprocessing,error
from math import log
from copy import deepcopy
from generatorReac import generatorReac 
#from Gauss_connector import Gaussian_connector
inCounter=0


#gener will run the self.filename in Gaussian & will generated a new dict
FILENOTEMP=10000
FILENO = 200


def handleFile0(filename):
    print filename,'\n'
    basename = ".".join(filename.split('/')[-1].split('.')[:-1])
    inp = Input(filename, basename, inCounter) # Initializing an object of Input module
    rvalues = inp.modify();del inp

    #return structure:  ([name of new file(filename),basename,template of file, dictionary of this file])
    return ([rvalues[1],basename,rvalues[2],rvalues[0]])

def rmsd(dic1,dic2):
    summ=0
    cout=0
    for atom in dic1:
        for attrNum in range(len(dic1[atom])):
            nums=dic1[atom][attrNum][1].split(',')
            for indx in range(len(nums)):
                if '.' in nums[indx]:
                    summ+=abs(float(num[indx])-float(dic2[atom][attrNum][1].split(',')[indx]))
                    cout+=1
    return summ/float(cout)


def tempGener(reactants,products,globalDict):
    global inCounter,gener
    DIST=0.001
    print '\n\n\nThis part is about generating the DeltaE to take temp=(-deltaE/ln(1-[acceptance fraction]))\n\n'
    #dictionaries=[]
    newDict=globalDict
    DIST=0.001 #Long step for arbitrary search for the mean.    
    for idxx in range(FILENOTEMP):
        reacFiles,prodFiles=[],[]
        for attr in reactants: # This part will generate input files for reactants and products
            filename=attr[0]
            template=attr[2]
            basename=attr[1]
            inp = Input(filename, basename, inCounter, template, newDict)
            
            # =(self.filename, self.basename, inCounter, self.template, newDict)
            
            ## newDict is the dictionary we want to implement.
            ## self.template is a string of the lines of the user input
            ##untill the first **** line.
            
            rvalues = inp.modify()
            """ This meathod creates a new input file and return a list of 3 or 2 organs:
                1) The dictionary that pulled to the new file.
                2) The name of the new file.
                3) String of the lines of the user input file untill the first **** line.
                * If it is not the first run, organ 3 dissmissed.
            """
            reacFiles.append(rvalues[1])

        for attr in products: # This part will generate input files for reactants and products
            filename=attr[0]
            template=attr[2]
            basename=attr[1]
            inp = Input(filename, basename, inCounter, template, newDict)
            
            # =(self.filename, self.basename, inCounter, self.template, newDict)
            
            ## newDict is the dictionary we want to implement.
            ## self.template is a string of the lines of the user input
            ##untill the first **** line.
            
            rvalues = inp.modify()
            """ This meathod creates a new input file and return a list of 3 or 2 organs:
                1) The dictionary that pulled to the new file.
                2) The name of the new file.
                3) String of the lines of the user input file untill the first **** line.
                * If it is not the first run, organ 3 dissmissed.
            """
            prodFiles.append(rvalues[1])
            
        gener=generatorReac(reacFiles,prodFiles,DIST,newDict)
        print '\n\n'+str(inCounter)+'  '+str(gener.gradeTemp)+'\n\n'
        newDict=gener.generateTemp()

#        gener.getBestDict() # Printing the debugging row.
        inCounter +=1    
        del inp # Deletion our object in order to not take memory space while running Gaussian.
    '''
    #Time to acheive the most far dictionaries:
    
    maxx=sorted([rms for rms in [rmsd(*dicts) for dicts in [(dictionaries[i],dictionaries[j])for ])
    for idxx in range(FILENOTEMP):
        for jdxx in range(FILENOTEMP):
    '''
           
           
    # Untill here we needed for generating "temp".
    # There is no need to return the temp since it re-produces in each iterarion of generate..

def generate(reactants,products,globalDict):
    ###########################################################################
    ####### Here is the main loop for the best set of parameters search:#######
    global inCounter, gener
    #inCounter is the main file number that added to the file. Gener must be global too so that this function can use its methods before instatiate one 

    print '\nThis part is about to calculate the best set of parameters'
    oldDict=newDict=gener.getBestDict().copy()
    for DIST in (0.001,0.0001,0.00001): # This DIST determines the step size
        
        for chooseYes in (0.45,0.35,0.25,0.2,0.1):
            oldDict=newDict=gener.getBestDict().copy()
            print '\n\nBest:  %s\n\n'%gener.best[1]
            meanDeltaE=gener.getMeanDeltaE() #meanDeltaE is the float DeltaE that is inside "temp"
            print '\nMeanDeltaE'+str(meanDeltaE)
            
            temp=(-meanDeltaE/log(0.5)) # Temperature declaration
            print str(temp)+" This is the temp\n"
            print 'temp:',temp
            for runss in range(FILENO): # Here we care that number of files will not exceed FILENO for each iteration
                reacFiles,prodFiles=[],[]
                for attr in reactants: # This part will generate input files for reactants and products
                    filename=attr[0]
                    template=attr[2]
                    basename=attr[1]
                    inp = Input(filename, basename, inCounter, template, newDict)
                    
                    # =(self.filename, self.basename, inCounter, self.template, newDict)
                    
                    ## newDict is the dictionary we want to implement.
                    ## self.template is a string of the lines of the user input file untill the first **** line.
                    
                    rvalues = inp.modify()
                    """ This meathod creates a new input file and return a list of 3 or 2 organs:
                        1) The dictionary that pulled to the new file.
                        2) The name of the new file.
                        3) String of the lines of the user input file untill the first **** line.
                        * If it is not the first run, organ 3 dissmissed.
                    """
                    reacFiles.append(rvalues[1])

                for attr in products: # This part will generate input files for reactants and products
                    filename=attr[0]
                    template=attr[2]
                    basename=attr[1]
                    inp = Input(filename, basename, inCounter, template, newDict)
                    
                    # =(self.filename, self.basename, inCounter, self.template, newDict)
                    
                    ## newDict is the dictionary we want to implement.
                    ## self.template is a string of the lines of the user input file untill the first **** line.
                    
                    rvalues = inp.modify()
                    """ This meathod creates a new input file and return a list of 3 or 2 organs:
                        1) The dictionary that pulled to the new file.
                        2) The name of the new file.
                        3) String of the lines of the user input file untill the first **** line.
                        * If it is not the first run, organ 3 dissmissed.
                    """
                    prodFiles.append(rvalues[1])

                gener=generatorReac(reacFiles,prodFiles,DIST,newDict)
                newDict=gener.generate(newDict,oldDict,DIST,temp,chooseYes)                    
                if gener.got:
                    oldDict = rvalues[0] #it is the newdict before it was changed. The new newdict will pass verification in the next iteration.
                print 'TEST: %s, %s, %s, inCounter:%s Gap: %s Temp: %s'%(DIST, chooseYes, runss, inCounter,gener.grade[-1],temp)                                     
                inCounter += 1 
                
                del inp # Deletion our object for not taking memory space while running Gaussian.
    print gener #Printing the results!!
    
        
def appendFiles(nameList,fileList):
    """
    This function appends the nameList to the fileList:
    1) Checks that the file is in the directory
    2) if not, it tries to append the root directory
    3) else, it prints an error massage
    """
    for filename in nameList:
        filename=os.path.expanduser(filename)
        split=filename.split('/')
        if len (split)>1:
            if split[0]=='':
                
                if os.path.exists(filename): 
                     fileList.append(filename)
                else:   # The full path is not correct
                    print "\nERROR: File does not exist in path: %s, aborting" % filename
                    exit()
            else: # We got the full path without "/"
                abspath = "".join(['/', filename])
                if os.path.exists(abspath):
                     fileList.append(abspath)
                else: 
                    abspath = "".join([os.getcwd(), '/', filename]) # Join the current path to filename
                    if os.path.exists(abspath):
                        fileList.append(abspath)
                    else:
                        print "\nERROR: file does not exists in path or path is not correct: %s, aborting" % filename
                        exit()
        else:  # We got just the filename without any folder info
            abspath = "".join([os.getcwd(), '/', filename]) # Join the current path to filename
            if os.path.exists(abspath):
                fileList.append(abspath)
            else:
                print "ERROR: file does not exists in path: %s, aborting" % abspath
                exit()


if __name__=="__main__":
    start_time = time.time()
    try:
        commands=open('PREFFERENCES.txt','rU')
    except:
        
        print 'ERROR: Cannot open: PREFFERENCES.txt file. Exiting!\n'
        exit(0)
    lines=commands.readlines()
    countLine=0
    while not re.search(r'^Reactants:'.lower(), lines[countLine].lower()): countLine+=1 #Looking for 'Reactants'
    countLine+=1
    while not re.search(r'\S', lines[countLine]): countLine+=1 #Empty lines between the reactants and the line: 'Reactants'
    reacStart=countLine    #Start reactants
    while not re.search(r'^Products:'.lower(), lines[countLine].lower()): countLine+=1
    prodStart=countLine #contemporarry!
    countLine-=1
    while not re.search(r'\S', lines[countLine]): countLine-=1 #Empty lines
    reacEnd=countLine+1
    countLine=prodStart+1 #Here may be an empty lines.
    while not re.search(r'\S', lines[countLine]): countLine+=1 #Empty lines
    prodStart=countLine
    while  re.search(r'\S', lines[countLine]): countLine+=1 #Products lines
    prodEnd=countLine
    while not re.search(r'^Traits:'.lower(), lines[countLine].lower()): countLine+=1
    countLine+=1
    while not re.search(r'\S', lines[countLine]): countLine+=1 #Empty lines
    traitsStart=countLine
    while countLine<len(lines) and re.search(r'\S',lines[countLine]): countLine+=1 #Traits lines
    traitsEnd=countLine
    
       #prodLine=countLine-1 #End of reactants
    try:
        reactants=[re.search(r'\S+\.\S+',line).group() for line in lines[reacStart:reacEnd]]
        products= [re.search(r'\S+\.\S+',line).group() for line in lines[prodStart:prodEnd]]        

        #These contain also the stochiometry of any file in the reacion:
        reacStoich=[re.findall(r' +\d+',line) for line in lines[reacStart:reacEnd]] #The numbers after reactant name
        prodStoich=[re.findall(r' +\d+',line) for line in lines[prodStart:prodEnd]] #The numbers after product name
        for i in range(len(reacStoich)):
            reacStoich[i]=[int(reac) for reac in reacStoich[i]]
        for i in range(len(prodStoich)):
            prodStoich[i]=[int(prod) for prod in prodStoich[i]]

        traits= [[re.search(r'\S+\s*=\s*\S+\s+\S',line).group().split('=')[0]]+re.search(r'\S+\s*=\s*\S+\s+\S+',line).group().split('=')[1].split() for line in lines[traitsStart:traitsEnd]]
        traits= [[trait[0].strip(),float(trait[1].strip()),float(trait[2].strip())] for trait in traits]
        # trait now are for instance: [[trait name, weight, value],...]
        print 'These are the traits to optimize by:\n',traits
    except:
        raise
        print '\n\n Problem is in input files of products and reactants. fix it!    :-)'
    print reactants,'\n',products
    reacFiles,prodFiles=[],[] #lists of reactants and products file names. 

    
    appendFiles(reactants,reacFiles) # This function verifies that each file is exist and appends it to reacFiles
    appendFiles(products ,prodFiles) # This function verifies that each file is exist and appends it to prodFiles
    # Creation of the first input file
    reactants= [handleFile0(reac) for reac in reacFiles]
    products = [handleFile0(prod) for prod in prodFiles]
    #reactants & products are a list of lists. Inner list has the structure:
    #[ name of new file(filename),template of file,basename,dictionary of this file]
    inCounter+=1 # since we did all the new files, it should be increased also.

    #This about merge all the dictionaries in the reactants and products files to one globalDict:
    globalDict=reactants[0][3] #the dictionary of the first file. globalDict is the dictionary that will be used in the minimization process
    for mol in reactants[1:]+products:
        for atom in mol[3].keys(): # The dictionary
            if atom not in globalDict.keys():
                globalDict[atom]=mol[3][atom]

    #Tis row assigning the error object to the errorHand name in the class generatorReac:      
    generatorReac.errorHand=error.errorFunction(traits,reacStoich,prodStoich)         
    temp=tempGener(reactants,products,globalDict)
    generate(reactants,products,globalDict)
    print time.time() - start_time, "seconds"

    

    

 
        
            
            
