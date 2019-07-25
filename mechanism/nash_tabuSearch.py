# Created by Thanh C. Le at 7/24/19
import sys
from queue import Queue

import numpy as np

class Individual:

    def __init__(self,problem,representation,init = True,):
        self.problem = problem
        self.representation = representation
        self.time_fitness = sys.maxsize
        self.salary_fitness = sys.maxsize
        if init:
            self.representation = self.generate_representation()
        self.time_fitness = self.computeFitness(0)
        self.salary_fitness = self.computeFitness(1)

    def generate_representation(self):
        return self.problem.generate_genotype()

    def updateFitness(self,x):
        self.fitness = x

    def getFitness(self,type=0):
        if type == 0:
            return self.time_fitness
        if type == 1:
            return self.salary_fitness
    def computeFitness(self,type=0):
        if type == 0:
            return self.problem.computeTotalTime(self.representation)
        if type == 1:
            return self.problem.computeSalary(self.representation)

    def neighborhood(self,num_neighbor,type=0):
        dict = {}
        for i in range(num_neighbor):
            neighbor = self.findNeighbor(type)
            dict[i] = Individual(self.problem,neighbor,False)
        return dict

    def findNeighbor(self,type=0):
        size = self.problem.num_project * self.problem.num_task
        gen = np.copy(self.representation)
        pivot1 = np.random.randint(0, size)
        pivot2 = np.random.randint(0, size)
        if pivot1 > pivot2:
            pivot1, pivot2 = pivot2, pivot1
        if type == 0:
            gen[pivot1:pivot2] = self.representation[pivot1 + 1:pivot2 + 1]
            gen[pivot2] = self.representation[pivot1]
            gen[size + pivot1:size + pivot2] = self.representation[size + pivot1 + 1:size + pivot2 + 1]
            gen[size + pivot2] = self.representation[size + pivot1]
        if type == 1:
            rand = np.random.rand()
            if rand < 0.5:
                gen[size + pivot2] = self.representation[size + pivot1]
                gen[size + pivot1] = self.representation[size + pivot2]
            else:
                gen[size + pivot1] = \
                    np.random.choice(self.problem.num_staff, p=self.problem.probs[:, self.representation[pivot1]])


        return gen

class TabuSearch:
    def __init__(self,problem):
        self.problem = problem
        self.candidate = Individual(problem,[],True)
        self.paretoSet = []
        self.paretoSet.append(Individual(problem,np.copy(self.candidate.representation),False))
        self.TabuList = {}
        self.TabuIndex = 0
        self.add2TabuList(self.candidate)

    def isDominate(self,ind1,ind2):
        result = -1
        if ind1.getFitness(0) <= ind2.getFitness(0):
            result += 1
        if ind1.getFitness(1) <= ind2.getFitness(1):
            result += 1
        return result

    def updateParetoSet(self,ind):
        newSet = []
        addOptimal = False
        deleteOptimal = False
        for best in self.paretoSet:
            if self.isDominate(ind,best) != 1:
                newSet.append(best)
            if self.isDominate(ind,best) != -1:
                addOptimal = True
            if self.isDominate(ind,best) == -1:
                deleteOptimal = True

        if not deleteOptimal:
            if addOptimal:
                newSet.append(Individual(self.problem, ind.representation, False))
        self.paretoSet = newSet


    def add2TabuList(self,ind):
        self.TabuList[self.TabuIndex] = ind
        self.TabuIndex += 1
        if self.TabuIndex == 20:
            self.TabuIndex = 0

    def search(self,num_neighbor,type=0):
        neighborhood = self.candidate.neighborhood(num_neighbor,type)
        neighborFitness = [ind.getFitness(type) for ind in neighborhood.values()]
        rank = np.argsort(neighborFitness)
        best = 0
        while (neighborhood[rank[best]] in self.TabuList):
            best += 1
        self.updateParetoSet(neighborhood[rank[best]])
        self.add2TabuList(self.candidate)
        self.candidate = neighborhood[rank[best]]










