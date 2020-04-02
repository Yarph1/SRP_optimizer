from Input import Input
import os,sys,time
from math import log
from generatorSingle import generatorSingle

FILENO = 4
FILENOTEMP=5

def whoami():
    return __file__

class Main(object):

    
    def __init__(self, filename):

        """ Constructor for the main class of the program
            Proccessing input line is in the end of this file,
            to achieve the right naming as "filename"
        """
        self.filename = filename

        # ?? Filename except the '.inp' taking in account the option for another '.' in filename:
        self.basename = ".".join(filename.split('/')[-1].split('.')[:-1])  
        if not os.path.exists("".join([os.getcwd(), '/Optimizer'])): # we need this folder to put the output files
            os.mkdir("".join([os.getcwd(), '/Optimizer']))
        else:
            pass
        self.template = "" 
        
    def main(self):
        inCounter = 0 # Count the optimizations rounds.
        # The main loop of the program:

        if inCounter == 0: # First run
            print self.basename
            inp = Input(self.filename, self.basename, inCounter) # Initializing an object of Input module
            #gener will run the self.filename in Gaussian & will generated a new dict
            gener=generatorSingle()
            rvalues = inp.modify()
            olddict = rvalues[0].copy()
            self.filename = rvalues[1]
            newdict = olddict
            self.template = rvalues[2]
            inCounter+=1


        #this part is about generating the temperature:
        print '\n\n\nThis part is about generating the DeltaE to take temp=(-deltaE/ln(1-[acceptance fraction]))\n\n'
        for idxx in range(FILENOTEMP):
            inp = Input(self.filename, self.basename, inCounter, self.template, newdict)
            ## newdict is the dictionary we want to implement.
            ## self.template is a string of the lines of the user input file untill the first **** line.
            rvalues = inp.modify()
            """ This meathod creates a new input file and return a list of 3 or 2 organs:
                1) The dictionary that pulled to the new file.
                2) The name of the new file.
                3) String of the lines of the user input file untill the first **** line.
                * If it is not the first run, organ 3 dissmissed.
            """
            
            self.filename = rvalues[1]
            DIST=0.001 #Long step for arbitrary search for the mean.
            print '\n\n'+str(inCounter)+'  '+str(gener.gradeTemp)+'\n\n'
            newdict=gener.generateTemp(self.filename,newdict,DIST)
            
            gener.getBestDict()
            inCounter += 1 
            del inp # Deletion our object for not taking memory space while running Gaussian. 
        # Untill here we needed to generate "temp" by generating the DeltaE in Generator class.
        #This DeltaE can be used to generate temp in any stage of the job. 

        #######################################################################
        ####### Here is the main loop for best set of parameters search:#######
        print '\nThis part is about to calculate the best set of parameters' 
        for DIST in (0.001,0.0001,0.00001): # This DIST determines the step size
           
            for chooseYes in (0.45,0.35,0.25,0.2,0.1):
                olddict=newdict=gener.getBestDict()
                print '\n\nBest:  %s\n\n'%gener.best[1]
                meanDeltaE=gener.getMeanDeltaE() #meanDeltaE is the float DeltaE that is inside "temp"
                print '\nMeanDeltaE'+str(meanDeltaE)
                
                temp=(-meanDeltaE/log(1-chooseYes))
                print 'temp:',temp
                for runss in range(FILENO): # Here we care that number of files will not exceed FILENO.
                    inp = Input(self.filename, self.basename, inCounter, self.template, newdict.copy())
                    

                    ## newdict is the dictionary we want to implement.
                    ## self.template is a string of the lines of the user input file untill the first **** line.

                    rvalues = inp.modify()
                    """ This 2meathod creates a new input file and return a list of 3 or 2 organs:
                        1) The dictionary that pulled to the new file.
                        2) The name of the new file.
                        3) String of the lines of the user input file untill the first **** line.
                        * If it is not the first run, organ 3 dissmissed.
                    """
                    
                    self.filename = rvalues[1]

                    #gener will run the self.filename in Gaussian & will generated a new dict
                    newdict=gener.generate(self.filename, newdict,olddict,DIST,temp,chooseYes).copy()                    
                    if gener.got:
                        olddict = rvalues[0].copy()
                    print 'TEST: %s %s %s %s %s Gap: %s Temp: %s'%(DIST, chooseYes, runss, inCounter,self.filename,gener.grade[-1],temp)                                     
                    inCounter += 1 
                    
                    del inp # Deletion our object for not taking memory space while running Gaussian.
        print gener
                    
if __name__ == "__main__": # we called the optimizer in the command line
    start_time = time.time()
    try:
        sys.argv.extend(['input/CO2_AM1_SRP_FDH.02.inp'])
        filename = sys.argv[1]
    except IndexError:
        print ('No File Name After The Command \n Exiting')
        exit(0)
    if len(filename.split('/')) > 1: # ?? >=
        if filename.split('/')[0] == '':# user gave us full path 
            if os.path.exists(filename): 
                inst = Main(filename)
                inst.main() # ??
            else:   # The full path is not correct
                print "ERROR: File does not exist in path: %s, aborting" % filename
        else: # We got the full path without "/"
            if os.path.exists("".join(['/', filename])):
                abspath = "".join(['/', filename])
                inst = Main(abspath)
                inst.main()
            else: 
                abspath = "".join([os.getcwd(), '/', filename]) # Join the current path to filename
                if os.path.exists(abspath):
                    inst = Main(abspath)
                    inst.main()
                else:
                    print "ERROR: file does not exists in path: %s, aborting" % abspath
    else:  # We got just the filename without any folder info
        abspath = "".join([os.getcwd(), '/', filename])
        if os.path.exists(abspath):
            inst = Main(abspath)
            inst.main()
        else:
            print "ERROR: file does not exists in path: %s, aborting" % abspath
    print time.time() - start_time, "seconds"
