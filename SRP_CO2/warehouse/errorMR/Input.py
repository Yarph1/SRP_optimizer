import os
import re
import sys
import AtomsParser

class Input(object):
    """
    Class for building and hanling input files.
    
    """
    
    def __init__(self,filename, project, index = 0, template = "", localdict = ""):

        """
        If we are in the first run, than we get an empty template. The template will built with standard parameters, as for the localdict.

        """
        
        self.index = index
        if index == 0: # First Run.
            if not os.path.exists('GaussFiles'):
                os.mkdir('GaussFiles')
            project= 'GaussFiles/'+project
            if not os.path.exists(project):
                os.mkdir(project)

            # Elements will be a dictionary of tupples.Keys=atoms, values=parameters:    
            self.elements = AtomsParser.parser() 
            
            #Creating the first new file:
            if len(os.path.basename(filename).split('.inp'))>1:
                self.newfile = open("".join([os.getcwd(), '/', project, '/', os.path.basename(filename).split('.inp')[0] , '_%s.gjf' % str(index)]), 'w')
            elif len(os.path.basename(filename).split('.gjf'))>1:
                self.newfile = open("".join([os.getcwd(), '/', project, '/', os.path.basename(filename).split('.gjf')[0] , '_%s.gjf' % str(index)]), 'w')
            else:
                print 'This program works with \'gjf\' or \'inp\' Gaussian files.'
                sys.exit(0)
                
                
            # Opens the user input file:
            self.filename = open(filename, 'r')
        
        else: # It isn't the first run
            project= 'GaussFiles/'+project
            # Create the new file name:
            filen = "".join([os.getcwd(), '/', project, '/', '_'.join(os.path.basename(filename).split('_')[:-1]), '_', str(self.index) , '.gjf'])

            # Opens the new file:
            self.newfile = open(filen, 'w')

            # Opens the old file:
            self.filename = open(filename, 'r')
            # Takes the old di
            self.template = template
            ## self.template is a string of the lines of the user input file untill the first **** line.
            self.localdict = localdict
            ## localdict will be a dict of lists. Any list contains lists with first organ- parameter name, second- its value.
        

    def modify(self):
        """
        Creates the new input file.
        """
        if self.index == 0:
            # Have to take the parameters from the user to the standard self.elements:
            contents = self.filename.readlines()
            self.filename.close()
            # Parsing the user file for Parameters:
            localdict=inparse(contents) # Contents is the lines of the user file.
## localdict is a dict of lists. Any list contains lists with first organ- parameter name, second- its value.

## now localdict have the dictionary from the user file, and we want to add to it the standard parameters
            for item in localdict:
                # This line will add to specific atom the standard params that not exist in the user input.
                # comparedict returns list with existing user parameters and not existing standard ones.
                localdict[item] = self.comparedicts(localdict[item], item)
                # localdict complited..

# writes a string contains the all lines require to the new input file "self.newfile" into it, and close it:
            self.new_input(localdict, contents) 
            return (localdict, self.newfile.name, self.template)
        ## self.newfile.name is the name of the new input file created 2 lines above, and template is the
        ## file without the parameters lines with one **** line.
        else:
            self.new_input(self.localdict, self.template) # ? why self??
            return [self.localdict, self.newfile.name]
        
    def new_input(self, localdict, contents): ##FINISH THIS##
        if self.index == 0:
            idx = contents.index(contents[-1]) + 1 # last line index

# looks for the first **** line. if no such line, idx is the end of the file:
            for line in contents: 
                if re.match('(\s\*\*\*\*)', line):
                    idx = contents.index(line)
                    break
                else:
                    pass
            template = "".join(contents[:idx]) # template is all lines till idx.
            part = "****\n"
            self.template = template
            self.template = "".join([self.template, part])
            for atom in localdict: # atom is a key.
                part = "".join([part, '%s\n' % atom]) 
                for item in localdict[atom]:
                    part = "".join([part, '%s=%s\n' % (item[0], item[1])]) # part is growing.
                part = "".join([part, '****\n']) # end of this atom
            template = "".join([template, part]) # now template conatin the parameters.
        else:
        ##FINISH THIS##
            part = ''
            #print localdict.keys()
            for atom in localdict:
                
                part = "".join([part, '%s\n' % atom])
                for item in localdict[atom]:
                    part = "".join([part, '%s=%s\n' % (item[0], item[1])])
                part = "".join([part, '****\n'])
                
            template = "".join([self.template, part])
        self.newfile.write(template)
        # template is a string of all the lines of the new input file.
        self.newfile.close()
        
    def comparedicts(self, params, atom):
