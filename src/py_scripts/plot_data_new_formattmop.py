import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

rel_path = '../../data/'
dirname = os.path.dirname(__file__)

# data path should point to the csv-file containing the mean and stderr values for each PMMA thickness
data_path = os.path.join(dirname, rel_path + 'summary_mod_new.csv')

header = 'AvgEnergyPrim Dose DosePrim DoseProt DLET DLETPrim DLETProt TLET TLETPrim TLETProt dQ dQPrim dQProt tQ tQPrim tQProt dZeff2Beta2 dZeff2Beta2Prim dZeff2Beta2Prot tZeff2Beta2 tZeff2Beta2Prim tZeff2Beta2Prot'

ion = 'H'
ref_quant = 'dLET, primary'

rows = 5
cols = 5

# loading data into pandas
with open(data_path, 'r') as col:
    df = pd.read_csv(col, delimiter=',')


df.columns = ['stat_moment', 'ion', 'PMMA', 'AvgEnergyPrim', 'Dose', 'DosePrim', 'DoseProt', 'DLET', 'DLETPrim', 'DLETProt', 'TLET', 'TLETPrim', 'TLETProt',
              'dQ', 'dQPrim', 'dQProt', 'tQ', 'tQPrim', 'tQProt', 'dZeff2Beta2', 'dZeff2Beta2Prim', 'dZeff2Beta2Prot', 'tZeff2Beta2', 'tZeff2Beta2Prim', 'tZeff2Beta2Prot']

df.columns = ['stat_moment', 'ion', 'PMMA', 'AvgEnergyPrim', 'Dose', 'DosePrim', 'DoseProt', 'dLET, all', 'dLET, primary', 'dLET, protons', 'tLET, all', 'tLET, primary', 'tLET, protons',
              'dQ, all', 'dQ, primary', 'dQ, protons', 'tQ, all', 'tQ, primary', 'tQ, protons', 'd' + r'$\frac{z^{*2}}{\beta ^{2}}$' + ', all', 'd' + r'$\frac{z^{*2}}{\beta ^{2}}$' + ', primary', 'd' + r'$\frac{z^{*2}}{\beta ^{2}}$' + ', protons', 't' + r'$\frac{z^{*2}}{\beta ^{2}}$' + ', all', 't' + r'$\frac{z^{*2}}{\beta ^{2}}$' + ', primary', 't' + r'$\frac{z^{*2}}{\beta ^{2}}$' + ', protons']

# df['1_Over_Avg_Energy'] = np.divide(1, df['AvgEnergyPrim'])

# splitting mean and stdom
df_mean = df[df['stat_moment'] == 'mean']
df_stdom = df[df['stat_moment'] == 'stderr']

df_mean[r'$\frac{1}{primary\ energy}$'] = np.divide(1, df_mean['AvgEnergyPrim'])
df_stdom[r'$\frac{1}{primary\ energy}$'] = np.multiply(np.divide(1, np.square(
    df_mean['AvgEnergyPrim'])), df_stdom['AvgEnergyPrim'])

# filtering by ion
df_mean_ion = df_mean[df_mean['ion'] == ion]
df_stdom_ion = df_stdom[df_stdom['ion'] == ion]

thick = df_mean_ion['PMMA'].values

# plotting raw data
r1 = 0
r2 = 0
fig, axs = plt.subplots(rows, cols)
for i in df_mean.columns[3:]:
    x = thick
    y = df_mean_ion[i]
    yerr = df_stdom_ion[i]
    print(i)
    axs[r1, r2].errorbar(x, y, yerr=yerr, fmt='bo')
    axs[r1, r2].set_title(i)
    # axs[r1, r2].set_xlabel('PMMA thickness')

    # changing axis position
    r1 += 1
    if r1 > rows - 1:
        r1 = 0
        r2 += 1
plt.show()

# Interpolating values before plotting against dLET_primary, so make the distribution homogeneous along the x-axis
'''
quant_names = list(df_mean_ion.columns[2:])
splines = {}
for i in quant_names:
    f2 = interp1d(thick, df_mean_ion[i], kind='cubic')
    splines[i] = f2
'''
# Plotting vs DLET_prim on x-axix
df_mean_ion.sort_values(by=[ref_quant], inplace=True)

rows = 4
cols = 5
r1 = 0
r2 = 0
fig, axs = plt.subplots(rows, cols)
for i in df_mean.columns[7:]:
    '''
    if i[1] == 'o':
        print(i)
        continue
    if i[0] == 'A':
        print(i)
        continue
    '''
    if 'LET' in ref_quant:
        x = np.divide(df_mean_ion[ref_quant], 10)
    else:
        x = df_mean_ion[ref_quant]

    if 'LET' in i:
        y = np.divide(df_mean_ion[i], 10)
        yerr = np.divide(df_stdom_ion[i], 10)
    else:
        y = df_mean_ion[i]
        yerr = df_stdom_ion[i]
    corr = np.corrcoef([x, y])

    if i != ref_quant:
        axs[r1, r2].errorbar(x, y, yerr=yerr, fmt='bo', label=i +
                             '\ncorr = ' + str(np.round(corr[0][1], 3)))
        axs[r1, r2].plot(x, y)
        # axs[r1, r2].set_title(i)
    else:
        axs[r1, r2].errorbar(x, y, yerr=yerr, fmt='ro', label=i +
                             '\ncorr = ' + str(np.round(corr[0][1], 3)))
        axs[r1, r2].plot(x, y, 'r-')
    axs[r1, r2].legend()
    # axs[r1, r2].set_xlabel('PMMA thickness')

    # changing axis position
    r1 += 1
    if r1 > rows - 1:
        r1 = 0
        r2 += 1
fontsize = 20
fig.text(0.5, 0.04, ref_quant, ha='center', fontsize=fontsize)
fig.text(0.04, 0.5, 'Quantity', va='center', rotation='vertical', fontsize=fontsize)
plt.show()
