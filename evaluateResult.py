# Created by Thanh C. Le at 7/25/19
import numpy as np

from data import loadData
from mechanism.nash_tabuSearch import Individual
from problem import MultiProjectScheduling


class EvaluateParetoFront:
    def __init__(self,paretoFront,num_objective):
        self.nps = len(paretoFront)
        self.paretoFront = np.zeros((self.nps,num_objective))
        for i in range(self.nps):
            for j in range(num_objective):
                self.paretoFront[i,j] = paretoFront[i].getFitness(j)

    def evalNPS(self):
        return self.nps

    def evalSpacing(self):
        d = np.zeros(self.nps)
        if self.nps == 1:
            return 0
        else:
            for i in range(self.nps):
                distance = np.sum(np.abs(self.paretoFront - self.paretoFront[i]), axis=1)
                d[i] = distance[np.argsort(distance)[1]]
            d = d - np.mean(d)
            d = d ** 2
            return np.sqrt(np.sum(d) / (self.nps - 1))


    def evalDiversity(self):
        max = np.max(self.paretoFront,axis=0)
        min = np.min(self.paretoFront,axis=0)
        delta = max - min
        return np.sqrt(np.sum(delta**2))

    def evalMMID(self):
        max = np.max(self.paretoFront,axis=0)
        min = np.min(self.paretoFront,axis=0)
        delta = max - min
        tb = (self.paretoFront - min)/delta
        tb = tb ** 2
        tb = np.sqrt(np.sum(tb,axis=1))
        return np.sum(tb)/self.nps

if __name__ == '__main__':
    data = loadData('data/data-J5-O8-M5-S136.txt')
    problem = MultiProjectScheduling(data)
    paretoSet =[]
    for i in range(3):
        paretoSet.append(Individual(problem,[]))
    eval = EvaluateParetoFront(paretoSet,2)
    print(eval.evalMMID())
