# Created by Thanh C. Le at 7/25/19
import sys
import numpy as np

from data import loadData
from problem import MultiProjectScheduling


class Individual():
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

    def isDominate(self,ind):
        result = -1
        if self.getFitness(0) <= ind.getFitness(0):
            result += 1
        if self.getFitness(1) <= ind.getFitness(1):
            result += 1
        return result

class Population():
    def __init__(self, size, problem, init=True):
        self.size = size
        self.problem = problem
        self.pop = np.array([])
        if init:
            self.pop = self.generate_population()
        self.nonDominatedRank, self.nonDominatedSet = self.nonDominatedSort()
        self.crowdingDistance = self.computeCrowdingDistance()

    def nonDominatedSort(self):
        rank = np.zeros(self.size,dtype=int)
        f_nonDominate = {}
        f_nonDominate[0] = np.array([],dtype=int)
        S = {}
        N = {}
        for i in range(self.size):
            p = self.get(i)
            si = np.array([],dtype=int)
            ni = 0
            for j in range(self.size):
                if i != j:
                    q = self.get(j)
                    if p.isDominate(q) == 1:
                        si = np.append(si,j)
                    elif q.isDominate(p) == 1:
                        ni += 1
            S[i] = si
            N[i] = ni
            if ni == 0:
                f_nonDominate[0] = np.append(f_nonDominate[0],i)
        index = 0
        while(len(f_nonDominate[index]) != 0):
            Q = np.array([],dtype=int)
            for p in f_nonDominate[index]:
                for q in S[p]:
                    N[q] = N[q] - 1
                    if N[q] == 0:
                        rank[q] = index + 1
                        Q = np.append(Q,q)
            index += 1
            f_nonDominate[index] = Q
        return rank, f_nonDominate


    def computeCrowdingDistance(self):
        crowdingDistance = np.zeros(self.size)
        for f in self.nonDominatedSet.values():
            for task in range(2):
                if len(f) > 0:
                    x = [self.get(i).getFitness(task) for i in f]
                    sort = np.argsort(x)
                    crowdingDistance[f[sort[0]]] = -sys.maxsize
                    crowdingDistance[f[sort[-1]]] = -sys.maxsize
                    delta = x[sort[0]] - x[sort[-1]]
                    for j in range(1, len(f) - 1):
                        crowdingDistance[f[sort[j]]] = (x[sort[j - 1]] - x[sort[j + 1]]) / delta
        return crowdingDistance



    def generate_population(self):
        pop = []
        for i in range(self.size):
            chrome = Individual(self.problem,[])
            pop.append(chrome)
        return np.array(pop)

    def get(self, index):
        return self.pop[index]

    def addIndividual(self, individual):
        self.pop = np.append(self.pop, individual)
        self.size += 1

    def addPopulation(self, population):
        self.pop = np.concatenate((self.pop, population))
        self.size += len(population)

    def isBetter(self,ind1,ind2):
        if self.nonDominatedRank[ind1] < self.nonDominatedRank[ind2]:
            return True
        elif self.nonDominatedRank[ind1] > self.nonDominatedRank[ind2]:
            return False
        else:
            if self.crowdingDistance[ind1] > self.crowdingDistance[ind2]:
                return True
            else:
                return False
    def updateInfo(self):
        self.nonDominatedRank, self.nonDominatedSet = self.nonDominatedSort()
        self.crowdingDistance = self.computeCrowdingDistance()

    def naturalSelection(self, size):
        self.updateInfo()
        newPop = np.array([],dtype=int)
        index = 0
        length = 0
        while(length < size):
            l = len(self.nonDominatedSet[index])
            if length+ l  > size:
                break
            newPop = np.concatenate((newPop,self.nonDominatedSet[index]))
            length += l
            index += 1
        delta = size - len(newPop)

        if delta > 0:
            cw = [self.crowdingDistance[i] for i in self.nonDominatedSet[index]]
            rank = np.argsort(cw)
            newPop = np.concatenate((newPop, self.nonDominatedSet[index][rank[:-delta]]))
        self.pop = self.pop[newPop]
        self.size = size

    def parentSelection(self, num_of_pairs):
        dict = {}
        for i in range(num_of_pairs):
            dict[i] = (self.tournament(2), self.tournament(2))
        return dict

    def tournament(self, k=2):
        best = np.random.randint(0, self.size)
        for i in range(k - 1):
            new = np.random.randint(0, self.size)
            if self.isBetter(new,best):
                best = new
        return best

if __name__ == '__main__':
    data = loadData('data/data-J5-O8-M5-S136.txt')
    problem = MultiProjectScheduling(data)
    pop = Population(100,problem)
    pop.addPopulation(pop.pop)
    pop.naturalSelection(100)
    print(pop.size)


