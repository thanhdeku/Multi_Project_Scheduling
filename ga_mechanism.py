# Created by Thanh C. Le at 7/19/19
# Genetic algorithm mechanism for single task
import sys

from data import createData
from problem import MultiProjectScheduling

import numpy as np

class Crossover:
    def randomTwoPivot(self,size):
        start_pivot = np.random.randint(0,size-1)
        end_pivot = np.random.randint(start_pivot+1,size)
        return start_pivot, end_pivot

    def pmx(self,ind1,ind2,start_pivot,end_pivot):

        size = min(len(ind1), len(ind2))
        p1, p2 = np.zeros(size,dtype=int), np.zeros(size,dtype=int)

        # Initialize the position of each indices in the individuals
        for i in range(size):
            p1[ind1[i]] = i
            p2[ind2[i]] = i

        off1 = np.copy(ind1)
        off2 = np.copy(ind2)
        # Apply crossover between cx points
        for i in range(start_pivot, end_pivot):
            # Keep track of the selected values
            # Swap the matched value
            off1[i], off1[p1[ind2[i]]] = ind2[i], ind1[i]
            off2[i], off2[p2[ind1[i]]] = ind1[i], ind2[i]
            # Position bookkeeping
            p1[ind1[i]], p1[ind2[i]] = p1[ind2[i]], p1[ind1[i]]
            p2[ind1[i]], p2[ind2[i]] = p2[ind2[i]], p2[ind1[i]]

        return off1, off2

    def cxTwoPoint(self,ind1,ind2,start_pivot,end_pivot):
        size = min(len(ind1),len(ind2))
        off1 = np.copy(ind1)
        off2 = np.copy(ind2)
        off1[start_pivot:end_pivot] = ind2[start_pivot:end_pivot]
        off2[start_pivot:end_pivot] = ind1[start_pivot:end_pivot]

        return off1, off2


class Mutation:

    def randomMutation(self,ind,num_of_mutation):
        size = int(len(ind)/2)
        for i in range(num_of_mutation):
            first_point = np.random.randint(0, size)
            second_point = np.random.randint(0, size)
            while second_point == first_point:
                second_point = np.random.randint(0, size)
            temp1 = ind[first_point]
            temp2 = ind[second_point]
            ind[first_point] = temp2
            ind[second_point] = temp1
            temp1 = ind[first_point+size]
            temp2 = ind[second_point+size]
            ind[first_point+size] = temp2
            ind[second_point+size] = temp1
        return ind

class Population:
    def __init__(self,size,problem,init = True):
        self.size = size
        self.problem = problem
        self.pop = np.array([])
        self.popFitness = np.array([])
        self.max = False
        if init:
            self.pop, self.popFitness = self.generate_population()
    def generate_population(self):
        pop = []
        popFitness = []
        for i in range(self.size):
            chrome = Individual(self.problem)
            pop.append(chrome)
            popFitness.append(chrome.fitness)
        return np.array(pop), np.array(popFitness)

    def get(self,index):
        return self.pop[index]
    def top_fitness(self,size):
        if self.max:
            return np.argpartition(self.popFitness, -size)[-size:]
        else:
            return np.argpartition(self.popFitness, size)[:size]

    def best_individual(self):
        if self.max:
            return np.argmax(self.popFitness)
        else:
            return np.argmin(self.popFitness)


    def addIndividual(self,individual):
        self.pop = np.append(self.pop,individual)
        self.popFitness = np.append(self.popFitness,individual.fitness)

    def addPopulation(self,population):
        self.pop = np.concatenate(self.pop,population)
        self.popFitness = np.concatenate(self.popFitness,population.popFitness)

    def naturalSelection(self,size):
        index = self.top_fitness(size)
        self.pop = self.pop[index]
        self.popFitness = self.popFitness[index]
    def parentSelection(self,num_of_pairs,type='roulette'):
        dict = {}
        if type == 'roulette':
            sumFitness = np.sum(self.popFitness)
            probs = self.popFitness/sumFitness
            for i in range(num_of_pairs):
                dict[i] = (self.roulette(probs),self.roulette(probs))
        if type == 'tournament':
            for i in range(num_of_pairs):
                dict[i] = (self.tournament(2), self.tournament(2))
        return dict

    def tournament(self,k=2):
        best = np.random.randint(0,self.size)
        for i in range(k-1):
            new = np.random.randint(0,self.size)
            if self.max:
                if self.popFitness[best] < self.popFitness[new]:
                    best = new
            else:
                if self.popFitness[best] > self.popFitness[new]:
                    best = new
        return best

    def roulette(self,probs):
        sum = 0
        rand = np.random.rand()
        index = 0
        while (rand > sum):
            sum += probs[index]
            index += 1
        return index-1
class Individual:

    def __init__(self,problem,representation=-1,init = True,):
        self.problem = problem
        self.representation = representation
        self.fitness = sys.maxsize
        if init:
            self.representation = self.generate_representation()
        self.fitness = self.problem.computeFitness(self.representation)
    def generate_representation(self):
        return self.problem.generate_genotype()

    def updateFitness(self,x):
        self.fitness = x

def test():
    # data = createData()
    # problem = MultiProjectScheduling(data)
    # pop = Population(5,problem)
    # print(pop.parentSelection(5,'tournament'))
    # x = np.random.permutation(5)
    # y = np.array([1,1,2,3,1])
    # z = np.concatenate((x,y))
    # print(z)
    # mutation = Mutation()
    # print(mutation.randomMutation(z,3))
    pass


test()