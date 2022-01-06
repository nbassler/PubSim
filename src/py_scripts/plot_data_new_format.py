import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy import optimize as op


def linfit(x, a):
    return a * x


rel_path = '../../data/'
dirname = os.path.dirname(__file__)

# data path should point to the csv-file containing the mean and stderr values for each PMMA thickness
data_path = os.path.join(dirname, rel_path + 'summary_jul8.csv')

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

quant_names = list(df_mean.columns[7:])
quant_labels = ["$\mathrm{LET_{d}, all \: particles}$", "$\mathrm{LET_{d}, primary}$", "$\mathrm{LET_{d}, protons}$", "$\mathrm{LET_{t}, all \: particles}$", "$\mathrm{LET_{t}, primary}$", "$\mathrm{LET_{t}, protons}$", "$\mathrm{Q_{d}, all \: particles}$", "$\mathrm{Q_{d}, primary}$", "$\mathrm{Q_{d}, protons}$",
                "$\mathrm{Q_{t}, all \: particles}$", "$\mathrm{Q_{t}, primary}$", "$\mathrm{Q_{t}, protons}$", "$\mathrm{Q_{eff, d}, all \: particles}$", "$\mathrm{Q_{eff, d}, primary}$", "$\mathrm{Q_{eff, d}, protons}$", "$\mathrm{Q_{eff, t}, all \: particles}$", "$\mathrm{Q_{eff, t}, primary}$", "$\mathrm{Q_{eff, t}, protons}$", "$\mathrm{1 \: / \: (primary \: energy) }$"]
# create dict with names
names = {}

for idx, q in enumerate(quant_names):
    names[q] = quant_labels[idx]

# plotting raw data
r1 = 0
r2 = 0
fig, axs = plt.subplots(rows, cols)
for i in df_mean.columns[3:]:
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

# scaling all LET columns to kev/um unit
for i in quant_names:
    if 'LET' in i:
        df_mean_ion[i] = np.divide(df_mean_ion[i], 10)
        df_stdom_ion[i] = np.divide(df_stdom_ion[i], 10)

# Interpolating values before plotting against ref_quant, so make the distribution homogeneous along the x-axis
splines = {}
for i in quant_names:
    f2 = interp1d(df_mean_ion[ref_quant], df_mean_ion[i], kind='cubic')
    splines[i] = f2

# Plotting vs DLET_prim on x-axix
df_mean_ion.sort_values(by=[ref_quant], inplace=True)

rows = 4
cols = 5
r1 = 0
r2 = 0

# x is ref_quant min to max, with equal steps between
start = np.min(df_mean_ion[ref_quant])
stop = np.max(df_mean_ion[ref_quant])
step = (stop-start)/2000

x = np.arange(start=start, stop=stop, step=step)

fig, axs = plt.subplots(rows, cols)

# starting with col7 = dLET, all
linewidth = 3
for i in quant_names:
    # getting y-values from splines
    y = splines[i](x)
    # calculating correlation coefficient
    corr = np.corrcoef([x, y])
    # performing linear fit
    popt, pcov = op.curve_fit(linfit, x, y)
    lfit = popt[0] * x
    r = np.subtract(lfit, y)
    RMSE = np.sqrt(np.mean(np.square(r)))
    RMSE_norm = np.divide(RMSE, np.max(y))

    if i != ref_quant:
        axs[r1, r2].plot(x, y, label=names[i] +
                         '\ncorr = ' + str(np.round(corr[0][1], 3)), linewidth=linewidth)
        # axs[r1, r2].set_title(i)
    else:
        axs[r1, r2].plot(x, y, 'r-', label=names[i] +
                         '\ncorr = ' + str(np.round(corr[0][1], 3)), linewidth=linewidth)
    axs[r1, r2].plot(x, lfit, label='normalized linear fit \nerror = ' +
                     str(np.round(RMSE_norm, 3)))
    axs[r1, r2].legend()
    # axs[r1, r2].set_xlabel('PMMA thickness')

    # changing axis position
    r1 += 1
    if r1 > rows - 1:
        r1 = 0
        r2 += 1
fontsize = 20
fig.text(0.5, 0.04, names[ref_quant], ha='center', fontsize=fontsize)
fig.text(0.04, 0.5, 'Quantity', va='center', rotation='vertical', fontsize=fontsize)
plt.tight_layout()
plt.show()
