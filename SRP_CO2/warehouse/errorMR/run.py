import sys,os,commands,subprocess, time
class longRunner (object):
     def emptPercent(self,station):

          return 100.0-float(str(subprocess.check_output(['peepL', 'quanta%s'%station])).split()[4][:-1])

     def getEmptyCores(self,station):
            out=self.emptPercent(station)
            i=int(station)
            if i<=24:
                    empty=out*(8.0/100)
            if i==24:
                    
                    empty=0.5*empty
            elif i>24 and i< 29:
                    empty=out* (12.0/100)
            elif i==29:
                    empty=out*(16.0/100)

            empty = round (empty)
            return int(empty)
     def isConnection(self,station):          
             return subprocess.call(['nc', '-z', 'quanta%s'%(station), '22', '-w', '2'],stdout=self.nul) #checks connection  to server 

     
          
     def run(self,cores,command,excludes=[],background=False):
          
          self.nul=open("/dev/null")  # Good place to through errors
          out=0.0

          for i in range (29,24,-1)+range(1,25):
                 if i in excludes:
                      continue
                 if i in range(1,10): # to make quanta1 to quanta01 etc
                         station=str(0)+str(i)
                 else:
                      station=str(i)
                 todo=self.isConnection(station)
                 runn=False
                 try:
                      if not todo: #there is connection
                      
                           out=self.emptPercent(station)
                      else:
                           continue
                      empty= self.getEmptyCores(station)

                      time.sleep(0.01)
                 
                      if cores<=empty:
                           time.sleep(0.2)
                           if cores<=self.getEmptyCores(station):
                                   time.sleep(0.2)
                                   if cores<=self.getEmptyCores(station):
                                           runn=True
                      else:
                           runn=False
                 except:
                      
                      continue
                         
                 
                 print 'quanta',station,'  ','empty cores: ',empty, ', running= ', runn

                 if runn:
                       #print '\n'
                       #print ('ssh quanta%s'%(i)+' \"'+' '.join(command)+'\"')
                       print 'running on quanta%s'%station
                       folder=os.getcwd()
                       if background:
                            subprocess.Popen(['ssh', 'quanta%s'%(station),'cd',folder,';']+command,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                       else:
                            subprocess.call(['ssh', 'quanta%s'%(station),'cd',folder,';']+command)
                                                                         
                       return runn
          return runn

if __name__=="__main__":
     
     try:
      
        cores=sys.argv[1] # number of cores needed
        cores =int(cores)
     except:
         print'Use this code: type number of cores and than the command'
         print 'for example: run 4 runqc g09 ...'


         print 'The first argument must be the number of cores! Exiting...'
         exit(0)
     if cores<1 or cores>10:
         print'Use this code: type number of cores and than the command'
         print 'for example: run 4 runqc g09 ...'
         print 'The first argument must be the number of cores between 1 and 10! Exiting...'
         exit(0)

     if len(sys.argv)<3:
         print 'No command given, exiting.'
         print'Use this code: type number of cores and than the command'
         print 'for example: run 4 runqc g09 ...'
         exit(0)

     if raw_input( "\nDo you wish to run your job in background? (y/n) ") in ['y','yes','background']:
          background=True
          #sys.argv.append('&')
     else:
          background=False
     
     excludes=[]
     if raw_input('Do you wish to NOT run on specific quanta stations? (y,n) ') in ['yes','y']:
          goodEx=False
          while not goodEx:
               try:
                    excludes=[int(ex) for ex in raw_input('\nPlease type station numbers to exclude divided by comma (example: 3,19,20)   ').split(',')]
               except ValueError:
                    print '\nNo station number with commas inserted '
                    continue
               goodEx= True
     if not longRunner().run(cores,sys.argv[2:],excludes,background):
          if raw_input('Quantas are full. Do you want me to check any 20 minutes until your job can run? (y,n)  ') in ['y','yes']:
               print ('\nThis code will check avery 20 minutes if there is an empty place.\n\nDo not close it. \nTo continue working please connect to another putty shell\n Waiting...')
               time.sleep(12)
               while not longRunner().run(cores,sys.argv[2:],excludes,background):
                    time.sleep(12)
          else:
               print ('Quanta full. The job didn\'t run')
     else:
          print 'successfully run your job!'
     
