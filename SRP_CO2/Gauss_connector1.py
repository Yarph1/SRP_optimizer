import os,sys,multiprocessing,run

class Gaussian_connector(multiprocessing.Process):

    def __init__(self,filename,qu):
        multiprocessing.Process.__init__(self)
        self.qu=qu
        self.filename=filename
       # print("Checking: "+str(self.filename))
        
        if not os.path.exists('output'):
            os.mkdir('output')


    def run(self):
        basename=os.path.basename(self.filename).split('.gjf')[0]
        if not os.path.exists('output/%s'%basename):
            os.mkdir('output/%s'%basename)

        #a=os.popen('peep')
        #y=open('%s/%s.'%(output/%s'%self.filename,pepp),w)
        #for line in a.readlines:
        #    y.write(line)
        
        #os.popen('pushd %s ; xrg09y %s ; popd'%(os.path.dirname(self.filename),basename))
        #print ('pushd %s ; xrg09y %s ; popd'%(os.path.dirname(self.filename),'.'.join(basename.split('.')[:-1])))
        if '.inp' in basename or '.gjf' in basename:
            #os.system('pushd %s ; xrg09y %s ; popd'%(os.path.dirname(self.filename),'.'.join(basename.split('.')[:-1])))
            while not run.longRunner().run(4,['pushd %s ; xrg09y %s ; popd'%(os.path.dirname(self.filename),'.'.join(basename.split('.')[:-1]))],range(1,10)+range(12,30)):
                pass
        else:
            #os.system('pushd %s ; xrg09y %s ; popd'%(os.path.dirname(self.filename),basename))
            while not run.longRunner().run(4,['pushd %s ; xrg09y %s ; popd'%(os.path.dirname(self.filename),basename)],range(1,10)+range(12,30)):
                pass
            
        self.qu.put('.'.join(self.filename.split('.')[:-1])+'.out')
        return








if __name__=="__main__":
    foo=Gaussian_connector()
    foo.runner(sys.argv[1])
