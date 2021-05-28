import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

rel_path = '../../data/'
dirname = os.path.dirname(__file__)

# data path should point to the csv-file containing the mean and stderr values for each PMMA thickness
data_path = os.path.join(dirname, rel_path + 'summary.csv')

header = 'AvgEnergyPrim Dose DosePrim DoseProt DLET DLETPrim DLETProt TLET TLETPrim TLETProt dQ dQPrim dQProt tQ tQPrim tQProt dZeff2Beta2 dZeff2Beta2Prim dZeff2Beta2Prot tZeff2Beta2 tZeff2Beta2Prim tZeff2Beta2Prot'

ion = 'H'

rows = 5
cols = 5

# loading data into pandas
with open(data_path, 'r') as col:
    df = pd.read_csv(col, delimiter=',')


df.columns = ['stat_moment', 'ion', 'PMMA', 'AvgEnergyPrim', 'Dose', 'DosePrim', 'DoseProt', 'DLET', 'DLETPrim', 'DLETProt', 'TLET', 'TLETPrim', 'TLETProt',
              'dQ', 'dQPrim', 'dQProt', 'tQ', 'tQPrim', 'tQProt', 'dZeff2Beta2', 'dZeff2Beta2Prim', 'dZeff2Beta2Prot', 'tZeff2Beta2', 'tZeff2Beta2Prim', 'tZeff2Beta2Prot']

#df['1_Over_Avg_Energy'] = np.divide(1, df['AvgEnergyPrim'])

# splitting mean and stdom
df_mean = df[df['stat_moment'] == 'mean']
df_stdom = df[df['stat_moment'] == 'stderr']

# filtering by ion
df_mean_ion = df_mean[df_mean['ion'] == ion]
df_stdom_ion = df_stdom[df_stdom['ion'] == ion]

thick = df_mean_ion['PMMA'].values


# plotting raw data
r1 = 0
r2 = 0
fig, axs = plt.subplots(rows, cols)
for i in df.columns[3:]:
    x = thick
    y = df_mean_ion[i]
    yerr = df_stdom_ion[i]

    axs[r1, r2].errorbar(x, y, yerr=yerr, fmt='bo')
    axs[r1, r2].set_title(i)
    # axs[r1, r2].set_xlabel('PMMA thickness')

    # changing axis position
    r1 += 1
    if r1 > rows - 1:
        r1 = 0
        r2 += 1
plt.show()

rows = 5
cols = 4

# Plotting vs DLET_prim on x-axix
df_mean_ion.sort_values(by=['DLETPrim'], inplace=True)

r1 = 0
r2 = 0
fig, axs = plt.subplots(rows, cols)
for i in df.columns[3:]:
    print(i)

    if i[1] == 'o':
        print(i)
        continue
    if i[0] == 'A':
        print(i)
        continue

    x = np.divide(df_mean_ion['DLETPrim'], 10)
    y = df_mean_ion[i]
    yerr = df_stdom_ion[i]

    if i != 'DLETPrim':
        axs[r1, r2].errorbar(x, y, yerr=yerr, fmt='bo', label=i)
        axs[r1, r2].plot(x, y)
        #axs[r1, r2].set_title(i)
    else:
        axs[r1, r2].errorbar(x, y, yerr=yerr, fmt='ro', label=i)
        axs[r1, r2].plot(x, y, 'r-')
    axs[r1, r2].legend()
    # axs[r1, r2].set_xlabel('PMMA thickness')

    # changing axis position
    r1 += 1
    if r1 > rows - 1:
        r1 = 0
        r2 += 1
fontsize = 20
fig.text(0.5, 0.04, 'LETd_Primary', ha='center', fontsize=fontsize)
fig.text(0.04, 0.5, 'Quantity', va='center', rotation='vertical', fontsize=fontsize)
plt.show()
