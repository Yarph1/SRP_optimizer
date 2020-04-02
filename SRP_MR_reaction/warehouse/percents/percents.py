import AtomsParser
"""
This file creates a csv containing all the parameters so
the user can add percents to the changing range.
"""

results = AtomsParser.parser()
filer = open('percents.csv', 'w')
for item in sorted(results.iterkeys()):
    filer.write('\n%s\n\n' % item)
    for tupl in results[item]:
        filer.write('%s,\n' % tupl[0])


filer.close()
