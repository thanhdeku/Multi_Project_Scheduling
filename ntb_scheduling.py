# Created by Thanh C. Le at 7/19/19
import argparse
import numpy as np
from data import *
from mechanism.nash_tabuSearch import *
from problem import MultiProjectScheduling
## Load parameters
parser = argparse.ArgumentParser(description='Genetic Algorithm Single Objective for Multi-Project Scheduling')
parser.add_argument("--NEIGHBOR_SIZE", type=int, default=10, help="neighborhood size")
parser.add_argument("--NUM_ITERS",type=int,default=1000,help="number of iteration")
parser.add_argument("--DATA",type=str,default='data/data-P5-T8-S5-seed337.txt',help="path to dataset")
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
params.result = np.array([])
ts = TabuSearch(params.problems)
for iters in range(params.NUM_ITERS):
    ts.search(params.NEIGHBOR_SIZE,type=0)
    ts.search(params.NEIGHBOR_SIZE,type=1)
    if (iters + 1)%100 == 0:
        print('Iteration-' + str(iters + 1))
        for optimal in ts.paretoSet:
            print('======('+str(optimal.time_fitness)+','+str(optimal.salary_fitness)+')======')

