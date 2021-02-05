import math
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

rel_path = '../../data/processed/dose_test/1.880/'
dirname = os.path.dirname(__file__)
file_path = os.path.join(dirname, rel_path)

no_files = 72
x_start = -7.92
x_end = 8.0
x_step = 0.16
names = [None]*no_files
for i in range(no_files):
    if i < 10:
        names[i] = 'data_000' + str(i) + '.txt'
    else:
        names[i] = 'data_00' + str(i) + '.txt'

dat = np.empty([no_files, 100])
for i in range(len(names)):
    df = pd.read_csv(file_path + names[i], delimiter=' ', skiprows=9)
    dat[i, :] = df['Page(2)'].tolist()

mean_dat = [None]*100
stdom_dat = [None]*100
for i in range(100):
    mean_dat[i] = np.mean(dat[:, i])
    stdom_dat[i] = np.std(dat[:, i]) / math.sqrt(no_files)

print('Mean Dose: ' + str(np.mean(mean_dat)))
x = np.arange(x_start, x_end, x_step)
print(mean_dat)
print(stdom_dat)
print(len(x))
plt.errorbar(x, mean_dat, yerr=stdom_dat, fmt='bo')
plt.plot([min(x), max(x)], [np.mean(mean_dat), np.mean(mean_dat)], 'r-')
#plt.ylim((0, 0.6))
plt.xlabel('Lateral distribution')
plt.ylabel('Dose')
plt.title('Dose with ' + rel_path[-6:-1] + ' cm PMMA, Mean Dose = ' + str(np.mean(mean_dat)))
plt.show()
