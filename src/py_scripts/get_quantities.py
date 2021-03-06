import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

'''
Generates a dataframe with the calculated quantities at the specific PMMA depths used
PMMA depths in turn are calculated from dLET_prim
'''
LETs = [[1.11, 4.02, 7.0, 11.9, 18.0, 22.6], [0.9, 1.2, 1.6, 1.8, 1.9, 2.3, 3.0, 5.1, 10.8, 15.2, 17.7, 19.0], [
    1.0, 2.5, 4.3, 6.1, 7.2, 9.6, 12.1, 13.6, 15.2, 16.5, 18.1, 19.5], [2.6, 4.7, 7.3, 11.1, 13.7, 15.4, 16.9, 18.3, 20.2, 21.4]]
file_names = ['collected_data_chaudhary2014_stragg1.txt', 'collected_data_Guan2015_2.2e7_parts.txt',
              'collected_data_Guan2015_2.2e7_parts.txt', 'collected_data_Guan2015_2.2e7_parts.txt']
papers = ['Chaudhary_2014', 'Guan_2015', 'Patel_2017', 'Bronk_2020']

rel_path = '../../data/output/'
dirname = os.path.dirname(__file__)
data_path = os.path.join(dirname, rel_path)

for k in range(len(file_names)):
    # loading data into pandas
    with open(data_path + file_names[k], 'r') as col:
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

    df_mean = df_mean.sort_index()
    df_stdom = df_stdom.sort_index()
    thick.sort()

    # First get a cubib interpolationg function for each quantity. This will be held in a dict
    # with the key being the header in df_mean and value being the function
    quant_names = list(df_mean.columns)
    splines = {}
    for i in quant_names:
        f2 = interp1d(thick, df_mean[i], kind='cubic')
        splines[i] = f2

    # Check dLET_prim splines to get which PMMA thicknesses will be used for checking all quantities
    x = np.arange(min(thick), max(thick), (max(thick) - min(thick))/10000)
    used_thick = [None] * len(LETs[k])
    for i in range(len(LETs[k])):
        run = 0
        while splines['DLETPrim'](x[run]) < LETs[k][i] * 10:
            run += 1
        used_thick[i] = (x[run] + x[run-1])/2

    # Finally create a dataframe with all interpolated values for the quantities
    quants = [[] for _ in range(len(LETs[k]) + 1)]
    quants[0] = quant_names
    for i in range(len(LETs[k])):
        dat = [None] * len(quant_names)
        for j in range(len(quant_names)):
            dat[j] = np.asscalar(splines[quant_names[j]](used_thick[i]))
        quants[i+1] = dat

    if k == 0:
        df_quants = pd.DataFrame(quants[1:], columns=quants[0])
    else:
        df_quants = df_quants.append(pd.DataFrame(quants[1:], columns=quants[0]))


# Adding paper info to df
pap_data = []
for i in range(len(LETs)):
    for j in range(len(LETs[i])):
        pap_data.append(papers[i])
df_quants['paper'] = pap_data

df_quants.to_csv('test.csv')
