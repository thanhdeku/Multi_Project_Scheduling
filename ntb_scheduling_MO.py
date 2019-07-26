# Created by Thanh C. Le at 7/19/19
import argparse
import time

import numpy as np
from data import *
from evaluateResult import EvaluateParetoFront
from mechanism.nash_tabuSearch import *
from problem import MultiProjectScheduling
import matplotlib.pyplot as plt
## Load parameters
parser = argparse.ArgumentParser(description='Genetic Algorithm Single Objective for Multi-Project Scheduling')
parser.add_argument("--NEIGHBOR_SIZE", type=int, default=10, help="neighborhood size")
parser.add_argument("--NUM_ITERS",type=int,default=10000,help="number of iteration")
parser.add_argument("--DATA",type=str,default='data/data-P5-T8-S5-seed337.txt',help="path to dataset")
parser.add_argument("--NUM_SEED",type=int,default=5,help="number of seed to get median of result")
parser.add_argument("--RESULT",type=str,default='Result/Data337-seed',help="path to result")
params = parser.parse_args()

## generate data
if params.DATA == '':
    params.data = createData()
else:
    params.data = loadData(params.DATA)

params.problems = MultiProjectScheduling(params.data)
# print(params.problems.process_time)
params.size = params.problems.num_task * params.problems.num_project
params.result = np.array([])
ts = TabuSearch(params.problems)

for i in range(params.NUM_SEED):
    np.random.seed(i)
    start_time = time.time()
    for iters in range(params.NUM_ITERS):
        ts.search(params.NEIGHBOR_SIZE, type=0)
        ts.search(params.NEIGHBOR_SIZE, type=1)
        print('==============Iteration-' + str(iters + 1) + '==============')
    w = open(params.RESULT + str(i) + '.ntb', 'w')
    for ind in ts.paretoSet:
        w.write(str(ind.getFitness(0)) + ' ' + str(ind.getFitness(1)))
        w.write('\n')
    w.close()