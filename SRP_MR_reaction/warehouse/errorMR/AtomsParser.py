import re,sys
def parser():
    """
This function parses a default Gaussian output file
and returns the default parameters for every atom
    """
    filer = open("atoms1.out", 'r')
    contents = filer.readlines()
    filer.close()
    
    # dictionary that will contain the standard parameters:
    elements = {} 
    counter = 0
    idx = -1
    fields = []
    while True:
        try:
            # searching for the **** line from idx+1 and store in idx:
            idx = contents.index(" ****\n", idx+1)
            fields.append(idx)  #Saving the line number of the ****
        except ValueError: # As for the last ****, there are no **** after them, so breaking.
            break
    for field in fields: # Runing on the indexes:
        try:
        # This line takes the content from the **** that field is its index untill the next one:
            subcontent = contents[fields[fields.index(field)]+1:fields[fields.index(field)+1]]
        except IndexError: # At the last field running, there is no index+1 in fields.
            pass
        #Searches for the first[0] not blank character in the first line[0], this is the atom sign: 
        currelement = re.findall("(\S*)", subcontent[0][1:])[0]
        elements[currelement] = [] 
        for item in subcontent[1:]: # item is a line
            for param in item.split():
                # Before the '=' exist the parameter name and after the value. append as tupple. 
                elements[currelement].append((param.split('=')[0], param.split('=')[1]))
    return elements # Retun type: dictionary of tupples!


def changeParser():
#This function returns a dictionary, when any parameter get its change value at its end
# It doesn't do as it expected. It may be modified in the furture
    u=open('FirstParameters.txt','w')
    count=0
    s=parser()
    lines=open('PARAMETRS.csv','r').readlines()
    
    for parm in sorted(s):
        for whati in range(len(s[parm])):
            s[parm][whati]=s[parm][whati]+(float(lines[count][74:83]),) # extend the tupple with the fraction of the change to this parameter.

            lin=str(parm)+('  'if len(parm)==1 else ' ')+str(s[parm][whati])  #Here we log the initial parameters and their change-fraction
            while len(lin)<74:
                lin=lin+' ' # So that the 1 will be in place 74 excactly
            
            u.write(lin+'\n')
            count+=1
    u.close()
    return s
    # s is the dictionaries of list of tuples, when any tuple contain the name of parameter, its value,its change rate (by user in PARAMETERS file).

def PARAMETERS():
#That module creates a file to have a look on the parameters.
    a=open('PARAMETRS.csv','w')
    s=parser()
    for parm in sorted(s):
 
        for whati in range(len(s[parm])):
            lin=str(parm)+('  'if len(parm)==1 else ' ')+str(s[parm][whati])
            while len(lin)<74:
                lin=lin+' ' # So that the 1 will be in place 74 excactly
            
            a.write (lin+'1\n')
    a.close()
            
if __name__ == "__main__":

        if len(sys.argv)>1:     
            if sys.argv[1]=='PARAMETERS':
                PARAMETERS()
            elif sys.argv[1]=='change':
                changeParser()
            else:
                print ('To restart the parameters use argument: PARAMETERS, To apply canges in the parameters, use argument: change')

        else:
            print ('To restart the parameters use argument: PARAMETERS, To apply canges in the parameters, use argument: change')



    
                
 #       a.write(str(''.join([parm, '\n',''.join([''.join(u) for u in s[parm]]), '\n\n'])))

