# Created by Thanh C. Le at 7/25/
import numpy as np

x=np.array([1,4,2,5,6])
rank = np.argsort(x)
print(x[rank[:-3]])