## params is list, of lists of dimenssion 2 that its first value is param name
## and secon param value. atom is the key for the list of params.
        local = [tupl[0] for tupl in params]

# This line search for standard parameters for the specific atom that are not in the user input:
        missing = filter((lambda x : x[0] not in local), self.elements[atom])
        """
            filter(function, iterable): 
            Construct a list from those elements of iterable for which function returns true.
            Here x[0] is the parameter name.
        """
        params.extend(missing) # Add the missing parameters.
        return params 
        # params= (parameters from user file) + (standard parameters missing from user file)

        
def inparse(contents): # Contents is the lines of the user file.
        atomsdict = {}
        flag=0
# Flag is the empty lines passed from the start of input file. We look for 3 empty lines.
        atoms_start = 2
        atoms_end = -1
        for line in contents:
            """ For any line we check if there is organ that is not empty. empty is an indicator to
                to the content of the line: >1 means there is a not empty organ.
            """
            empty = 0
            atoms_end += 1 
            # Any not blunk in the line, means find something.
            for item in re.findall('(\S*)', line):
                if len(item) > 0: # We found somthing.
                    empty += 1
                else:
                    pass
            if not empty: # Means empty == 0.
                flag += 1
            else:
                pass
            if flag == 2:
                pass
            elif flag == 3:
                break
            else:
                atoms_start += 1 # Now equal 2+ number of lines until flag==3. 2 for method and **** lines.
        for line in contents[atoms_start:atoms_end]: #?? atoms_end ??
            for item in re.findall('(\S*)', line):
                if len(item) > 0:
                    if len(item) == 1:
                    #  If we deal Cl or 2 chars atom name, it will be fixed in fetchparams method.
                        if item[0] in atomsdict.keys(): # This atom apears 2 times.
                            pass
                        else:
                            atomsdict[item[0]] = []
                    else:
                        pass
        atomsdict = fetchparams(atomsdict, contents) 
        return atomsdict
# atomsdict is a dict of lists. Any list contains list with first organ- parameter name, second- its value.

def fetchparams(atomsdict, contents):
        fields = []
        subs = []
        idx = 0 # idx count lines.
        for line in contents:
            if re.match('(\s\*\*\*\*)', line):
                fields.append(idx) # Line number for ****.
            else:
                pass
            idx += 1 # Moves a line.
        if len(fields) > 0:
            for field in fields:
                try:
                    start = field # Line of ****
                    end = fields[fields.index(field) + 1] # next line of ****
                    subcontent = contents[start+1:end] 
                    subs.append(subcontent)
                except IndexError: #Last field do not have index+1.
                    pass
            for sub in subs: # subs is now a list of list of lines.

# sub[0] is the first line in the interval between 2 **** lines, contain the atom sign.
                atomsdict[re.search('\S', sub[0]).group(0)] = psplit(sub[1:])
        else:
            pass
        return atomsdict
# atomsdict is a dict of lists. Any list contains list with first organ- parameter name, second- its value.


def psplit(params): # params are lines, contains parameters of specific atom.
    newparams = []
    for param in params:
        newparams.extend([item for item in param.split()])
    for item in newparams:
        newparams[newparams.index(item)] = item.split('=')
        ## item is now list of 2 organs in the 2 edges of the '='.
        ## newparams is a list of these lists. 

    return newparams
                     
if __name__ == "__main__":
    foo = Input(sys.argv[1])
    foo.modify()
