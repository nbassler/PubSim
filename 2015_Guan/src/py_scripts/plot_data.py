import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rel_path = '../../data/output/'
dirname = os.path.dirname(__file__)
data_path = os.path.join(dirname, rel_path + 'wdir/')

# loading data into pandas
with open(data_path + '../collected_data.txt', 'r') as col:
    df = pd.read_csv(col, delimiter=' ')


thick = df.PMMA.unique()
print(thick)
headers = list(df.columns.values)

df_mean = pd.DataFrame(columns=headers)
df_std = pd.DataFrame(columns=headers)
print(df_std)


# dictionary with all mean and std values, with each thickness as a key, and [mean, std] as value
vals = {}
for i in thick:
    filt = df['PMMA'] == i
    df_i = df[filt]

    # mean value
    df_mean.loc[str(i)] = df_i.mean()

    # std
    df_std.loc[str(i)] = df_i.std()

r1 = 0
r2 = 0
fig, axs = plt.subplots(4, 4)
for i in headers[1:]:
    x = thick
    y = df_mean[i]
    yerr = df_std[i]

    axs[r1, r2].errorbar(x, y, yerr=yerr)
    axs[r1, r2].set_title(i)
    #axs[r1, r2].set_xlabel('PMMA thickness')

    # changing axis position
    r1 += 1
    if r1 > 3:
        r1 = 0
        r2 += 1

plt.show()
