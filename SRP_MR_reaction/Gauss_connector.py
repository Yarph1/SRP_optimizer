import os,sys,multiprocessing

class Gaussian_connector(multiprocessing.Process):
    def __init__(self):
        pass

    def __init__(self,filename,qu):
        multiprocessing.Process.__init__(self)
        self.qu=qu
        self.filename=filename
       # print("Checking: "+str(self.filename))
        
        if not os.path.exists('output'):
            os.mkdir('output')


    def run(self):
        #a=os.popen('peep')
        basename=os.path.basename(self.filename).split('.gjf')[0]
        if not os.path.exists('output'):
            os.mkdir('output')

        if not os.path.exists('output/%s'%basename):
            os.mkdir('output/%s'%basename)
        #y=open('%s/%s.'%(output/%s'%filename,pepp),w)
        #for line in a.readlines:
        #    y.write(line)
        
        #os.popen('pushd %s ; xrg09y %s ; popd'%(os.path.dirname(filename),basename))
        #print ('pushd %s ; xrg09y %s ; popd'%(os.path.dirname(filename),'.'.join(basename.split('.')[:-1])))
        if '.inp' in basename or '.gjf' in basename:
            os.system('pushd %s ; xrg09y %s ; popd'%(os.path.dirname(self.filename),'.'.join(basename.split('.')[:-1])))
        else:
            os.system('pushd %s ; xrg09y %s ; popd'%(os.path.dirname(self.filename),basename))
        self.qu.put('.'.join(self.filename.split('.')[:-1])+'.out')
        #return open('.'.join(filename.split('.')[:-1])+'.out')
        return()








if __name__=="__main__":
    foo=Gaussian_connector()
    foo.runner(sys.argv[1])
