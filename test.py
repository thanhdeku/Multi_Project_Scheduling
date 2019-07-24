# Created by Thanh C. Le at 7/24/19
from data import loadData
from mechanism.nash_tabuSearch import Individual
from problem import MultiProjectScheduling

data = loadData('data/data-J5-O8-M5-S136.txt')
problem = MultiProjectScheduling(data)
ind = Individual(problem,[])
print(ind.findNeighbor())
