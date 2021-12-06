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
LETs = [[0.9, 1.2, 1.6, 1.8, 1.9, 2.3, 3.0, 5.1, 10.8, 15.2, 17.7, 19.0], [
    1.0, 2.5, 4.3, 6.1, 7.2, 9.6, 12.1, 13.6, 15.2, 16.5, 18.1, 19.5], [2.6, 4.7, 7.3, 11.1, 13.7, 15.4, 16.9, 18.3, 20.2, 21.4]]
file_names = ['summary.csv', 'summary.csv', 'summary.csv']
papers = ['Guan_2015', 'Patel_2017', 'Bronk_2020']

LETs = [[0.99, 0.99, 0.99, 1.02, 1.02, 1.02, 1.02, 1.03, 1.05, 1.05, 1.07, 1.07, 1.08, 1.08, 1.08, 1.09, 1.09, 1.09, 1.11, 1.11, 1.11, 1.11, 1.11, 1.11, 1.11, 1.12, 1.12, 1.12, 1.13, 1.13, 1.13, 1.14, 1.14, 1.14, 1.14, 1.16, 1.16, 1.16, 1.17, 1.18, 1.18, 1.18, 1.19, 1.19, 1.19, 1.2, 1.2, 1.2, 1.2, 1.21, 1.21, 1.21, 1.21, 1.21, 1.22, 1.23, 1.25, 1.28, 1.29, 1.3, 1.3, 1.41, 1.45, 1.45, 1.69, 1.7, 1.72, 1.74, 1.75, 1.77, 1.79, 1.8, 1.83, 1.85, 1.88, 1.91, 1.91, 1.93, 1.94, 2.02, 2.02, 2.02, 2.03, 2.03, 2.05, 2.05, 2.06, 2.08, 2.09, 2.1, 2.11, 2.12, 2.12, 2.12, 2.17, 2.2, 2.2, 2.2, 2.2, 2.2, 2.25, 2.28, 2.28, 2.3, 2.3, 2.32, 2.35, 2.35, 2.36, 2.41, 2.42, 2.42, 2.42, 2.5, 2.5, 2.5, 2.53, 2.53, 2.53, 2.53, 2.53, 2.53, 2.53, 2.53, 2.53, 2.54, 2.54, 2.56, 2.56, 2.56, 2.56, 2.6, 2.6, 2.6, 2.63,
         2.64, 2.65, 2.65, 2.66, 2.69, 2.71, 2.73, 2.74, 2.74, 2.76, 2.76, 2.8, 2.86, 2.86, 2.9, 2.93, 2.93, 2.93, 2.95, 2.99, 3.05, 3.1, 3.1, 3.11, 3.12, 3.19, 3.19, 3.2, 3.27, 3.27, 3.4, 3.44, 3.46, 3.48, 3.48, 3.51, 3.615, 3.7, 3.71, 3.75, 3.79, 3.83, 3.91, 3.94, 3.94, 4, 4.02, 4.02, 4.04, 4.04, 4.04, 4.07, 4.1, 4.25, 4.25, 4.3, 4.3, 4.4, 4.5, 4.5, 4.53, 4.76, 4.8, 4.82, 4.93, 5.1, 5.22, 5.28, 5.8, 5.8, 5.8, 5.82, 6, 6.08, 6.19, 6.2, 6.23, 6.23, 6.3, 6.35, 6.35, 6.71, 6.85, 6.85, 6.9, 7, 7, 7.06, 7.5, 7.5, 7.5, 7.6, 7.7, 7.7, 7.7, 7.7, 7.7, 7.75, 7.9, 7.9, 7.9, 7.9, 8.11, 8.22, 8.22, 8.72, 8.83, 9.23, 9.23, 9.445, 10, 10, 10, 10, 10.1, 10.5, 10.8, 10.9, 10.9, 11, 11, 11, 11, 11.9, 11.9, 12.1, 13.4, 13.4, 13.5, 14, 14, 14, 15, 15.6, 17, 17, 17, 17.1, 17.6, 17.8, 18, 18, 19.7, 19.7, 19.8]]
file_names = ['summary_jul8.csv']
papers = ['Pag_2014']
ion = "H"
'''
LETs = [[20.2, 39.8, 63.1, 70.6, 84.3, 100.8, 126.3, 157.6, 196.4, 242.9, 285.8, 308.4]]
file_names = ['summary.csv']
papers = ['Bronk_2020']
ion = 'C'

LETs = [[6.6, 11.1, 14.3, 21.9, 33.8, 41.6, 50.4, 57.9, 65.2, 70.3, 73.4, 70.1]]
file_names = ['summary.csv']
papers = ['Bronk_2020']
ion = 'He'
'''
rel_path = '../../data/'
dirname = os.path.dirname(__file__)

# data path should point to the csv-file containing the mean and stderr values for each PMMA thickness
data_path = os.path.join(dirname, rel_path)

for k in range(len(file_names)):
    # loading data into pandas
    with open(data_path + file_names[k], 'r') as col:
        df = pd.read_csv(col, delimiter=',')

    df.columns = ['stat_moment', 'ion', 'PMMA', 'AvgEnergyPrim', 'Dose', 'DosePrim', 'DoseProt', 'DLET', 'DLETPrim', 'DLETProt', 'TLET', 'TLETPrim', 'TLETProt',
                  'dQ', 'dQPrim', 'dQProt', 'tQ', 'tQPrim', 'tQProt', 'dZeff2Beta2', 'dZeff2Beta2Prim', 'dZeff2Beta2Prot', 'tZeff2Beta2', 'tZeff2Beta2Prim', 'tZeff2Beta2Prot']
    '''
    df.columns = ['stat_moment', 'ion', 'PMMA', 'AvgEnergyPrim', 'Dose', 'DosePrim', 'DoseProt', 'DLET', 'DLETPrim', 'DLETProt', 'TLET', 'TLETPrim', 'TLETProt',
                  'dQ_300keV', 'dQPrim_300keV', 'dQProt_300keV', 'tQ_300keV', 'tQPrim_300keV', 'tQProt_300keV', 'dZeff2Beta2', 'dZeff2Beta2Prim', 'dZeff2Beta2Prot', 'tZeff2Beta2', 'tZeff2Beta2Prim', 'tZeff2Beta2Prot']
    # splitting mean and stdom
    df_mean = df[df['stat_moment'] == 'mean']
    df_stdom = df[df['stat_moment'] == 'stderr']

    # filtering by ion
    df_mean_ion = df_mean[df_mean['ion'] == ion]
    df_stdom_ion = df_stdom[df_stdom['ion'] == ion]

    thick = df_mean_ion['PMMA'].values
    headers = list(df.columns.values)
    '''
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
    '''

# First get a cubib interpolationg function for each quantity. This will be held in a dict
# with the key being the header in df_mean and value being the function
    quant_names = list(df_mean_ion.columns[2:])
    splines = {}
    for i in quant_names:
        f2 = interp1d(thick, df_mean_ion[i], kind='cubic')
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
