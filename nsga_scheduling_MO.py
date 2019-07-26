# Created by Thanh C. Le at 7/25/19
import argparse
import time

import numpy as np
from data import *
from evaluateResult import EvaluateParetoFront
from mechanism.nsgaII_mechanism import Population, Crossover, Mutation, Individual
from problem import MultiProjectScheduling
## Load parameters
parser = argparse.ArgumentParser(description='Genetic Algorithm Single Objective for Multi-Project Scheduling')
parser.add_argument("--POP_SIZE", type=int, default=100, help="population size")
parser.add_argument("--PAIRS_SIZE",type=int, default=50, help="offspring size")
parser.add_argument("--CX_RATE", type=float, default=0.7, help="crossover rate")
parser.add_argument("--MU_RATE", type=float, default=0.03, help="mutation rate")
parser.add_argument("--NUM_ITERS",type=int,default=100,help="number of iteration")
parser.add_argument("--DATA",type=str,default='data/data-P5-T8-S5-seed337.txt',help="path to dataset")
parser.add_argument("--RESULT",type=str,default='Result/Data337-seed',help="path to result")
parser.add_argument("--NUM_SEED",type=int,default=5,help="number of seed to get median of result")
params = parser.parse_args()

## generate data
if params.DATA == '':
    params.data = createData()
else:
    params.data = loadData(params.DATA)

params.problems = MultiProjectScheduling(params.data)
# print(params.problems.process_time)
params.size = params.problems.num_task * params.problems.num_project
population = Population(params.POP_SIZE, params.problems, True)
crossover = Crossover()
mutation = Mutation()

for i in range(params.NUM_SEED):
    np.random.seed(i)
    start_time = time.time()
    for iter in range(params.NUM_ITERS):
        parentSelection = population.parentSelection(params.PAIRS_SIZE)
        offspringPop = []
        for idx, (idx_parent1, idx_parent2) in enumerate(parentSelection.values()):
            if idx_parent1 != idx_parent2:
                parent1 = population.get(idx_parent1)
                parent2 = population.get(idx_parent2)
                s_pivot, e_pivot = crossover.randomTwoPivot(params.size)
                left_parent1, right_parent1 = parent1.representation[0:params.size], parent1.representation[
                                                                                     params.size:]
                left_parent2, right_parent2 = parent2.representation[0:params.size], parent2.representation[
                                                                                     params.size:]
                left_offspring1, left_offspring2 = crossover.pmx(left_parent1, left_parent2, s_pivot, e_pivot)
                right_offspring1, right_offspring2 = crossover.cxTwoPoint(right_parent1, right_parent2, s_pivot,
                                                                          e_pivot)
                offspring1 = Individual(params.problems, np.concatenate((left_offspring1, right_offspring1)))
                offspring2 = Individual(params.problems, np.concatenate((left_offspring2, right_offspring2)))
                offspringPop.append(offspring1)
                offspringPop.append(offspring2)
        population.addPopulation(offspringPop)
        population.updateInfo()
        print('=======' + 'Iteration-' + str(iter + 1) + '=======')
        population.naturalSelection(params.POP_SIZE)
    w = open(params.RESULT+str(i)+'.nsga','w')
    for ind in population.best:
        w.write(str(ind.getFitness(0))+' '+str(ind.getFitness(1)))
        w.write('\n')
    w.close()


