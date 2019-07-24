# Created by Thanh C. Le at 7/20/19
import numpy as np
def createData(num_of_project = 5, num_of_staffs = 5, num_of_tasks = 8):
    process_time = np.random.randint(1, 20, size=(num_of_staffs, num_of_project * num_of_tasks))
    salary = np.random.randint(1, 20, size=num_of_staffs)
    return (num_of_project, num_of_tasks, num_of_staffs, process_time, salary)

def generateData(num_of_project = 5, num_of_staffs = 5, num_of_tasks = 8):
    x, y, z, process_time, salary = createData(num_of_project= 5, num_of_staffs= 5, num_of_tasks= 8)
    seed = np.random.randint(0,1000)
    path = 'data/data-P' + str(num_of_project) + '-T' + str(num_of_tasks) + '-S' + str(num_of_staffs) + '-seed' + str(seed) + '.txt'
    w = open(path,'w')
    w.write(str(x))
    w.write(' ')
    w.write(str(y))
    w.write(' ')
    w.write(str(z))
    for j in range(num_of_staffs):
        w.write('\n')
        for i in range(num_of_project * num_of_tasks):
            w.write(str(process_time[j,i])+' ')
    w.write('\n')
    for i in range(num_of_staffs):
        w.write(str(salary[i])+' ')
    w.close()
def loadData(path):
    r = open(path)
    param = r.readline().split()
    x = int(param[0])
    y = int(param[1])
    z = int(param[2])
    data = np.zeros((z,(x*y)),dtype=int)
    for i in range(z):
        line = r.readline().split()
        data[i] = np.array(line).astype(int)
    salary = r.readline().split()
    salary = np.array(salary)
    salary = salary.astype(int)
    return x,y,z,data, salary

def test():
    generateData()
