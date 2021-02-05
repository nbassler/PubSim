import math
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

rel_path = '../../data/processed/dose_test/new_SH/'
dirname = os.path.dirname(__file__)
file_path = os.path.join(dirname, rel_path)

PMMA = ['1.760', '1.820', '1.880', '1.940', '2.000']
# PMMA = ['1.300', '1.350', '1.400', '1.450', '1.500', '1.550', '1.600', '1.650', '1.700',
#        '1.750', '1.800', '1.850', '1.900', '1.950', '2.000', '2.050', '2.100', '2.150', '2.200', ]
variant = '_st2'
no_steps = 100
dat_start = 9
diff_start = 5
no_diff_steps = 200
no_files = 36
fig, axs = plt.subplots(1, 2)
for j in PMMA:
    file = file_path + j + variant + '/'

    # Getting the file names
    names = [None]*no_files
    diff_names = [None]*no_files
    for i in range(no_files):
        if i < 10:
            names[i] = 'data_000' + str(i) + '.txt'
            diff_names[i] = 'diff_data_000' + str(i) + '.txt'
        else:
            names[i] = 'data_00' + str(i) + '.txt'
            diff_names[i] = 'diff_data_00' + str(i) + '.txt'

    # Starting with non-diff data
    dat = np.empty([no_files, no_steps])
    for i in range(len(names)):
        df = pd.read_csv(file + names[i], delimiter=' ', skiprows=dat_start)
        dat[i, :] = df['Page(2)'].tolist()

    mean_dat = [None]*no_steps
    stdom_dat = [None]*no_steps
    for i in range(no_steps):
        mean_dat[i] = np.mean(dat[:, i])
        stdom_dat[i] = np.std(dat[:, i]) / math.sqrt(no_files)
    axs[0].errorbar([float(j)], [np.mean(mean_dat)],
                    yerr=[np.mean(stdom_dat)/math.sqrt(no_steps)], fmt='bo')

    # Now diff-data
    dat = np.empty([no_files, no_diff_steps])
    for i in range(len(diff_names)):
        df = pd.read_csv(file + diff_names[i], delimiter=' ', skiprows=diff_start)
        dat[i, :] = df['Diff1(bin#)'].tolist()
    mean_dat = [None]*no_diff_steps
    stdom_dat = [None]*no_diff_steps
    for i in range(no_diff_steps):
        mean_dat[i] = np.mean(dat[:, i])
        stdom_dat[i] = np.std(dat[:, i]) / math.sqrt(no_files)

    x = np.arange(0.00, 38.0, 38.0/no_diff_steps)

    axs[1].errorbar(x, mean_dat, yerr=stdom_dat, label=j + ' cm PMMA')


axs[0].set_xlabel('PMMA depth')
axs[0].set_ylabel('Dose')
axs[0].set_title(
    'Relative Dose_primary for a specific PMMA thickness. Dose max at ~2.59 cm PMMA' + variant)
axs[1].set_xlabel('Energy_primary [MeV/nucl]')
axs[1].set_ylabel('Fluence_primary [/cm2]')
axs[1].set_title('Differential Energy/Fluence Spectra' + variant)
axs[1].legend()
plt.show()
