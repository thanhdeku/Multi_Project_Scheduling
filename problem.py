# Created by Thanh C. Le at 7/19/19
from queue import Queue

from data import createData
import numpy as np

class MultiProjectScheduling():
    def __init__(self,data):
        self.num_job, self.num_operation, self.num_machine, self.process_time = data
        sum = np.sum(self.process_time,axis=0)
        self.probs = (1- self.process_time/(sum.reshape(1,self.num_operation*self.num_job)))/(self.num_machine-1)


    def computeFitness(self,genotype):
        job_time = np.zeros(self.num_job)
        machine_time = np.zeros(self.num_machine)
        total_operation = self.num_job*self.num_operation
        for i in range(self.num_job*self.num_operation):
            operation_index = genotype[i]
            job_index = int(operation_index/self.num_operation)
            machine_index = genotype[i+total_operation]
            end_time = self.process_time[machine_index,operation_index]
            machine_time[machine_index] += end_time
            job_time[job_index] = max(job_time[job_index],machine_time[machine_index])
        return np.sum(job_time)

    def generate_jobScheduling(self):
        x = np.array([i for i in range(self.num_job) for j in range(self.num_operation)])
        np.random.shuffle(x)
        return x

    def generate_operation(self,order = True):
        job_scheduling = self.generate_jobScheduling()
        temp = np.array([i for i in range(self.num_operation)])
        operation_scheduling = []
        if order:
            dict = {}
            for i in range(self.num_job):
                element = temp + self.num_operation * i
                queue = Queue()
                for j in range(self.num_operation):
                    queue.put(element[j])
                dict[i] = queue
            for i in range(len(job_scheduling)):
                operation_scheduling.append(dict[job_scheduling[i]].get())
        else:
            dict = {}
            for i in range(self.num_job):
                element = temp + self.num_operation * i
                np.random.shuffle(element)
                queue = Queue()
                for j in range(self.num_operation):
                    queue.put(element[j])
                dict[i] = queue
            for i in range(len(job_scheduling)):
                operation_scheduling.append(dict[job_scheduling[i]].get())

        return np.array(operation_scheduling)

    def generate_genotype(self, type = 'randomWithProbs'):
        operation_scheduling = self.generate_operation()
        machine_scheduling = []
        if type == 'randomWithProbs':
            for i in range(self.num_job*self.num_operation):
                machine_scheduling.append(np.random.choice(self.num_machine,p=self.probs[:,operation_scheduling[i]]))
        return np.concatenate((operation_scheduling,np.array(machine_scheduling)))

def test():
    data = createData()
    mp = MultiProjectScheduling(data)
    # print(mp.process_time[5,5])
test()