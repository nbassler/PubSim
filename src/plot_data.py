import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

rel_path = '../../data/'
dirname = os.path.dirname(__file__)
data_path = os.path.join(dirname, rel_path + 'collected_data.txt')
#file_path = '/home/fredo/projects/PubSim/2015_Guan/output/collected_data_2.2e7_parts_truncated.txt'

rows = 5
cols = 5

# loading data into pandas
with open(data_path, 'r') as col:
    df = pd.read_csv(col, delimiter=' ')
print(df)

df['1_Over_Avg_Energy'] = np.divide(1, df['AvgEnergyPrim'])
thick = df.PMMA.unique()
headers = list(df.columns.values)

df_mean = pd.DataFrame(columns=headers)
df_stdom = pd.DataFrame(columns=headers)


# creating two new dataframes:One with mean values and one with stds
for i in thick:
    filt = df['PMMA'] == i
    df_i = df[filt]

    # mean value
    df_mean.loc[str(i)] = df_i.mean()

    # stdom, dividing std with sqrt of number of data-files
    df_stdom.loc[str(i)] = df_i.std().div(math.sqrt(len(df_i.index)))


r1 = 0
r2 = 0
fig, axs = plt.subplots(rows, cols)
for i in headers[1:rows*cols:]:
    x = thick
    y = df_mean[i]
    yerr = df_stdom[i]

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
df_mean.sort_values(by=['DLETPrim'], inplace=True)
print(df_mean['DLETPrim'])
r1 = 0
r2 = 0
fig, axs = plt.subplots(rows, cols)
for i in headers[1:]:

    if i[1] == 'o':
        print(i)
        continue
    if i[0] == 'A':
        print(i)
        continue

    x = np.divide(df_mean['DLETPrim'], 10)
    y = df_mean[i]
    yerr = df_stdom[i]

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
