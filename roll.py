import random
import re

def roll_(dice):
        
        # split on the "d" into two elements
        d = dice.split('d')

        # remove any non-digit characters from either element
        for i in range(len(d)):
            d[i] = re.sub('\D', '', d[i])
        
        # make it work with non-numeric entries (had a problem with entering "d20" and it using an emtpy string from before the d)
        d = [x for x in d if x.isdigit()]
        d = [int(x) for x in d]

        # roll all of the dice and add up the score
        rollTotal = 0
        i = 0
        while True:
            if len(d) == 1:
                roll = random.randrange(1, d[0]+1)
                rollTotal += roll
                break
            roll = random.randrange(1, d[1]+1)
            rollTotal += roll
            i += 1
            if i == d[0]:
                break
        
        return rollTotal

