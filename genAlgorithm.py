# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 19:06:33 2021

@author: SHULKA RAMLAL
"""

from decimal import Decimal 
import random

class boxItems:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value


class infoClass:
    def __init__(self, maxCapacity, minValue, numBoxes):
        self.maxCapacity = maxCapacity
        self.minValue = minValue
        self.numBoxes = numBoxes

objList =[]
infoList =[]

def readtxtFile(s):
    with open(s, 'r') as f:
        f.readline()
        nextLine = True
        while nextLine:
            temp = f.readline()
            maxCap = Decimal(temp)
            temp = f.readline()
            minVal = Decimal(temp)
            temp = f.readline()
            numB = int(temp)
            infoList.append(infoClass(maxCap,minVal, numB))
        
            for line in f:
                if line.strip() != "***":
                    data = line.split()
                    objList.append(boxItems(data[0], Decimal(data[1]), Decimal(data[2])))
                else:
                    break
    return None
 

def spawn_individual():
    return [random.randint(0,1) for x in range (0,infoList[0].numBoxes)]  

def spawn_population():
    return [spawn_individual() for x in range (0,(infoList[0].numBoxes)*2)]    

def fitness(target):
    total_value = 0
    total_weight = 0
    index = 0
    for i in target:        
        if index >= (infoList[0].numBoxes):
            break
        if i == 1:
            total_value += objList[index].value
            total_weight += objList[index].weight
        index += 1

    if total_weight > infoList[0].maxCapacity:
        return 0
    if total_value < infoList[0].minValue:
        return 0
    else:
        return total_value
    
def winnerWeight(target):
    total_weight = 0
    index = 0
    for i in target:        
        if index >= (infoList[0].numBoxes):
            break
        if i == 1:
            total_weight += objList[index].weight
        index += 1

    else:
        return total_weight
    
def mutate(target):
    r = random.randint(0,len(target)-1)
    if target[r] == 1:
        target[r] = 0
    else:
        target[r] = 1
    return None
        
def evolve_population(pop):
    parent_eligibility = 0.2
    mutation_chance = 0.08
    parent_lottery = 0.05

    parent_length = int(parent_eligibility*len(pop))
    parents = pop[:parent_length]
    nonparents = pop[parent_length:]


    for np in nonparents:
        if parent_lottery > random.random():
            parents.append(np)

    # Mutate randomly 
    for p in parents:
        if mutation_chance > random.random():
            mutate(p)

    children = []
    desired_length = len(pop) - len(parents)
    while len(children) < desired_length :
        male = parents[random.randint(0,len(parents)-1)]
        female = parents[random.randint(0,len(parents)-1)] 
        geneSelector = random.randint(0,1)
        half = int(len(male)/2)
        if geneSelector == 1:
            child = male[:half] + female[half:] 
        else:
            child = female[:half] + male[half:]
        if mutation_chance > random.random():
            mutate(child)
        children.append(child)

    parents.extend(children)
    return parents


def main():
    fileName = input("Please enter the name of the file:")   
    
    if fileName.endswith(".txt"):
        file = fileName
    else:
        file = fileName+".txt"
    file = file.strip()
            
    try:
        readtxtFile(file)
    except:
        print("")
  
    numWinners = 0
    while len(infoList)>0:
        generation = 1
        population = spawn_population()
        noSolution = True
        while noSolution:
            print ("Generation %d with %d" % (generation,len(population)))
            population = sorted(population, key=lambda x: fitness(x), reverse=True)
            for i in population:        
                print ("%s, fit: %s" % (str(i), fitness(i))) 
                if fitness(i)> 0:
                    noSolution = False
            population = evolve_population(population)
            generation += 1
        
        
        print("calculating winner")
        for j in population:
            if fitness(j) > 0:
                print("")
                print("Selected winner:")
                print ("%s, value: %s, weight: %s, generation: %s" % (str(j), fitness(j), winnerWeight(j), generation))
                numWinners += 1
                break
        for x in range(infoList[0].numBoxes):
            objList.pop(0)
        infoList.pop(0)
    print("THE NUMBER OF TRUCK LOADS CALCULATED: ")
    print(numWinners)
    name = input("Press enter to exit")
          
        
if __name__ == "__main__":
    main()
