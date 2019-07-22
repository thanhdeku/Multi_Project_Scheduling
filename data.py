# Created by Thanh C. Le at 7/20/19
import numpy as np
def createData(num_of_jobs = 5, num_of_machine = 5, num_of_operation = 8):
    process_time = np.random.randint(1,20,size=(num_of_machine,num_of_jobs*num_of_operation))
    return (num_of_jobs,num_of_operation,num_of_machine,process_time)

def generateData(num_of_jobs = 5, num_of_machine = 5, num_of_operation = 8):
    x, y, z, data = createData(num_of_jobs = 5, num_of_machine = 5, num_of_operation = 8)
    seed = np.random.randint(0,1000)
    print(data)
    path = 'data/data-J'+str(num_of_jobs)+'-O'+str(num_of_operation)+'-M'+str(num_of_machine)+ '-S'+str(seed)+'.txt'
    w = open(path,'w')
    w.write(str(x))
    w.write('\n')
    w.write(str(y))
    w.write('\n')
    w.write(str(z))
    for j in range(num_of_machine):
        w.write('\n')
        for i in range(num_of_jobs*num_of_operation):
            w.write(str(data[j,i])+' ')
    w.close()
def loadData(path):
    r = open(path)
    x = int(r.readline())
    y = int(r.readline())
    z = int(r.readline())
    data = np.zeros((z,(x*y)),dtype=int)
    for i in range(z):
        line = r.readline().split()
        for j in range(x*y):
            data[i,j] = int(line[j])
    return x,y,z,data
    #
    # w.close()
def test():
    generateData()
test()