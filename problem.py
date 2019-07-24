# Created by Thanh C. Le at 7/19/19
from queue import Queue

from data import createData, loadData
import numpy as np

class MultiProjectScheduling():
    def __init__(self,data):
        self.num_project, self.num_task, self.num_staff, self.process_time, self.salary = data
        sum = np.sum(self.process_time,axis=0)
        self.probs = (1 - self.process_time / (sum.reshape(1, self.num_task * self.num_project))) / (self.num_staff - 1)


    def computeFitness(self,genotype):
        return self.computeTotalTime(genotype)

    def computeTotalTime(self,genotype):
        job_time = np.zeros(self.num_project)
        machine_time = np.zeros(self.num_staff)
        total_operation = self.num_project * self.num_task
        for i in range(self.num_project * self.num_task):
            operation_index = genotype[i]
            job_index = int(operation_index / self.num_task)
            machine_index = genotype[i + total_operation]
            end_time = self.process_time[machine_index, operation_index]
            machine_time[machine_index] += end_time
            job_time[job_index] = max(job_time[job_index], machine_time[machine_index])
        return np.sum(job_time)

    def computeSalary(self,genotype):
        size = (self.num_task*self.num_project)
        tasks = genotype[0:size]
        staff = genotype[size:]
        time = self.process_time[staff,tasks]
        total_salary = self.salary[staff] * time
        return np.sum(total_salary)

    def generate_jobScheduling(self):
        x = np.array([i for i in range(self.num_project) for j in range(self.num_task)])
        np.random.shuffle(x)
        return x

    def generate_operation(self,order = True):
        job_scheduling = self.generate_jobScheduling()
        temp = np.array([i for i in range(self.num_task)])
        operation_scheduling = []
        if order:
            dict = {}
            for i in range(self.num_project):
                element = temp + self.num_task * i
                queue = Queue()
                for j in range(self.num_task):
                    queue.put(element[j])
                dict[i] = queue
            for i in range(len(job_scheduling)):
                operation_scheduling.append(dict[job_scheduling[i]].get())
        else:
            dict = {}
            for i in range(self.num_project):
                element = temp + self.num_task * i
                np.random.shuffle(element)
                queue = Queue()
                for j in range(self.num_task):
                    queue.put(element[j])
                dict[i] = queue
            for i in range(len(job_scheduling)):
                operation_scheduling.append(dict[job_scheduling[i]].get())

        return np.array(operation_scheduling)

    def generate_genotype(self, type = 'randomWithProbs'):
        operation_scheduling = self.generate_operation()
        machine_scheduling = []
        if type == 'randomWithProbs':
            for i in range(self.num_project * self.num_task):
                machine_scheduling.append(np.random.choice(self.num_staff, p=self.probs[:, operation_scheduling[i]]))
        return np.concatenate((operation_scheduling,np.array(machine_scheduling)))

# def test():
#     data = loadData('data/data-J5-O8-M5-S136.txt')
#     problem = MultiProjectScheduling(data)
#     gen = problem.generate_genotype()
#     print(problem.computeSalary(gen))
# test()