import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

rel_path = '../../data/output/'
dirname = os.path.dirname(__file__)
data_path = os.path.join(dirname, rel_path + 'wdir/')

rows = 5
cols = 5

# loading data into pandas
with open(data_path + '../collected_data_chaudhary2014_stragg1.txt', 'r') as col:
    df = pd.read_csv(col, delimiter=' ')

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


print(df_mean)
print(df_stdom)
print(thick)

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
