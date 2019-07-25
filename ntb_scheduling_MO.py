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
parser.add_argument("--DATA",type=str,default='data/data-P5-T8-S5-seed23.txt',help="path to dataset")
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

nps = 0
mmid = 0
spacing = 0
diversity = 0
run_time = 0
for i in range(params.NUM_SEED):
    np.random.seed(i)
    start_time = time.time()
    for iters in range(params.NUM_ITERS):
        ts.search(params.NEIGHBOR_SIZE, type=0)
        ts.search(params.NEIGHBOR_SIZE, type=1)
        if (iters + 1) % 100 == 0:
            print('==============Iteration-' + str(iters + 1) + '==============')
            eval = EvaluateParetoFront(ts.paretoSet, 2)
            if iters == params.NUM_ITERS - 1:
                nps += eval.evalNPS()
                mmid += eval.evalMMID()
                spacing += eval.evalSpacing()
                diversity += eval.evalDiversity()
            print('===NPS===' + str(round(eval.evalNPS(), 3)) + '===')
            print('===MMID===' + str(round(eval.evalMMID(), 3)) + '===')
            print('===SPACING===' + str(round(eval.evalSpacing(), 3)) + '===')
            print('===DIVERSITY===' + str(round(eval.evalDiversity(), 3)) + '===')
    run_time += time.time() - start_time

nps /= params.NUM_SEED
mmid /= params.NUM_SEED
spacing /= params.NUM_SEED
diversity /= params.NUM_SEED
run_time /= params.NUM_SEED
w = open('Result/ntb.txt','w')
w.write('NPS: ' + str(nps))
w.write('MMID: ' + str(mmid))
w.write('Spacing: ' + str(spacing))
w.write('Diversity: ' + str(diversity))
w.write('Run time: ' + str(run_time))
w.close()
