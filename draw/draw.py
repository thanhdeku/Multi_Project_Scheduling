# Created by Thanh C. Le at 7/25/19
import matplotlib.pyplot as plt
import numpy as np

nsga_f1 = np.load('draw/nsga_f1-1.npy')
nsga_f2 = np.load('draw/nsga_f2-1.npy')
x = np.argsort(nsga_f1)
ntb_f1 = np.load('draw/ntb_f1-1.npy')
ntb_f2 = np.load('draw/ntb_f2-1.npy')
y = np.argsort(ntb_f1)
# plt.plot(nsga_f1[x],nsga_f2[x])
plt.plot(ntb_f1[y],ntb_f2[y])
plt.show()
plt.savefig('result_25_7')



