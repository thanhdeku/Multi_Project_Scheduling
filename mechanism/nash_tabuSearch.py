# Created by Thanh C. Le at 7/24/19
import sys
import numpy as np

class Individual:

    def __init__(self,problem,representation,init = True,):
        self.problem = problem
        self.representation = representation
        self.time_fitness = sys.maxsize
        self.salary_fitness = sys.maxsize
        if init:
            self.representation = self.generate_representation()
        self.time_fitness = self.computeFitness('time')
        self.salary_fitness = self.computeFitness('salary')

    def generate_representation(self):
        return self.problem.generate_genotype()

    def updateFitness(self,x):
        self.fitness = x

    def computeFitness(self,type='time'):
        if type == 'time':
            return self.problem.computeTotalTime(self.representation)
        if type == 'salary':
            return self.problem.computeSalary(self.representation)

    def neighborhood(self,num_neighbor,type=0):
        dict = {}
        for i in range(num_neighbor):
            neighbor = self.findNeighbor()
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
            gen[size + pivot1:size + pivot2] = self.representation[size + pivot1 + 1:size + pivot2 + 1]
            gen[size + pivot2] = self.representation[size + pivot1]
        return gen

class TabuList:
    def __init__(self,size,problem):
        self.size = size
        self.problem = problem

    def generatePop(self):
        pop = []
        timeFitness = []
        salaryFitness = []
        for i in range(self.size):
            ind = Individual(self.problem,[],True)
            pop.append(ind)
            timeFitness.append(ind.time_fitness)
            salaryFitness.append(ind.salary_fitness)




