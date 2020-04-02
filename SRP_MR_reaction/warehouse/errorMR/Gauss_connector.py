import os,sys

class Gaussian_connector(object):
    def __init__(self):
        pass
    def runner(self,filename):
        #a=os.popen('peep')
        basename=os.path.basename(filename).split('.gjf')[0]
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
            os.system('pushd %s ; xrg09y %s ; popd'%(os.path.dirname(filename),'.'.join(basename.split('.')[:-1])))
        else:
            os.system('pushd %s ; xrg09y %s ; popd'%(os.path.dirname(filename),basename))

        return open('.'.join(filename.split('.')[:-1])+'.out')








if __name__=="__main__":
    foo=Gaussian_connector()
    foo.runner(sys.argv[1])
