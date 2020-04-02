import re
if __name__=="__main__":
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
        traits=   [[re.search(r'\S+\s*=\s*\S+\s+\S',line).group().split('=')[0]]+re.search(r'\S+\s*=\s*\S+\s+\S+',line).group().split('=')[1].split() for line in lines[traitsStart:traitsEnd]]
        traits= [[trait[0].strip(),float(trait[1].strip()),float(trait[2].strip())] for trait in traits]
        # trait now are for instance: [[trait name, weight, value],...]
        #print traits
    except:
        raise
        print '\n\n Problem is in input files of products and reactants. fix it!    :-)'
    print reacStoich,'\n',prodStoich,'\n'
    reacFiles,prodFiles=[],[] #lists of reactants and products files
