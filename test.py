# Created by Thanh C. Le at 7/24/19
from data import loadData
from mechanism.nash_tabuSearch import Individual
from problem import MultiProjectScheduling
import numpy as np
x = np.array([0,9,2,5,4])
print(np.argsort(x))