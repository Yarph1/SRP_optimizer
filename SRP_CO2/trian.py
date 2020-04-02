import random
for i in range(100):
  numberOfDictsInNextGen=int(random.gauss(2,3)) #Edit! 2 is the mean of the gaussian distribution
  if numberOfDictsInNextGen == 0:
      numberOfDictsInNextGen=2
  elif numberOfDictsInNextGen < 0:
      numberOfDictsInNextGen=abs(numberOfDictsInNextGen)+1
  print(numberOfDictsInNextGen)
