import sys
a=open(sys.argv[1],'rw')
b=open(sys.argv[2],'w')
for line in a.readlines():
    if '~/error_function' in line or '0+0k 0+0io' in line:
        pass
    else:
        b.write(line)

a.close()
b.close()

